from django.contrib import admin
from .models import Item
# Register your models here.
class ItemAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)

admin.site.register(Item, ItemAdmin)
