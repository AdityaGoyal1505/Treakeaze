import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conference_mgmt.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
username = 'superadmin'
email = 'superadmin@example.com'
password = 'SuperAdmin123!'

u = User.objects.filter(username=username).first()
if u:
    print(f'Superuser "{username}" already exists')
else:
    User.objects.create_superuser(username, email, password)
    print(f'Superuser "{username}" created successfully')
