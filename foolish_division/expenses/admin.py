from django.contrib import admin

from foolish_division.expenses.models import Expense, ExpenseGroupMember, ExpenseGroup


@admin.register(ExpenseGroupMember)
class ExpenseGroupMember(admin.ModelAdmin):
    list_display = ('user', 'group', 'type')


@admin.register(ExpenseGroup)
class ExpenseGroup(admin.ModelAdmin):
    list_display = ('uuid', 'name', 'description')


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'name', 'payer', 'submitter', 'group', 'share_type', 'amount')


