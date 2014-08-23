from django.contrib import admin
from models import EstateAd

class EstateAdAdmin(admin.ModelAdmin):
	list_display = ('title', 'id', 'region', 'type', 'size_m2', 'price')
	list_filter = ('region', 'type', 'building_type')

admin.site.register(EstateAd, EstateAdAdmin)