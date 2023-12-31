
from django.urls import path
from twapp.api.views import (
    tweet_delete_view,
    tweet_action_view,
    tweet_detail_view,
    tweet_list_view,
    tweet_create_view,
    register_user,
    login_user,
    logout_user,
    user_profile_view,
    get_authenticated_user,
    MessageListView,
    PostListView,
    TopicListView,
    send_connection_request,
    connection_requests_received,
    accept_connection_request,
    get_friends_list,
    creatMessage,
    topic_fix_view,
    get_related_post,

   

    
)

urlpatterns = [
    
    path('', tweet_list_view,name='tweet-list'),
    path('listlist', PostListView.as_view(),name='listlist'),
    # path('<str:uname>', tweet_list_view,name='list'),
    # path('', tweet_create_view,name="create"),
    
    path('create', tweet_create_view,name="create"),
    path('action',tweet_action_view),
    path('<int:tweet_id>', tweet_detail_view),
    path('<int:tweet_id>/delete', tweet_delete_view),
    path('register_user',register_user,name='register_user'),
    path('login_user',login_user,name='login_user'),
    path('profile/<str:user>',user_profile_view,name='profile'),
    path('logout_user',logout_user,name='logout_user'),
    path('get_authenticated_user',get_authenticated_user,name='get_authenticated_user'),
    path('message/<str:name>',MessageListView.as_view(),name='message'),
    path('topic',TopicListView.as_view(),name='topic'),
    path('createMessage',creatMessage,name='createmessage'),
    path('sendRequest',send_connection_request,name='sendRequest'),
    path('connectionRequest',connection_requests_received,name='connectionRequest'),
    path('acceptRequest',accept_connection_request,name='acceptRequest'),
    path('get_freinds_list',get_friends_list,name='get_freinds_list'),
    path('fix_topic',topic_fix_view,name='fix_topic'),
    path('related_post',get_related_post,name='related_post'),


    

]

