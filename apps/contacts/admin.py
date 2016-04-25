from django.contrib import admin

# Register your models here.

from .models import (
    User,
    ContactMedia
)


class ContactMediaAdmin(admin.ModelAdmin):
    list_display = ('serial_number', 'admin_thumbnail','created_date','updated_date')
    counter = 0

    def serial_number(self, obj):
        self.counter = self.counter + 1
        return self.counter

    list_per_page = 100

admin.site.register(ContactMedia,ContactMediaAdmin)
