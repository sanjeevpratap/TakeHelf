from django.db import models
from django.db.models import Count

class ThreadManager(models.Manager):
    def get_or_create_personal_thread(self, user1, user2):
        # Sort the usernames alphabetically
        sorted_usernames = sorted([user1.username, user2.username])

        threads = self.get_queryset().filter(thread_type='personal')
        threads = threads.filter(users__in=[user1, user2]).distinct()
        threads = threads.annotate(u_count=Count('users')).filter(u_count=2)

        if threads.exists():

            print(threads," ttttttttttttttttttttttttttttttttttttttttttttttt",sorted_usernames)
            return threads.first()
        else:
            thread = self.create(thread_type='personal')
            thread.users.add(user1)
            thread.users.add(user2)
            thread.name = f'{sorted_usernames[0]} and {sorted_usernames[1]}'  # Set the room name
            thread.save()
            return thread

    def by_user(self, user):
        return self.get_queryset().filter(users__in=[user])

