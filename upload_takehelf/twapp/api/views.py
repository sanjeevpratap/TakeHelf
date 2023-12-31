from http.client import HTTPResponse
import random
from django.shortcuts import render,redirect,HttpResponse
from django.http import HttpResponse,Http404,JsonResponse,HttpResponseRedirect

from tweetme.settings import ALLOWED_HOSTS
from ..models import Tweet ,UserProfile,Thread,Message,Topic
from ..forms import TweetForm
from django.utils.http import url_has_allowed_host_and_scheme
from django.conf import  settings
from ..serializers import TweetSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from django.contrib.auth import authenticate, login,logout
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from ..serializers import TweetSerializer,TweetActionSerializer,TweetCreateSerializer,CustomUserSerializer,UserProfileSerializer
from rest_framework.authentication import SessionAuthentication
from django.contrib.auth.decorators import login_required
from rest_framework.generics import ListAPIView,CreateAPIView,ListCreateAPIView
from rest_framework.authtoken.models import Token
from django.http import HttpResponseForbidden

from django.contrib.auth import get_user_model  
from django.shortcuts import get_object_or_404
ALLOWED_HOSTS =settings.ALLOWED_HOSTS
User = get_user_model()

from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in

from ..serializers import ThreadSerializer, MessageSerializer,TopicSerializer
from rest_framework import generics


from rest_framework import generics, status
from rest_framework.response import Response
# from urllib.parse import unquote


# from urllib.parse import unquote
from rest_framework import generics
from twapp.models import Thread, Message
from twapp.serializers import MessageSerializer
from rest_framework.parsers import MultiPartParser
from ..models import MakeConnection,CustomUser
from ..serializers import  MakeConnectionSerializer


from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from rest_framework.serializers import ValidationError
from .ml import run_lda_algorithm
from django.db.models.signals import post_save







# CONNECTION AND NETWORK PART


@api_view(['GET'])
def get_friends_list(request):
 
    sent_connections = MakeConnection.objects.filter(sender=request.user, is_friend='YES')
    received_connections = MakeConnection.objects.filter(receiver=request.user, is_friend='YES')

    friend_connections = sent_connections | received_connections

    response_obj = []

    for connection in friend_connections:
        if connection.sender != request.user:
            friend_info = {
                'id': connection.sender.id,
                'username': connection.sender.username,
            }
            response_obj.append(friend_info)

        if connection.receiver != request.user:
            friend_info = {
                'id': connection.receiver.id,
                'username': connection.receiver.username,
            }
            response_obj.append(friend_info)

    # serializer = MakeConnectionSerializer(friend_connections, many=True, context={'request': request.user})

    return Response(response_obj)

   


@api_view(['POST'])
def send_connection_request(request):
    receiver_username = request.data.get('receiver_username')

    if not receiver_username:
        return Response({'error': 'Receiver username is required'}, status=status.HTTP_400_BAD_REQUEST)

    receiver = get_object_or_404(CustomUser, username=receiver_username)

    # Get the IDs of the currently logged-in user (request.user) and the receiver
    sender_id = request.user.id
    receiver_id = receiver.id

    # Use sender_id and receiver_id when creating the MakeConnection instance
    connection = MakeConnection.objects.create(sender_id=sender_id, receiver_id=receiver_id, is_friend='IN_PROCESS')

    # Serialize the connection and the receiver user
    connection_serializer = MakeConnectionSerializer(connection)
    response_data = {
    'connection_id': connection.id,
    'sender_id': request.user.id,
    'sender_username': request.user.username,
    'receiver_id': receiver.id,
    'receiver_username': receiver.username,
    'connection_status': connection.is_friend,
    'message': 'Connection request sent successfully!',
    'sent_at': timezone.now().isoformat(),  # Include the current date and time
        # Add more details as needed
    }

    return Response(response_data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def connection_requests_received(request):

    connection_requests = MakeConnection.objects.filter(receiver=request.user.id, is_friend='IN_PROCESS')
    serializer = MakeConnectionSerializer(connection_requests, many=True)
    return Response(serializer.data)
   

@api_view(['PUT'])
def accept_connection_request(request):
    if not request.user.is_authenticated:
        return Response({'detail': 'User not authenticated'}, status=401)

    connection_id = request.data.get('id')
    connection = get_object_or_404(MakeConnection, pk=connection_id, receiver=request.user, is_friend='IN_PROCESS')
    
    # Update the connection status to 'YES'
    connection.is_friend = 'YES'
    
    # Save the changes to the MakeConnection object
    connection.save()
    thread_obj = Thread.objects.get_or_create_personal_thread(request.user, connection.sender)
    
    # Serialize the updated MakeConnection object using the serializer
    serializer = MakeConnectionSerializer(connection)
    
    # Return the serialized data in the response
    return Response(serializer.data)









#CHATTING PART

class MessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    #print("enterde")
    def get_queryset(self):
        thread_name = self.kwargs.get('name')
        #print(thread_name, "......................................")
        
        if thread_name is not None:
            try:
                thread = Thread.objects.get(name=thread_name)
                queryset = Message.objects.filter(thread=thread)
                #print(queryset, "11111111111111111111111111111111111111111111111111111111")
                return queryset
            except Thread.DoesNotExist:
                return []
        else:
            return []
        

class MessageCreateView1(generics.CreateAPIView):
    serializer_class = MessageSerializer

    def create(self, request, *args, **kwargs):
        sender = request.user
        thread_name = request.data.get('thread')
        text = request.data.get('text')

        # Retrieve the thread object by name
        thread_obj = Thread.objects.get(name=thread_name)

        # Pass context with sender and thread information to the serializer
        serializer = self.get_serializer(data={'text': text, 'sender': sender, 'thread': thread_obj})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'testing': 'done'}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def creatMessage(request):
    sender = request.user
    thread_name = request.data.get('threadData')
    text = request.data.get('text')
    
    # Debugging print statements
    print(f"Thread Name: {thread_name}")
    
    try:
        thread_obj = Thread.objects.get(id=thread_name)
        print(f"Thread Object Name: {thread_obj.name}")
    except Thread.DoesNotExist:
        print("Thread does not exist.")
        return Response({'error': 'Thread does not exist.'}, status=400)

    # Instantiate the serializer with the correct arguments
    serializer = MessageSerializer(data={'sender': sender.id, 'text': text, 'thread': thread_obj.id})
    
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data, status=200)
    else:
        print(serializer.errors)
        return Response({'error': "something went wrong"}, status=400)


class ThreadListView(generics.ListAPIView):
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer
    
    def get_queryset(self):
        thread_name=self.kwargs.get('name')
        if thread_name is not None:
            try:
                thread=Thread.objects.get(name=thread_name)
                queryset=Message.objects.filter(thread=thread)
                return queryset
            except:
                return []
        else:
            return []





#USER AND PROFILE PART

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_authenticated_user(request):
    user = request.user  # This is the user associated with the token
    return Response({'id':user.id, 'username': user.username, 'email': user.email},status=200)


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)


@api_view(['GET'])
@permission_classes([IsAuthenticated])  
def user_profile_view(request, user):
    # pass
    user = get_object_or_404(CustomUser, username=user)
    #print(user)
    user_profile = get_object_or_404(UserProfile, user=user)
    serializer = UserProfileSerializer(user_profile)
    return Response(serializer.data, status=200)


# @receiver(user_logged_in)
# def ensure_user_profile(sender, request, user, **kwargs):
#     UserProfile.objects.get_or_create(user=user)












#AUTHENTICATION PART

@api_view(["POST"])
def register_user(request):
    serializer = CustomUserSerializer(data=request.data)
    #print(request.data)
    if serializer.is_valid():
        user = serializer.save()
        #print(user)
        token, created= Token.objects.get_or_create(user=user)
        return Response({"token": token.key,"success":True},status=200)
    return Response(serializer.errors, status=401)



@api_view(["POST"])
def login_user(request):
    username=request.data.get("username")
    
    password = request.data.get("password")
    
    user = authenticate(request,username=username , password=password)
    if user is not None:
        login(request,user)
        token, _ = Token.objects.get_or_create(user=user)         
        return Response({"token": token.key, "success": True},status=200)
    else:
        return Response({"error": "Invalid credentials", "success": False}, status=401)

@api_view(['POST'])  # You can change the HTTP method as needed
@permission_classes([IsAuthenticated])
def logout_user(request):
    logout(request)
    response = Response({'message': 'Logged out successfully'}, status=200)
    response.delete_cookie('access_token')  # Delete the token cookie
    return response






class TopicListView(generics.ListAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
















# @api_view(['POST'])    #http method the client == POST
# @permission_classes([IsAuthenticated])     #this deal with permission that user is allowed to do below operations
# def tweet_create_view(request, *args, **kwargs):
    
#     if request.user.is_authenticated:
#         authenticated_user = request.user
#         print("Authenticated user:", authenticated_user)
#     serializer= TweetCreateSerializer(data=request.data )
    
    
#     if serializer.is_valid(raise_exception=True):
        
#         serializer.save(user=request.user )
        
#         return Response(serializer.data,status=201)
    
#     return Response({"error":"this is eroor"},status=400)

class TweetListCreate(ListCreateAPIView):
    queryset=Tweet.objects.all()
    serializer_class=TweetCreateSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def tweet_create_view(request, *args, **kwargs):
    print("request data",request.data)
    tweet_content = request.data.get('content', '')
    existing_topics=Topic.objects.all()
    topic_names,unchanged_list = run_lda_algorithm(tweet_content,existing_topics)
   

    serializer = TweetCreateSerializer(data=request.data, context={'request': request})
    
    print( "    user search",topic_names, unchanged_list)
    if serializer.is_valid(raise_exception=True):
        new_tweet=serializer.save(user=request.user)
        
        # Update topic model, set topics as active, and increase post count
        for name in topic_names:
            topic, created = Topic.objects.get_or_create(name=name)
            topic.is_active = True
            topic.post_count += 1  # Increase post count
            topic.save()
        unchanged_topics = [Topic.objects.get_or_create(name=name)[0] for name in unchanged_list]

        new_tweet.topics.add(*unchanged_topics)

        # print(serializer.data, "................")
        return Response(serializer.data, status=201)

    return Response({"error": "this is an error"}, status=400)


@api_view(['POST'])
def topic_fix_view(request):
    topic_list = request.data.get('list', [])
    
    print("Topic list are.................... ", topic_list)

    user_profile_instance = UserProfile.objects.get(user=request.user)

    try:
        # Add the topic IDs to the selected_topics field
        user_profile_instance.selected_topics.add(*topic_list)
        return Response({"Response": "Successfully updated selected topics"})
    except Exception as e:
        print("Error:", e)
        return Response({"Error": "Error occurred during update"})

from django.db.models import Q

@api_view(['GET'])
def get_related_post(request):
    # Assuming you have the user information in the request or you can get it from the request
    user_profile = UserProfile.objects.get(user=request.user)

    # Get the topics associated with the user's UserProfile
    user_topics = user_profile.selected_topics.all()

    # Retrieve tweets that have topics related to the user's topics
    related_tweets = Tweet.objects.filter(topics__in=user_topics).exclude(user=request.user).distinct()

    # You can now serialize and return the related_tweets
    serializer = TweetSerializer(related_tweets, many=True)
    
    return Response(serializer.data)








@api_view(['GET'])   #http method the client == GET
def tweet_detail_view(request,tweet_id,*args,**kwargs):
     qs=Tweet.objects.filter(id=tweet_id)
     if not qs.exists():
        return Response({},status=404)
     obj =qs.first()
     serializer= TweetSerializer(obj)
    
     return Response(serializer.data,status=200)

     
@api_view(['DELETE','POST'])   #http method the client == GET
@permission_classes([IsAuthenticated])
def tweet_delete_view(request,tweet_id,*args,**kwargs):
     qs=Tweet.objects.filter(id=tweet_id)
     if not qs.exists():
        return Response({},status=404)
     qs=qs.filter(user=request.user)
     if not qs.exists():
        return Response({"message": " you cannot delete this tweet"},status=401  )
     obj =qs.first()
     obj.delete()
     #serializer= TweetSerializer(obj)
    
     return Response({"message":"Tweet deleted"},status=200)


@api_view(['POST'])   #http method the client == GET
@permission_classes([IsAuthenticated])
def tweet_action_view(request,*args,**kwargs):
    #print("hello   ")
    '''
    id is required.
    Action options are: like,unlike,retweet
    '''
    #print(request,request.data,"  ........")
    serializer =TweetActionSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
       data = serializer.validated_data
       tweet_id =data.get("id")
       action =data.get("action")
    #    content='okk'
       
    #    #print(data, tweet_id, action, content)
       qs=Tweet.objects.filter(id=tweet_id)
       if not qs.exists():
          return Response({},status=404)
       
       obj =qs.first()
       #print(qs,"////////////////////////////",obj)
       if action == "like":
          obj.likes.add(request.user)
          serializer =TweetSerializer(obj)
          #print("sessssssssssssssss")
          return Response(serializer.data,status=200)

       elif action == "unlike":
          obj.likes.remove(request.user)
          serializer =TweetSerializer(obj)
          return Response(serializer.data,status=200)
       elif action == "retweet":

        
        new_tweet = Tweet.objects.create(user=request.user,parent=obj) #creating retweet parent
        serializer =TweetSerializer(new_tweet)
        return Response(serializer.data,status=201)
        

    

    return Response({},status=200)

@api_view(['GET'])   #http method the client == GET

def tweet_list_view(request,*args,**kwargs):
     qs=Tweet.objects.all()
     username= request.GET.get('username')
 
    
     if username !=None:
        qs=qs.filter(user__username__iexact=username)
     serializer= TweetSerializer(qs,many=True)
     #print(serializer)
    #  print(serializer.data)
     return Response(serializer.data)


class PostListView(generics.ListAPIView):
    serializer_class=TweetSerializer
    queryset=Tweet.objects.all()
























































































def tweet_create_view_pure_django(request, *args, **kwargs):
    # #print(abc)   for server error checking
    user =request.user
    if not request.user.is_authenticated:
        user= None
        if request.accepts("pages/home.html"):
            
            return JsonResponse({}, status=401)
        return redirect(settings.LOGIN_URL)
    form = TweetForm(request.POST or None)
    next_url= request.POST.get("next") or None
   
    
    if form.is_valid():
        #print("valid")
        
        obj=form.save(commit=False)
        obj.user =request.user or None     #Annamous user(none user)
        obj.save()
        
        if request.accepts("pages/home.html"):
            return JsonResponse(obj.serialize(), status=201)    # 201 == created items
        # if next_url !=None and is_safe_url(next_url,ALLOWED_HOSTS) :
        if next_url !=None and url_has_allowed_host_and_scheme(next_url,ALLOWED_HOSTS) :
            
            return redirect(next_url)
        
        form = TweetForm()
    if form.errors:
        if request.accepts("pages/home.html"):
            
            return JsonResponse(form.errors, status=400)
    
    return render(request ,'components/form.html',context={"form":form})



def tweet_list_view_pure_django(request,*args,**kwargs):
    qs=Tweet.objects.all()
    tweet_list= [ x.serialize() for x in qs]
    # tweet_list= [{"id": x.id,  "content":x.content , "likes": random.randint(0,232)} for x in qs]
    data= {
        "isUser": False,
        "response": tweet_list
    }
    return JsonResponse(data)

def tweet_detail_view_pure_django(request,tweet_id,*args,**kwargs):

    """
    REST API VIEW 
      return json data
    """
    
    ##print(args,kwargs,tweet_id)
    data={
        "id":tweet_id,
        # "content":obj.content,
    }
    status=200
    try:
        obj=Tweet.objects.get(id=tweet_id)
        data['content'] = obj.content
    except:
        data['message'] = "Not found"
        status = 404
   
    return JsonResponse(data,status=status)
    # return HttpResponse(f"hello  {tweet_id}- {obj.content}")