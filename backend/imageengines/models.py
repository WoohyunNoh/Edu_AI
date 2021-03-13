from django.db import models
from accounts.models import User

class Project(models.Model):
    # id   = models.AutoField(primary_key=True)
    user = models.ForeignKey('accounts.User', on_delete = models.CASCADE)
    # path = models.TextField(verbose_name = 'path')
    create_date = models.DateTimeField(auto_now=True)
    result = models.BooleanField(default=False)
    name = models.TextField(max_length=255, default='')

