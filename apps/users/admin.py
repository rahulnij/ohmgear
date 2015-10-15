from django.contrib import admin

# Register your models here.

from .models import User



class UserAdmin(admin.ModelAdmin):
    
    list_display = ('id', 'first_name','email','created_date','get_status')

    def get_status(self, obj):
        if obj.status:
            return 'Active'     
        else:
            return 'InActive' 

    get_status.short_description = 'status'
    get_status.allow_tags = True

    list_per_page = 25
    
admin.site.register(User,UserAdmin)
