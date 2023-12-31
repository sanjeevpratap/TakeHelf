from django.conf import settings
from django.conf.urls.static import static
from tkinter import Y
from django.contrib import admin
from django.urls import path,include,re_path
from django.views.generic import TemplateView
from twapp.views import (
    home_view,
    tweets_list_view,
    tweets_detail_view,
   
    # tweets_profile_view
)
from twapp.api import views
from accounts.views import(
    login_view,
    logout_view,
    register_view
)
from accounts import views
urlpatterns = [
    # path('',views.TweetListCreate.as_view()),
    # path('',TemplateView.as_view(template_name='react_via_dj.html')),
    # re_path(r'^.*', TemplateView.as_view(template_name='react_via_dj.html')),
    path('admin/', admin.site.urls),
    path('html/', tweets_list_view,name='html'),
    # path('login/', login_view),
    # path('logout/', logout_view),
    # path('register/', register_view, name='register'),
    # path('logout/', logout_view, name='logout'),
    

    path('tweet/<str:tweet_id>', tweets_detail_view),
    # re_path(r'profiles?/', include('profiles.urls')),    #profiles is optional
    # re_path(r'profiles?/', include('profiles.urls')),    #profiles is optional
    path('api/tweets/',include('twapp.api.urls')),
    # path('',include('twapp.api.urls'))
    path('', include('twapp.urls')),
    

]

if settings.DEBUG:
    urlpatterns +=static(settings.STATIC_URL,
                document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)