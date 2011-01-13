from models import Category
from models import AudioMedia
from django.contrib import admin

class AudioMediaAdmin(admin.ModelAdmin):
    list_display = ('name', 'file')

admin.site.register(AudioMedia, AudioMediaAdmin)
admin.site.register(Category)