from django.db import models
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, UserManager
)
from PIL import Image
import os
from solo.models import SingletonModel


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    linkedin = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    profile_photo = models.ImageField(
        'Foto de perfil', blank=True, null=True,
        upload_to='profiles_photos/'
    )
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    @staticmethod
    def resize_image(image, new_width=208):
        image_full_path = os.path.join(settings.MEDIA_ROOT, image.name)
        image_pillow = Image.open(image_full_path)
        original_width, original_height = image_pillow.size

        if original_width <= new_width:
            image_pillow.close()

            return

        new_height = round((new_width * original_height) / original_width)
        new_image = image_pillow.resize((new_width, new_height), Image.LANCZOS)

        new_image.save(
            image_full_path,
            optimize=True,
            quality=50,
        )
    
    def save(self, *args, **kwargs):
        saved = super().save(*args, **kwargs)

        if self.profile_photo:
            try:
                self.resize_image(self.profile_photo)
            except FileNotFoundError:
                pass
        
        return saved

    def __str__(self):
        return f'User {self.id} - {self.email}'

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        db_table = 'users'
        ordering = ['id']


class ProjectsDate(SingletonModel):
    start_date = models.DateTimeField('Data inicial', null=True)
    end_date = models.DateTimeField('Data final', null=True)

    def __str__(self):
        return f'Prazo: {self.start_date} - {self.end_date}'

    class Meta:
        db_table = 'prazo'
        verbose_name = 'prazo'
