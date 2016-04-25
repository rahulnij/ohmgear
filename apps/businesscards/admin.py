from django.contrib import admin

# Register your models here.

from .models import (
    BusinessCardSkillAvailable, 
    BusinessCardIdentifier,
    BusinessCard
)


class BusinessCardAdmin(admin.ModelAdmin):
    list_display = ('serial_number', 'user_email')
    counter = 0

    def user_email(self, obj):
        return obj.user_id.email

    def image(self, obj):
        return obj


    def serial_number(self, obj):
        self.counter = self.counter + 1
        return self.counter
    
    list_per_page = 100
admin.site.register(BusinessCard, BusinessCardAdmin)


class BusinessCardSkillAvailableAdmin(admin.ModelAdmin):
    
    list_display = ('serial_number', 'skill_name')
    search_fields = ['skill_name']
    counter = 0

    def serial_number(self, obj):
        self.counter = self.counter + 1
        return self.counter
    
    list_per_page = 100
    
admin.site.register(BusinessCardSkillAvailable, BusinessCardSkillAvailableAdmin)


class BusinessCardIdentifierAdmin(admin.ModelAdmin):
    
    list_display = ('businesscard_name', 'identifier_name_display', 'created_date', 'updated_date')
    # search_fields = ['identifier']
    counter = 0

    def serial_number(self, obj):
        self.counter = self.counter + 1
        return self.counter
    
    def identifier_name_display(self, obj):
        return obj.identifier_id.identifier

    identifier_name_display.short_description = 'Identifier Name'
    
    def businesscard_name(self, obj):
        return obj.businesscard_id.name

    businesscard_name.short_description = 'BusinessCard Name'
    
    list_per_page = 100
    
admin.site.register(BusinessCardIdentifier, BusinessCardIdentifierAdmin)
