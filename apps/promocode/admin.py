from django.contrib import admin

from .models import Promocode


class PromocodeAdmin(admin.ModelAdmin):

    list_display = (
        'promocode_title',
        'promocode_worth',
        'created_date',
        'expiry_date',
        'get_user_type',
        'no_of_use'
    )

    def get_user_type(self, obj):
        if (obj.user_type == 1):
            return 'Admin'
        if (obj.user_type == 2):
            return 'Individual'
        else:
            return 'Corporate'

    list_per_page = 25

admin.site.register(Promocode, PromocodeAdmin)
