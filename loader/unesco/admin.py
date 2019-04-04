from django.contrib import admin

# Register your models here.
from unesco.models import Category, Region, Iso, States, Site

admin.site.register(Category)
admin.site.register(Region)
admin.site.register(Iso)
admin.site.register(States)
admin.site.register(Site)
