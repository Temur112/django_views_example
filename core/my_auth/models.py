from django.db import models
from django.contrib.auth.models import User
# Create your models here.


def user_avatar_path(instance, filename):
    return "avatars/images/user_{pk}/{filename}".format(pk=instance.pk, filename=filename)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True, null=False)
    agreement_accepted = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to=user_avatar_path, blank=True, null=True)

    def __str__(self):
        return str(self.user.username)


