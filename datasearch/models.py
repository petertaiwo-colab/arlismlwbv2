from django.db import models

class Dtsrchdb(models.Model):
    dtsite=models.CharField(max_length=10)
    searchkey=models.CharField(max_length=100)
    sess_id=models.CharField(max_length=500)
    metadata=models.JSONField(null=True)
    dtssmrypg=models.CharField(max_length=100)
    email=models.EmailField()
    domain=models.CharField(max_length=20)
    passcode=models.CharField(max_length=6)
    passres=models.CharField(max_length=1)
    errormsg=models.CharField(max_length=100, default="")
    usernm=models.CharField(max_length=10)

class Userreg(models.Model):
    sess_id=models.CharField(max_length=400)
    email=models.EmailField()
    domain=models.CharField(max_length=20)
    passcode=models.CharField(max_length=6)
    passres=models.CharField(max_length=1)
    errormsg=models.CharField(max_length=100, default="")
    username=models.CharField(max_length=10)

class Usersessn(models.Model):
    user=models.CharField(max_length=10)
    userbucket=models.CharField(max_length=30)
    usertemplates=models.CharField(max_length=30)
    dtsite=models.CharField(max_length=10)
    searchkey=models.CharField(max_length=100)
    sess_id=models.CharField(max_length=500)
    sritems=models.JSONField(default=[])
    metadata=models.JSONField(default={"dtsloc": 0, "currvw": 0, "currpg": 0, "numitems": 0, "labels": {}})
    currimage=models.JSONField(default={})
    dtssmrypg=models.CharField(max_length=100)
    sgmk=models.JSONField(default={"instname": 0, "vmtype": 0, "setuptime": 0, "insturl": 0, "urltime": 0, })
    lclnb=models.JSONField(default={"instname": 0, "vmtype": 0, "setuptime": 0, "insturl": 0, "urltime": 0, })
# class Dtsdim1(models.Model):

class Admintrack(models.Model):
    jport=models.JSONField(default=[])


    
