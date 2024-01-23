from django.contrib import admin


class ExpenseCategoryOwnerAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'role')


class ExpenseCategoryAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'name')


class VendorCategoryAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'name')


class VendorAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'name', 'category')


class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'name', 'payer', 'submitter', 'vendor', 'category', 'share_type', 'amount')


admin.register(ExpenseCategoryOwnerAdmin)
admin.register(ExpenseCategoryAdmin)
admin.register(VendorCategoryAdmin)
admin.register(VendorAdmin)
admin.register(ExpenseAdmin)
