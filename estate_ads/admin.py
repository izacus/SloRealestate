from django.contrib import admin

from estate_ads.models import EstateAd, AdPicture


class EstateAdAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'region', 'type', 'size_m2', 'price', 'publish_date')
    list_filter = ('region', 'type', 'building_type')


class AdPictureAdmin(admin.ModelAdmin):
    list_display = ('id', 'picture_url')

admin.site.register(EstateAd, EstateAdAdmin)
admin.site.register(AdPicture, AdPictureAdmin)