from http.client import HTTPResponse
import random
from django.shortcuts import render,redirect,HttpResponse
from django.http import HttpResponse,Http404,JsonResponse,HttpResponseRedirect

from tweetme.settings import ALLOWED_HOSTS
from .models import Tweet
from .forms import TweetForm
from django.utils.http import url_has_allowed_host_and_scheme
from django.conf import  settings
from .serializers import TweetSerializer


ALLOWED_HOSTS =settings.ALLOWED_HOSTS

# def home_view(request,*args,**kwargs):
#     print(request.user or none)
#     #print(args,kwargs)
#     # return HttpResponse("hello world")
#     return render(request,"pages/home.html",context={},status=200)

def home_view(request, *args,**kwargs):
    username:None
    if request.user.is_authenticated:
        username = request.user.username
    return render(request,"pages/home.html",context={},status=200)

def tweets_list_view(request, *args,**kwargs):

    # qs=Tweet.objects.all()
    username= request.GET.get('username')
 
    
    # if username !=None:
    #     qs=qs.filter(user__username__iexact=username)
    return render(request,"tweets/list.html",context={'user':username},status=200)

def tweets_detail_view(request,tweet_id, *args,**kwargs):
    return render(request,"tweets/detail.html")


