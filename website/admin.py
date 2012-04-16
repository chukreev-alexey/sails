# -*- coding: utf-8 -*-
from django.contrib import admin

from website.models import (Settings, Country, Oper, Currency, Office, Staff,
                            Order, Payment, PaymentType)
from autocomplete.views import autocomplete, AutocompleteSettings

class CountryAutocomplete(AutocompleteSettings):
    search_fields = ('^name', )
autocomplete.register(Order.country, CountryAutocomplete)

class OperAutocomplete(AutocompleteSettings):
    search_fields = ('^name', )
autocomplete.register(Order.oper, OperAutocomplete)

class StaffAutocomplete(AutocompleteSettings):
    search_fields = ('^name', )
autocomplete.register(Order.staff, StaffAutocomplete)

class PaymentStaffAutocomplete(AutocompleteSettings):
    search_fields = ('^name', )
autocomplete.register(Payment.staff, PaymentStaffAutocomplete)

admin.site.register(Settings)
admin.site.register(Country)
admin.site.register(Currency)
admin.site.register(Oper)
admin.site.register(Office)
admin.site.register(PaymentType)

class StaffAdmin(admin.ModelAdmin):
    list_display = ('name', 'office', 'get_group_list')
    list_filter = ('office', 'user__groups')
admin.site.register(Staff, StaffAdmin)

class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 1

class OrderAdmin(admin.ModelAdmin):
    inlines = [PaymentInline, ]
admin.site.register(Order, OrderAdmin)