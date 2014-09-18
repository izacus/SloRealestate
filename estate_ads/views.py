from datetime import datetime, timedelta, time
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render

# Create your views here.
from models import EstateAd, AD_TYPES, REGIONS, BUILDING_TYPES


def index_view(request):
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
    ads = ads_query.all()

    paginator = Paginator(ads, 20)
    page = request.GET.get('p')
    try:
        ads = paginator.page(page)
    except PageNotAnInteger:
        ads = paginator.page(1)
    except EmptyPage:
        ads = paginator.page(paginator.num_pages)

    return render(request, "index.html", { "ads": ads,
                                           "ad_types": AD_TYPES,
                                           "regions": sorted(REGIONS, key=lambda x: x[1]),
                                           "building_types": BUILDING_TYPES,
                                           "t": type,
                                           "r": region,
                                           "b": building })