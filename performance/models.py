from django.db import models

# Create your models here.
class Testdata(models.Model):
    item = models.IntegerField()
    costprice = models.IntegerField()
    sellprice = models.IntegerField()


