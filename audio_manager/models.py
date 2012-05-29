from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=200,unique=True)

    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Categories"
        app_label = 'audio_manager'
    
class AudioMedia(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to="audio", blank=True)
    categories = models.ManyToManyField(Category, blank=True)
    date = models.DateField(verbose_name="Content Date", blank=True, null=True)

    class Meta:
        verbose_name_plural = "Audio Media"
        app_label = 'audio_manager'