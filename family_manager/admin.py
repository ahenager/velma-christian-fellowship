from models import Family, FamilyMember
from django.contrib import admin

class FamilyMemberInline(admin.TabularInline):
    model = FamilyMember

class FamilyAdmin(admin.ModelAdmin):
    inlines = [
        FamilyMemberInline,
    ]

admin.site.register(Family,FamilyAdmin)