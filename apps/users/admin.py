from django.contrib import admin

# Register your models here.

from .models import User

def inactive_users(modeladmin, request, queryset):
    queryset.update(status='0')
inactive_users.short_description = "InActivate users"

def active_users(modeladmin, request, queryset):
    queryset.update(status='1')
active_users.short_description = "Activate users"


class UserAdmin(admin.ModelAdmin):
    # code to display selected fields from the database
    list_display = ('serial_number', 'first_name','email','created_date','get_status')
    # search field criterion
    search_fields = ['email']
    # custom drop down option in the admin 
    actions = [inactive_users,active_users]
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
