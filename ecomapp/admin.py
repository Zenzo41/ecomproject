from django.contrib import admin
from .models import *
# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'ordered_by', 'order_status', 'payment_completed')
    list_filter = ('order_status', 'payment_completed')
    actions = ['mark_payment_completed', 'mark_payment_pending']

    def mark_payment_completed(self, request, queryset):
        queryset.update(payment_completed=True)
    mark_payment_completed.short_description = "Mark selected orders as Payment Completed"

    def mark_payment_pending(self, request, queryset):
        queryset.update(payment_completed=False)
    mark_payment_pending.short_description = "Mark selected orders as Payment Pending"

admin.site.register(Order, OrderAdmin)

admin.site.register([Customer,Category,Cart,CartProduct,Admin] )

class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'marked_price', 'selling_price', 'expiry', 'view_count')
    list_filter = ('category', 'expiry')
    search_fields = ('title', 'category__name')  # Assuming you have a name field in the Category model

admin.site.register(Product, ProductAdmin)