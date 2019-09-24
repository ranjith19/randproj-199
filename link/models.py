from django.db import models
import random
import string


def get_random_string():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))

# Create your models here.


class UPILink(models.Model):
    link = models.TextField()
    identifier = models.CharField(default=get_random_string, max_length=20)
