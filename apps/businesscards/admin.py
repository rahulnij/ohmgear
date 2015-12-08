from django.contrib import admin

# Register your models here.

from .models import BusinessCardSkillAvailable

class BusinessCardSkillAvailableAdmin(admin.ModelAdmin):
    
    list_display = ('serial_number', 'skill_name')
    counter = 0

    def serial_number(self, obj):
        self.counter = self.counter + 1
        return self.counter
    
    list_per_page = 25
    
admin.site.register(BusinessCardSkillAvailable,BusinessCardSkillAvailableAdmin)
