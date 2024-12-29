from django.contrib import admin

from foolish_division.expenses.models import ExpenseCategory, ExpenseCategoryOwner, VendorCategory, Expense, Vendor


@admin.register(ExpenseCategoryOwner)
class ExpenseGroupMember(admin.ModelAdmin):
    list_display = ('user', 'group', 'type')


@admin.register(ExpenseCategory)
class ExpenseGroup(admin.ModelAdmin):
    list_display = ('uuid', 'name', 'description')


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'name', 'payer', 'submitter', 'group', 'share_type', 'amount')


