from django.db import models


class Whitelist(models.Model):
    id = models.IntegerField(primary_key=True)
    msisdn = models.CharField(max_length=15)
    active = models.IntegerField(max_length=1)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = u'me2u_whitelist'


class DealerWhitelist(models.Model):
    id = models.IntegerField(primary_key=True)
    msisdn = models.CharField(max_length=15)
    active = models.IntegerField(max_length=1)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = u'dealer_me2u_whitelist'
