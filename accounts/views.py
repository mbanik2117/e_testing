# accounts/views.py
import random
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from accounts.forms import CustomUserCreationForm  # Import your custom form
from .models import CustomUser
from .task_1 import send_signup_email, send_signup_verification, send_login_verification


class SignupView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'accounts/signup.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = user.username  # Set email as the same value as username
            user.save()

            # Generate a 6-digit random code
            verification_code = str(random.randint(100000, 999999))

            # Store the verification code in the user object
            user.verification_code = verification_code
            user.save()

            # Call the Celery task to send the verification code asynchronously
            send_signup_verification.apply_async(args=[user.id, verification_code])

            # Redirect to the verification page
            return redirect('signup_code_verification', user_id=user.id)

        return render(request, 'accounts/signup.html', {'form': form})


class SignupVerificationView(View):
    def get(self, request, user_id):
        return render(request, 'accounts/signup_verification_page.html', {'user_id': user_id})

    def post(self, request, user_id):
        user = CustomUser.objects.get(pk=user_id)
        entered_code = request.POST.get('verification_code', '')

        # Check if the entered code matches the stored verification code
        if entered_code == user.verification_code:
            send_signup_email.apply_async(args=[user.id])
            login(request, user)
            return redirect('home')  # Redirect to home upon successful verification
        else:
            # Handle code mismatch, you can display an error message
            return render(request, 'accounts/signup_verification_page.html', {'user_id': user_id, 'error': True})


class ResendVerificationCodeView(View):
    def post(self, request, user_id):
        user = CustomUser.objects.get(pk=user_id)
        verification_code = str(random.randint(100000, 999999))

        # Update the stored verification code in the user object
        user.verification_code = verification_code
        user.save()

        # Call the Celery task to send the new verification code asynchronously
        send_signup_verification.apply_async(args=[user.id, verification_code])

        return redirect('signup_code_verification', user_id=user.id)


class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'accounts/login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()

            # Generate a 6-digit random code for login verification
            verification_code = str(random.randint(100000, 999999))

            # Store the verification code in the user object
            user.login_verification_code = verification_code
            user.save()

            # Call the Celery task to send the verification code asynchronously
            send_login_verification.apply_async(args=[user.id, verification_code])

            # Redirect to the login verification page
            return redirect('login_verification', user_id=user.id)

        return render(request, 'accounts/login.html', {'form': form})


class LoginVerificationView(View):
    def get(self, request, user_id):
        return render(request, 'accounts/login_verification.html', {'user_id': user_id})

    def post(self, request, user_id):
        user = CustomUser.objects.get(pk=user_id)
        entered_code = request.POST.get('verification_code', '')

        # Check if the entered code matches the stored verification code
        if entered_code == user.login_verification_code:
            login(request, user)
            return redirect('home')  # Redirect to home upon successful verification
        else:
            # Handle code mismatch, you can display an error message
            messages.error(request, 'Invalid verification code. Please try again.')
            return render(request, 'accounts/login_verification.html', {'user_id': user_id})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')

