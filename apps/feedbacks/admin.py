from django.contrib import admin

# Register your models here.

from .models import Feedbacks


class FeedbacksAdmin(admin.ModelAdmin):

    list_display = ('user_name_display', 'bug_type',
                    'created_date', 'updated_date')
    #search_fields = ['identifier']
    counter = 0

    def serial_number(self, obj):
        self.counter = self.counter + 1
        return self.counter

    def user_name_display(self, obj):
        return obj.user_id.email
    user_name_display.short_description = 'User Name'

    list_per_page = 100

admin.site.register(Feedbacks, FeedbacksAdmin)
