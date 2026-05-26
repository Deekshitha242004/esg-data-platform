from django.contrib import admin
from .models import Organization, Upload, EmissionRecord

admin.site.register(Organization)
admin.site.register(Upload)
admin.site.register(EmissionRecord)