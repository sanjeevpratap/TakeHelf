from rest_framework import serializers 
from .models import Tweet,UserProfile
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import Thread,Message,Topic

MAX_TWEET_LENGTH= settings.MAX_TWEET_LENGTH
TWEET_ACTION_OPTIONS = settings.TWEET_ACTION_OPTIONS 


User = get_user_model()

from .models import MakeConnection


class MakeConnectionSerializer(serializers.ModelSerializer):
    sender_username = serializers.SerializerMethodField()
    receiver_username = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()  # Add this line for the 'id' field

    class Meta:
        model = MakeConnection
        fields = ['id', 'is_friend', 'message', 'sender', 'receiver', 'sender_username', 'receiver_username']

    def get_id(self, obj):  # Define a method to get the 'id' field
        return obj.id

    def get_sender_username(self, obj):
        return obj.sender.username

    def get_receiver_username(self, obj):
        return obj.receiver.username

    





class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User  # Using your custom CustomUser model
        fields = ('id', 'username', 'email', 'is_active', 'is_staff', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
class UserProfileSerializer(serializers.ModelSerializer):
    user=serializers.SerializerMethodField(read_only=True)
    profile_picture =serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ('bio', 'profile_picture','user') 

    def get_user(self, obj):
        user = obj.user
        return {
            "id": user.id,
            "username": user.username,
            "email":user.email
        }

    def get_profile_picture(self, obj):  # Rename the method to 'get_image'
        if obj.profile_picture:
            # Assuming you have MEDIA_URL configured in your Django settings
            media_url = settings.MEDIA_URL
            return f"{media_url}{obj.profile_picture}"
        return None

class TweetActionSerializer(serializers.Serializer):
    id =serializers.IntegerField()
    action =serializers.CharField()
    content= serializers.CharField(allow_blank=True,required=False)

    def validate_action(self,value):
        value =value.lower().strip()     #"Like " -> "like"
        if not value in TWEET_ACTION_OPTIONS:
            raise serializers.ValidationError("This is not a valid action for tweets ")
        return value



class TweetCreateSerializer(serializers.ModelSerializer):     #created to manage null from retweet
    likes =serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model=Tweet
        fields=['id','content','likes','image']
    def get_likes(self,obj):
        return obj.likes.count()
    def validate_content(self,value):
        if len(value) > MAX_TWEET_LENGTH:
            raise serializers.ValidationError("This tweet is too long")
        return value
 

# class TweetSerializer(serializers.ModelSerializer):        
#     likes =serializers.SerializerMethodField(read_only=True)
#     content =serializers.SerializerMethodField(read_only=True)
    
#     parent = TweetCreateSerializer(read_only=True)
#     user = serializers.SerializerMethodField(read_only=True)
    


#     class Meta:
#         model=Tweet
#         fields=['id','content','likes','is_retweet','parent','user']
#     def get_likes(self,obj):
#         return obj.likes.count()

        
#     def get_user(self, obj):  # Serialize the user field
#         user = obj.user
#         return {
#             "id": user.id,
#             "username": user.username
#         }
from django.conf import settings
from rest_framework import serializers
from .models import Tweet

class TweetSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)
    content =serializers.SerializerMethodField(read_only=True)
    parent = TweetCreateSerializer(read_only=True)
    user = serializers.SerializerMethodField(read_only=True)
    image = serializers.SerializerMethodField(read_only=True)  # Rename the field to 'image'

    class Meta:
        model = Tweet
        fields = ['id', 'content', 'likes', 'is_retweet', 'parent', 'user', 'image']  # Include 'image' in the fields

    def get_likes(self, obj):
        return obj.likes.count()

    def get_user(self, obj):
        user = obj.user
        return {
            "id": user.id,
            "username": user.username
        }

    def get_image(self, obj):  # Rename the method to 'get_image'
        if obj.image:
            # Assuming you have MEDIA_URL configured in your Django settings
            media_url = settings.MEDIA_URL
            return f"{media_url}{obj.image}"
        return None


    def get_content(self,obj):  # related to retweet
        content = obj.content
        if obj.is_retweet:
            content = obj.parent.content


        return content 
    
    
class ThreadSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()

    class Meta:
        model = Thread
        fields = ['id', 'name', 'thread_type', 'users']

    def get_id(self, obj):
        return obj.id




class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = [ 'sender', 'sender_username', 'text', 'timestamp', 'thread']

    def get_sender_username(self, obj):
        return obj.sender.username

   

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model=Topic
        fields= '__all__'