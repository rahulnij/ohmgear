

from django.contrib import admin
from .models import Feedbacks, FeedbackCategory, FeedbackCategorySubject, ContactUs


class FeedbacksAdmin(admin.ModelAdmin):

    list_display = ('user_name_display', 'bug_type',
                    'created_date', 'updated_date')
    counter = 0

    def serial_number(self, obj):
        self.counter = self.counter + 1
        return self.counter

    def user_name_display(self, obj):
        return obj.user_id.email
    user_name_display.short_description = 'User Name'

    list_per_page = 100

admin.site.register(Feedbacks, FeedbacksAdmin)


class FeedbackCategorySubjectAdmin(admin.ModelAdmin):
    model = FeedbackCategorySubject


admin.site.register(FeedbackCategorySubject, FeedbackCategorySubjectAdmin)


class FeedbackCategoryInline(admin.ModelAdmin):
    model = FeedbackCategory
    # inlines = [FeedbackCategorySubjectAdmin]


admin.site.register(FeedbackCategory, FeedbackCategoryInline)


class FeedbackCategoryAdmin(admin.ModelAdmin):
    pass


class ContactUsAdmin(admin.ModelAdmin):
    model = ContactUs
    # inlines = [FeedbackCategorySubjectAdmin]


admin.site.register(ContactUs, ContactUsAdmin)
