from django.contrib import admin
import csv
from django.utils.encoding import smart_str
from django.http import HttpResponse
from simple_history.admin import SimpleHistoryAdmin
# Register your models here.

from .models import User

def inactive_users(modeladmin, request, queryset):
    queryset.update(status='0')
inactive_users.short_description = "InActivate users"

def active_users(modeladmin, request, queryset):
    queryset.update(status='1')
active_users.short_description = "Activate users"

# code to export custom data fields to csv
def export_csv(modeladmin, request, queryset):
    
    response = HttpResponse(content_type ='text/csv')
    response['Content-Disposition'] = 'attachment; filename=mymodel.csv'
    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)
    writer.writerow([
        smart_str(u"First Name"),
        smart_str(u"Last Name"),
        smart_str(u"Email"),
        smart_str(u"Created Date"),
    ])
    for obj in queryset:
        writer.writerow([
            smart_str(obj.first_name),
            smart_str(obj.last_name),
            smart_str(obj.email),
            smart_str(obj.created_date)      
        ])
    return response
export_csv.short_description = u"Export selected objects to CSV"

class UserAdmin(admin.ModelAdmin):
    # code to display selected fields from the database
    list_display = ('serial_number', 'first_name','email','created_date','get_status')
    # search field criterion
    search_fields = ['email']
    # custom drop down option in the admin 
    actions = [inactive_users,active_users,export_csv,]
    counter = 0
    
   # non-editable fields in the admin
   # def get_readonly_fields(self, request, obj=None):
   #	if obj: # editing an existing object
   #     	return self.readonly_fields + ('password','user_type')
   #    	return self.readonly_fields  
    
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
    
admin.site.register(User,UserAdmin)