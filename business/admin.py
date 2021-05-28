from django.contrib import admin

from customers.models import Customer
from expenses.models import Expense
from inventory.models import Stock

from .models import BusinessType, BusinessAccount


@admin.register(BusinessType)
class BusinessTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')


class CustomerInline(admin.TabularInline):
    model = Customer
    extra = 1


class ExpenseInline(admin.TabularInline):
    model = Expense
    extra = 1


class StockInline(admin.TabularInline):
    model = Stock
    extra = 1


@admin.register(BusinessAccount)
class BusinessAccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'business_type', 'created_at', 'updated_at')
    list_filter = ('business_type', )
    search_fields = ('business_name', )
    inlines = [CustomerInline, ExpenseInline, StockInline]
