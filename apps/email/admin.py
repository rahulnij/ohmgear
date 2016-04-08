from django.contrib import admin
from models import EmailTemplate
# Register your models here.


class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ('subject', 'content', 'slug', 'status', 'from_email')
    list_filter = ('status',)

    def has_delete_permission(self, request, obj=None):  # note the obj=None
        return False

admin.site.register(EmailTemplate, EmailTemplateAdmin)
