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
        # Delete the entire folder associated with the user's profile image
        if self.image:
            folder_path = os.path.join(settings.MEDIA_ROOT, f"profile_pics/user_{self.user.id}")
            if os.path.exists(folder_path):
                # Remove the folder and its contents
                for filename in os.listdir(folder_path):
                    file_path = os.path.join(folder_path, filename)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                os.rmdir(folder_path)
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = "All Profile"
        ordering = ['user_id']