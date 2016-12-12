from django.db import models

class Packages(models.Model):
    id = models.IntegerField(primary_key=True)
    provisioning_packages_id = models.IntegerField()
    package_name = models.CharField(max_length=50)
    created_at = models.DateField(null=True, blank=True)
    modified_at = models.DateField(null=True, blank=True)
    package_cost = models.IntegerField()
    #category_id = models.IntegerField()
    #active = models.BigIntegerField(null=True, blank=True)
    refill_id = models.CharField(max_length=20)
    trans_amount = models.CharField(max_length=20)
    gui = models.IntegerField(max_length=2)
    class Meta:
        db_table = u'new_packages'
