from django.db import models
from django.conf import settings

class Aspirant(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    face_image = models.ImageField(upload_to='face_images/', blank=False, null=False)  # Mandatory for login
    date_of_birth = models.DateField()
    parent_name = models.CharField(max_length=150, blank=True, null=True)
    parent_email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.user.username
