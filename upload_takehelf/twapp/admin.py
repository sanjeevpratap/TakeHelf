from django.contrib import admin


from .models import Tweet,TweetLike,UserProfile
from .models import CustomUser


from .models import Thread, Message,MakeConnection,Topic



admin.site.register(Topic)

admin.site.register(CustomUser)

admin.site.register(MakeConnection)


class TweetLikeAdmin(admin.TabularInline):
    model =TweetLike

class TweetAdmin(admin.ModelAdmin):
    inlines=[TweetLikeAdmin]
    list_display =['__str__','user']
    search_fields = ['content','user__username','user__email']
    class Meta:
        model =Tweet
admin.site.register(Tweet,TweetAdmin)
admin.site.register(UserProfile)


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ('name', 'thread_type')
    filter_horizontal = ('users',)  

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('thread', 'sender', 'text', 'created_at')
    list_filter = ('thread', 'sender')
    search_fields = ('thread__name', 'sender__username', 'text')