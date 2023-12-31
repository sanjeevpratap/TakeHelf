from django.db import models
import random
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from datetime import datetime
from django.contrib.auth.models import BaseUserManager

from twapp.managers import ThreadManager
# User =settings.AUTH_USER_MODEL



class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        
        return self.create_user(username, email, password, **extra_fields)


class CustomUser(AbstractBaseUser):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    objects = CustomUserManager()

    USERNAME_FIELD = "username"  # Set username as the USERNAME_FIELD
    EMAIL_FIELD = "email"
    
    REQUIRED_FIELDS = [ "email"]  # Added "username" to the list

    def __str__(self):
        return self.username

    def get_full_name(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return self.is_staff

    def has_module_perms(self, app_label):
        "Does the user have permission to view the app `app_label`?"
        return True

class Topic(models.Model):
    name=models.CharField(max_length=255,unique=True)
    is_active=models.BooleanField(default=False)
    post_count=models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    selected_topics=models.ManyToManyField(Topic ,related_name='user_profiles')

    def __str__(self):
        return self.user.username

class TweetLike(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    tweet = models.ForeignKey("Tweet",on_delete=models.CASCADE)
    timestamp =models.DateTimeField(auto_now_add=True)

    

class Tweet(models.Model):
    # Map to SQL DATA
    #id = models.AutoFields(primary_key=True)
    parent = models.ForeignKey("self",null=True,on_delete=models.SET_NULL)
    user =models.ForeignKey(CustomUser , on_delete=models.CASCADE)    # one users can have many tweets
    likes =models.ManyToManyField(CustomUser,related_name='tweet_user',blank=True,through=TweetLike)
    content=models.TextField(blank=True, null=True)
    image= models.FileField(upload_to='images/', blank=True, null=True)
    topics = models.ManyToManyField(Topic, related_name='posts')
    timestamp =models.DateTimeField(auto_now_add=True)
    
   
    class Meta:
        ordering = ['-id']

    @property
    def is_retweet(self):
        return self.parent !=None
    
    # def serialize(self):    created when serializer file was not there and changig in to json in model not in view.
    #     return {
    #         "id": self.id,
    #         "content": self.content,
    #         "likes": random.randint(0,200)
    #     }


#for chatting ................
class TrackingModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Thread(TrackingModel):
    THREAD_TYPE = (
        ('personal', 'Personal'),
        ('group', 'Group')
    )
    name = models.CharField(max_length=50, null=True, blank=True)
    thread_type = models.CharField(max_length=15, choices=THREAD_TYPE, default='group')
    # users = models.ManyToManyField(User)  # Using the actual User model from django.contrib.auth
    users = models.ManyToManyField(settings.AUTH_USER_MODEL)  # Using the actual User model from django.contrib.auth
    # users = models.ManyToManyField(CustomUser)  
    
    objects = ThreadManager()  # Default manager

    def __str__(self):
        if self.thread_type == 'personal' and self.users.count() == 2:
            return f'{self.users.first()} and {self.users.last()}'
        return f'{self.name}'



class Message(TrackingModel):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField(blank=False, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'From <Thread - {self.thread}>'


class MakeConnection(models.Model):
    sender = models.ForeignKey(CustomUser, related_name='connection_requests_sent', on_delete=models.CASCADE)
    receiver = models.ForeignKey(CustomUser, related_name='connection_requests_received', on_delete=models.CASCADE)
    is_friend_choices = [
        ('YES', 'Yes'),
        ('NO', 'No'),
        ('IN_PROCESS', 'In Process'),
    ]
    is_friend = models.CharField(max_length=10, choices=is_friend_choices, default='NO')
    message = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.sender} to {self.receiver}: {self.is_friend}"

    def accept_connection(self):
        if self.is_friend == 'IN_PROCESS':
            self.is_friend = 'YES'
            self.save()

    def send_connection(self):
        if self.is_friend == 'NO':
            self.is_friend = 'IN_PROCESS'
            self.save()


