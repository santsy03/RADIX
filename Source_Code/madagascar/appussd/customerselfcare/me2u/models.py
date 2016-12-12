from django.db import models


class Users(models.Model):
    username = models.CharField(max_length=20, primary_key=True)
    salt = models.CharField(max_length=20)
    password = models.CharField(max_length=50)
    attempts = models.IntegerField(max_length=1)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = u'users'
