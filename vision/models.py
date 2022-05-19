from django.db import models

# Create your models here.
class Visionuser(models.Model):
    user = models.CharField(max_length=255)
    metadata=models.JSONField()
    


class Imagesessn(models.Model):

    def user_directory_path(instance, filename):    
        return 'MLWB/{0}/images/{1}'.format(instance.user, filename)
        
    user = models.CharField(max_length=255)
    myfiles = models.FileField(upload_to=user_directory_path)
    # metadata = models.JSONField()


    def __str__(self):
        return self.user