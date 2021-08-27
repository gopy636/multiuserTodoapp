from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .manager import UserManager
import uuid

class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=100, unique=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=13, null=True, blank=True)
    verification_token = models.CharField(max_length=100, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title=models.CharField(max_length=100)
    descriptions=models.CharField(max_length=250)
    startime = models.DateTimeField()
    endtime =models.DateTimeField()
    user= models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='event')
    url=models.URLField(max_length=200,null=True,blank=True)
    user_doc=models.FileField(upload_to='file',blank=True,null=True)
    is_completed=models.BooleanField(default=False)
    is_pending=models.BooleanField(default= True)
    add_member=models.ManyToManyField(CustomUser,related_name='member')

        

    
    




