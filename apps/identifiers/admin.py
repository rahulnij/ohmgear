from django.contrib import admin
from .models import Identifier


class IdentifierAdmin(admin.ModelAdmin):

    list_display = ('identifier', 'user_id_display',
                    'created_date', 'updated_date')
    search_fields = ['identifier']
    counter = 0

    def serial_number(self, obj):
        self.counter = self.counter + 1
        return self.counter

    def user_id_display(self, obj):
        return obj.user.email
    user_id_display.short_description = 'User Email'

    list_per_page = 100

admin.site.register(Identifier, IdentifierAdmin)
