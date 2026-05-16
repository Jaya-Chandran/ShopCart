from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        username = os.environ.get('ADMIN_USER', 'admin')
        password = os.environ.get('ADMIN_PASS', 'jai1234')
        email = os.environ.get('ADMIN_EMAIL', 'jaichandranr28@gmail.com')
        
        if User.objects.filter(username=username).exists():
            u = User.objects.get(username=username)
            u.set_password(password)
            u.is_staff = True
            u.is_superuser = True
            u.save()
            self.stdout.write(f'Admin password RESET: {username}')
        else:
            User.objects.create_superuser(username, email, password)
            self.stdout.write(f'Admin CREATED: {username}')