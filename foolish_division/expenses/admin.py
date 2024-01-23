from django.contrib import admin

from foolish_division.expenses.models import ExpenseCategory, ExpenseCategoryOwner, VendorCategory, Expense, Vendor


@admin.register(ExpenseCategoryOwner)
class ExpenseCategoryOwnerAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'role')


@admin.register(ExpenseCategory)
class ExpenseCategoryAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'name')


@admin.register(VendorCategory)
class VendorCategoryAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'name')


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'name', 'category')


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'name', 'payer', 'submitter', 'vendor', 'category', 'share_type', 'amount')


