from django.db import models
from django.contrib.auth.models import User

# Create your models here.

    
class Music(models.Model):
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200, default="Artista desconhecido")
    soundcloud_url = models.URLField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Album(models.Model):
    name = models.CharField(max_length=200)
    musics = models.ManyToManyField(Music)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
