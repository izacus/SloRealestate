from datetime import datetime, timedelta, time
from django.shortcuts import render

# Create your views here.
from models import EstateAd, AD_TYPES, REGIONS, BUILDING_TYPES


def index_view(request):

    today = datetime.now().date()
    tomorrow = today + timedelta(1)
    today_start = datetime.combine(today, time())
    today_end = datetime.combine(tomorrow, time())

    ads_query = EstateAd.objects

    type = None
    if request.GET.get("t") is not None:
        type = int(request.GET.get("t"))
        ads_query = ads_query.filter(type=type)

    region = None
    if request.GET.get("r") is not None:
        region = int(request.GET.get("r"))
        ads_query = ads_query.filter(region=region)

    building = None
    if request.GET.get("b") is not None:
        building = int(request.GET.get("b"))
        ads_query = ads_query.filter(building_type=building)

    ads_query = ads_query.order_by('price_m2', 'year_built', 'publish_date')
    ads = ads_query.all()#.filter(publish_date__lte=today_end, publish_date__gte=today_start).select_related().all()
    return render(request, "index.html", { "ads": ads,
                                           "ad_types": AD_TYPES,
                                           "regions": sorted(REGIONS, key=lambda x: x[1]),
                                           "building_types": BUILDING_TYPES,
                                           "t": type,
                                           "r": region,
                                           "b": building })