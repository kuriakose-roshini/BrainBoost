from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib import messages
from .forms import AspirantRegistrationForm, AspirantLoginForm
from django.contrib.auth.decorators import login_required
from .models import Aspirant
import base64
import cv2
import numpy as np
import os
from django.core.files.base import ContentFile

from .train_face_model import train_face_model
User = get_user_model()
FACE_IMAGE_PATH = "media/face_images/"

def aspirant_register(request):
    if request.method == "POST":
        form = AspirantRegistrationForm(request.POST)
        captured_image = request.POST.get("captured_image")

        if not captured_image:
            messages.error(request, "Face image capture is required!")
            return render(request, 'aspirant/aspirant_register.html', {'form': form})

        if form.is_valid():
            try:
                aspirant = form.save(commit=False)

                # Decode Base64 face image and save it
                format, imgstr = captured_image.split(';base64,')
                ext = format.split('/')[-1]
                image_data = base64.b64decode(imgstr)
                filename = f"{aspirant.user.username}.{ext}"
                image_path = os.path.join("media/face_images/", filename)

                with open(image_path, "wb") as f:
                    f.write(image_data)

                aspirant.face_image = f"face_images/{filename}"
                aspirant.save()

                # Train Haarcascade model
                train_face_model()

                messages.success(request, "Registration successful! Face trained successfully.")
                return redirect('aspirant_login')

            except Exception as e:
                print(f"Error: {e}")  # Log the error in the terminal
                messages.error(request, f"Registration failed: {e}")
        else:
            print("Form errors:", form.errors)  # Print errors in the terminal
            messages.error(request, f"Registration failed. Errors: {form.errors}")

    else:
        form = AspirantRegistrationForm()

    return render(request, 'aspirant/aspirant_register.html', {'form': form})





def aspirant_login(request):
    if request.method == "POST":
        form = AspirantLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user is not None and hasattr(user, 'aspirant'):
                login(request, user)
                return redirect('aspirant_dashboard')
            else:
                messages.error(request, "Invalid credentials or not an aspirant.")
    else:
        form = AspirantLoginForm()
    return render(request, 'aspirant/aspirant_login.html', {'form': form})

@login_required
def aspirant_dashboard(request):
    return render(request, 'aspirant/aspirant_dashboard.html')