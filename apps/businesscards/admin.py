from django.contrib import admin

# Register your models here.

from .models import (
    BusinessCardSkillAvailable,
    BusinessCardAddSkill,
    BusinessCardIdentifier,
    BusinessCard
)
from apps.contacts.models import Contacts, ContactMedia
from django.conf import settings


def active_users(modeladmin, request, queryset):
    queryset.update(status='1')

active_users.short_description = "Activate users"


class BusinessCardAdmin(admin.ModelAdmin):
    list_display = ('serial_number', 'bcard_name', 'bcard_identifier',
                    'bcard_skills', 'user_email', 'active', 'created_date')
    counter = 0

    def active(self, obj):
        bcard_data = BusinessCard.objects.filter(id=obj.id)
        if bcard_data[0].is_active == 1 :
            return "Active"
        else:
            return "Not Active"

    def user_email(self, obj):
        return obj.user_id.email

    def bcard_name(self, obj):
        if obj.name:
            return obj.name
        else:
            return "N/A"

    def bcard_template(self, obj):
        bcard_data = ContactMedia.objects.filter(user_id=obj.user_id)
        if bcard_data:
            return u'<img src="%s%s" style="width: 50px;height:50px;border-radius: 15px;" />' % (settings.DOMAIN_NAME + '/media/', bcard_data[0].img_url)
        else:
            return "N/A"

        bcard_template.short_description = 'BusinessCard Thumbnail'
        bcard_template.allow_tags = True

    def bcard_identifier(self, obj):
        bcard_data = BusinessCardIdentifier.objects.filter(
            businesscard_id=obj.id)
        if bcard_data:
            return bcard_data[0].identifier_id.identifier
        else:
            return "N/A"

    def bcard_skills(self, obj):
        bcard_data = BusinessCardAddSkill.objects.filter(
            businesscard_id=obj.id)
        if bcard_data:
            return bcard_data[0].skill_name
        else:
            return "N/A"

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

admin.site.register(BusinessCardSkillAvailable,
                    BusinessCardSkillAvailableAdmin)


class BusinessCardIdentifierAdmin(admin.ModelAdmin):

    list_display = ('businesscard_name', 'identifier_name_display',
                    'created_date', 'updated_date')
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
