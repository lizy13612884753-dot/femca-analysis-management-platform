import os
import django

if os.getenv("CI") != "true":
    raise RuntimeError("This script must only run in CI")

username = os.environ["CI_TEST_USERNAME"]
email = os.environ["CI_TEST_EMAIL"]
password = os.environ["CI_TEST_PASSWORD"]

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "femca_platform.settings")
django.setup()
from django.contrib.auth import get_user_model

User = get_user_model()

user, created = User.objects.get_or_create(
    username=username,
    defaults={
        "email": email,
        "role": "viewer"
    }
)

user.set_password(password)
user.save()
