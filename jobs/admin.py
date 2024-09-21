from django.contrib import admin
from .models import Job
from import_export.admin import ImportExportModelAdmin


# Register your models here.
admin.site.register(Job, ImportExportModelAdmin)