
import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "clothing.settings")
django.setup()
from django.db.utils import IntegrityError

from user.models import Clothing, Tags, User, Rate

from user.models import Clothing



def fix():
    Clothing.objects.update(name='')