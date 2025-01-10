from django.contrib import admin

from foolish_division.log.models import LogEntry


# Register your models here.
@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('profile', 'group')