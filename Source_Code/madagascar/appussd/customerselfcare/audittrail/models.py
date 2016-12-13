from django.db import models


class Audittrail(models.Model):
    audittrailid = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50)
    msisdn = models.CharField(max_length=12)
    servicename = models.CharField(max_length=50)
    packagename = models.CharField(max_length=50)
    price = models.CharField(max_length=10)
    createddatetime = models.DateTimeField(null=True,
                                           auto_now_add=True)

    def __unicode__(self):
        return self.audittrailid

    class Meta:
        db_table = u'audit_trail'
        ordering = ["audittrailid"]

    class Admin:
        pass
