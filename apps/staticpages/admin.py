from django.contrib import admin
from .models import StaticPages
# Register your models here.


class AboutAdmin(admin.ModelAdmin):

    list_display = ('headline', 'content', 'status')
    #search_fields = ['skill_name']
    counter = 0

    def serial_number(self, obj):
        self.counter = self.counter + 1
        return self.counter

    list_per_page = 100

admin.site.register(StaticPages, AboutAdmin)
