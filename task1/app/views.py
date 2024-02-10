from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import CustomUserCreationForm, LoginForm
from .models import Patient, Doctor
import os

def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user_type = form.cleaned_data.get('user_type')
            if user_type == 'patient':
                user.is_patient = True                
            elif user_type == 'doctor':
                user.is_doctor = True
            else:
                raise ValueError('User must be either patient or doctor.')
            user.save()  # Save the user after setting the user type

            # Continue with creating Patient or Doctor instances
            if user.is_patient:
                patient = Patient.objects.create(user=user)
                patient.save()
            elif user.is_doctor:
                doctor = Doctor.objects.create(user=user)
                doctor.save()
            request.session['user_info'] = {
                'first_name': user.first_name, 
                'last_name': user.last_name, 
                'username': user.username, 
                'email': user.email, 
                'user_type': user_type, 
                'address_line1': user.address_line1, 
                'city': user.city, 
                'state': user.state, 
                'pincode': user.pincode, 
                'profile_pictures': user.profile_pictures.url
            }

            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_patient:
                    request.session['is_patient'] = True
                    return redirect('patient_dashboard')
                elif user.is_doctor:
                    request.session['is_doctor'] = True
                    return redirect('doctor_dashboard')
            else:
                 messages.error(request, 'Invalid username or password. Please try again.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    if request.method == 'POST':
        logout(request)
        if 'is_patient' in request.session:
            del request.session['is_patient']
        elif 'is_doctor' in request.session:
            del request.session['is_doctor']
    return redirect('home')

#if user is patient, & in session, then render patient_dashboard
@login_required
def patient_dashboard(request):
    if 'is_patient' in request.session:
        user_info = request.session.get('user_info', {})
        return render(request, 'patient_dashboard.html', {'user': request.user, 'user_info': user_info})
    else:
        return redirect('home')




@login_required
def doctor_dashboard(request):
    if 'is_doctor' in request.session:
        user_info = request.session.get('user_info', {})
        return render(request, 'doctor_dashboard.html', {'user': request.user, 'user_info': user_info})
    else:
        return redirect('home')

