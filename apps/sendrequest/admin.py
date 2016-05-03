from django.contrib import admin

# Register your models here.

from .models import SendRequest



class SendRequestAdmin(admin.ModelAdmin):

    list_display = ('request_type', 'sender_user_id_display', 'receiver_user_id_display', 'request_status', 'sender_bcard_name',
                    'created_date', 'updated_date')
    # search_fields = ['identifier']
    counter = 0

    def sender_user_id_display(self, obj):
        return obj.sender_user_id.email
    sender_user_id_display.short_description = 'Sender Email'

    def receiver_user_id_display(self, obj):

        if obj.receiver_user_id:
            return obj.receiver_user_id.email
        else:
            return "Not Yet Registered"
    receiver_user_id_display.short_description = 'Receiver Email'

    def request_status(self, obj):
        request_status.short_description = 'Request Status'

    def sender_bcard_name(self, obj):

        if obj.sender_business_card_id.name:
            return obj.sender_business_card_id.name
        else:
            return "N/A"

    list_per_page = 100

admin.site.register(SendRequest, SendRequestAdmin)
