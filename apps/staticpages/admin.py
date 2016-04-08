from django.contrib import admin
from .models import StaticPages


class AboutAdmin(admin.ModelAdmin):

    list_display = ('headline', 'content', 'status')
    counter = 0

    def serial_number(self, obj):
        self.counter = self.counter + 1
        return self.counter

    list_per_page = 100

admin.site.register(StaticPages, AboutAdmin)
