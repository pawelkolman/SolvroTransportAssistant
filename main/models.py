from django.db import models
from users.models import CustomUser

# Create your models here.

class Favourite(models.Model):
    source = models.CharField(max_length=255)
    target = models.CharField(max_length=255)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.source + ' - ' + self.target