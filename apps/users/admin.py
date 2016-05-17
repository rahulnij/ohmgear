
# Django models
from django.utils.encoding import smart_str
from django.http import HttpResponse
from djcelery.models import (TaskState, WorkerState,
                             PeriodicTask, IntervalSchedule, CrontabSchedule)
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import Token
from django.contrib import admin
admin.autodiscover()

<<<<<<< HEAD
# Third Party models
=======
#Third Party models
>>>>>>> unregistered models
import csv

from .models import (
    User,
    UserType,
    Profile,
    BusinessType,
    IncomeGroup,
    UserEmail,
    SocialLogin,
    SocialType,
    ConnectedAccount
)


def inactive_users(modeladmin, request, queryset):
    queryset.update(status='0')

inactive_users.short_description = "InActivate users"


def active_users(modeladmin, request, queryset):
    queryset.update(status='1')

active_users.short_description = "Activate users"


# code to export custom data fields to csv
def export_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=mymodel.csv'
    writer = csv.writer(response, csv.excel)
    # BOM (optional...Excel needs it to open UTF-8 file properly)
    response.write(u'\ufeff'.encode('utf8'))
    writer.writerow([
        # smart_str(u"First Name"),
        # smart_str(u"Last Name"),
        smart_str(u"Email"),
        smart_str(u"Created Date"),
    ])
    for obj in queryset:
        writer.writerow([
            # smart_str(obj.first_name),
            # smart_str(obj.last_name),
            smart_str(obj.email),
            smart_str(obj.created_date)
        ])
    return response
export_csv.short_description = u"Export selected objects to CSV"


class UserAdmin(admin.ModelAdmin):
    # code to display selected fields from the database
    list_display = ('serial_number', 'email', 'created_date',
                    'get_status', 'user_type')
    # search field criterion
    search_fields = ['email']
    # custom drop down option in the admin
    actions = [inactive_users, active_users, export_csv, ]
    # need this for bootstrap
    counter = 0

    # non-editable fields in the admin
    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ('password', 'user_type')
        return self.readonly_fields

    def get_status(self, obj):
        if obj.status:
            return 'Active'
        else:
            return 'InActive'

    def serial_number(self, obj):
        self.counter = self.counter + 1
        return self.counter

    get_status.short_description = 'status'
    get_status.allow_tags = True
    list_per_page = 100


class UserTypeAdmin(admin.ModelAdmin):
    model = UserType


class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    raw_id_fields = ('user',)
    search_fields = ('user__email',)
    # code to display selected fields from the database
    list_display = ('first_name', 'last_name', 'user_id_display',
                    'mobile_number', 'admin_thumbnail')

    def user_id_display(self, obj):
        return obj.user.email
    user_id_display.short_description = 'User Email'


# class UserProfileAdmin(admin.TabularInline):
#     model = Profile

class BusinessTypeAdmin(admin.ModelAdmin):
    pass


class SocialLoginAdmin(admin.ModelAdmin):
    pass


class UserEmailAdmin(admin.ModelAdmin):
    list_display = ('user_original_email_display','additional_email','is_Verified',
                    'created_date', 'updated_date')

    def user_original_email_display(self, obj):
        return obj.user_id.email
    user_original_email_display.short_description = 'OriginalEmail'

    def additional_email(self, obj):
        return obj.email
    additional_email.short_description = 'Additional Email'

    def is_Verified(self, obj):

        if obj.isVerified == 1:
            return "Activated"
        else:
            return "Not Activated"
    is_Verified.short_description = 'Status'


class SocialTypeAdmin(admin.ModelAdmin):
    pass


class IncomeGroupAdmin(admin.ModelAdmin):
    pass


class ConnectedAccountAdmin(admin.ModelAdmin):
    pass

# Unregister Default Available Apps
admin.site.unregister(Group)
admin.site.unregister(PeriodicTask)
admin.site.unregister(CrontabSchedule)
admin.site.unregister(TaskState)
admin.site.unregister(WorkerState)
admin.site.unregister(IntervalSchedule)
admin.site.unregister(Token)

admin.site.register(User, UserAdmin)
admin.site.register(UserType, UserTypeAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(BusinessType, BusinessTypeAdmin)
admin.site.register(SocialLogin, SocialLoginAdmin)
admin.site.register(UserEmail, UserEmailAdmin)
admin.site.register(SocialType, SocialLoginAdmin)
admin.site.register(IncomeGroup, IncomeGroupAdmin)
admin.site.register(ConnectedAccount, ConnectedAccountAdmin)
