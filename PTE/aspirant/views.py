# views.py in your aspirant app
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .models import Aspirant
from .face_utils import FaceRecognition
from .forms import AspirantRegistrationForm, AspirantLoginForm
import cv2
face_recognition = FaceRecognition()


def register_aspirant(request):
    if request.method == 'POST':
        form = AspirantRegistrationForm(request.POST)
        if form.is_valid():
            try:
                # Save user but don't commit to DB yet
                user = form.save(commit=False)

                # Set any additional fields
                user.is_active = True  # Activate user immediately

                # Save to database
                user.save()

                # Initialize face recognition
                face_recognition = FaceRecognition()

                try:
                    # Capture face images (60 samples)
                    images_captured = face_recognition.capture_images(user.id)

                    if images_captured < 30:  # Minimum threshold
                        user.delete()  # Rollback user creation
                        messages.error(request,
                                       'Failed to capture sufficient face images. Please try again in better lighting.'
                                       )
                        return render(request, 'aspirant/aspirant_register.html', {'form': form})

                    messages.success(request,
                                     f'Registration successful! {images_captured} face images captured. Please login.'
                                     )
                    return redirect('aspirant_login')

                except cv2.error as e:
                    user.delete()  # Rollback user creation
                    messages.error(request,
                                   'Camera error. Please ensure your camera is connected and try again.'
                                   )
                    return render(request, 'aspirant/aspirant_register.html', {'form': form})

                except Exception as e:
                    user.delete()  # Rollback user creation
                    messages.error(request,
                                   f'Face registration failed: {str(e)}'
                                   )
                    return render(request, 'aspirant/aspirant_register.html', {'form': form})

            except Exception as e:
                messages.error(request,
                               f'Registration failed: {str(e)}'
                               )
                return render(request, 'aspirant/aspirant_register.html', {'form': form})

    else:
        form = AspirantRegistrationForm()

    return render(request, 'aspirant/aspirant_register.html', {
        'form': form,
        'camera_required': True  # Flag for template to show camera warning
    })

def login_aspirant(request):
    if request.method == 'POST':
        form = AspirantLoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)

            if user is not None:
                # Perform face recognition
                recognized_user_id = face_recognition.recognize_face()

                if recognized_user_id == user.id:
                    login(request, user)
                    messages.success(request, f'Welcome {user.username}!')
                    return redirect('aspirant_dashboard')
                else:
                    messages.error(request, 'Face recognition failed. Please try again.')
            else:
                messages.error(request, 'Invalid email or password.')
    else:
        form = AspirantLoginForm()

    return render(request, 'aspirant/aspirant_login.html', {'form': form})

@login_required
def dashboard_aspirant(request):
    return render(request, 'aspirant/aspirant_dashboard.html')

