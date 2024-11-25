from django.contrib import admin
from .models import Employee, Record, ArchiveRecord

admin.site.register(Employee)
admin.site.register(Record)
admin.site.register(ArchiveRecord)