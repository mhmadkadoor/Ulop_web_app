from django.db import models
from django.contrib.auth.models import User
import os
from django.conf import settings
# Create your models here.

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/profile_pics/user_<id>/<filename>
    return f"profile_pics/user_{instance.user.id}/{filename}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='profile_pics/male_def.jpg', upload_to=user_directory_path)
    bio = models.TextField(default='No bio')
    

    def __str__(self):
        return f'{self.user.username} Profile'

    def delete(self, *args, **kwargs):
        # Delete the image file
        if self.image:
            image_path = os.path.join(settings.MEDIA_ROOT, self.image.name)
            if os.path.isfile(image_path):
                os.remove(image_path)
        super().delete(*args, **kwargs)  # Call the "real" delete() method.

    class Meta:
        verbose_name = "All Profile"
        ordering = ['user_id']