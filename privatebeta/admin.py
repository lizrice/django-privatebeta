from django.contrib import admin
from privatebeta.models import InviteRequest

class InviteRequestAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    list_display = ('email', 'created', 'invited', 'accepted')
    list_filter = ('created', 'invited')
    readonly_fields = ('accepted',)

admin.site.register(InviteRequest, InviteRequestAdmin)
