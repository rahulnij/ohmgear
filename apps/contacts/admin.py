from django.contrib import admin

# Register your models here.

from .models import (
    User,
    ContactMedia
)

# contact info of user could show more fields as per requirement


class ContactMediaAdmin(admin.ModelAdmin):
    list_display = ('serial_number', 'user_name', 'home_phone', 'country_code',
                    'country_flag', 'home_email', 'work_email', 'company_name', 'created_date', 'updated_date')
    counter = 0

    def user_name(self, obj):
        return obj.contact_id.bcard_json_data['side_first']['basic_info'][1]['placeHolder'] + " " + obj.contact_id.bcard_json_data['side_first']['basic_info'][2]['placeHolder']

    def company_name(self, obj):
        return obj.contact_id.bcard_json_data['side_first']['basic_info'][5]['placeHolder']

    def home_phone(self, obj):
        return obj.contact_id.bcard_json_data['side_first']['contact_info']['phone'][0]['data']

    def country_code(self, obj):
        return obj.contact_id.bcard_json_data['side_first']['contact_info']['phone'][0]['countryCode']

    def country_flag(self, obj):
        return obj.contact_id.bcard_json_data['side_first']['contact_info']['phone'][0]['countryFlag']

    def home_email(self, obj):
        return obj.contact_id.bcard_json_data['side_first']['contact_info']['email'][0]['data']

    def work_email(self, obj):
        return obj.contact_id.bcard_json_data['side_first']['contact_info']['email'][0]['data']

    def serial_number(self, obj):
        self.counter = self.counter + 1
        return self.counter

    list_per_page = 100

admin.site.register(ContactMedia, ContactMediaAdmin)
