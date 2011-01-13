from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=200,unique=True)

    def __unicode__(self):
        return self.name
    class Meta:
                   verbose_name_plural = "Categories"
    
class AudioMedia(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to="audio")
    categories = models.ManyToManyField(Category, blank=True)

    class Meta:
               verbose_name_plural = "Audio Media"