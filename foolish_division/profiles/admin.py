from django.contrib import admin

from foolish_division.profiles.models import ExpenseProfile


# Register your models here.
@admin.register(ExpenseProfile)
class ExpenseProfileAdmin(admin.ModelAdmin):
    list_display = ('owner', 'name', 'owner')