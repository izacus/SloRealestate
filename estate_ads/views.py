import datetime
import operator

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.db.models import Q

# Create your views here.
from estate_ads.models import AD_TYPES, REGIONS, BUILDING_TYPES, EstateAd


def index_view(request):
    date = datetime.date.today()
    start_week = date - datetime.timedelta(date.weekday())
    end_week = start_week + datetime.timedelta(7)

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

    if request.GET.get("mxa") is not None:
        ads_query = ads_query.filter(size_m2__lte=int(request.GET.get("mxa")))

    if request.GET.get("mna") is not None:
        ads_query = ads_query.filter(size_m2__gte=int(request.GET.get("mna")))

    search_locations = request.GET.get("locations", None)
    if search_locations:
        locations = [loc.strip() for loc in search_locations.split(",")]
        query = [Q(title__icontains=loc) | Q(description__icontains=loc)
                 for loc in locations]
        ads_query = ads_query.filter(reduce(operator.or_, query))

    ads_query = ads_query.order_by('-publish_date', 'size_m2', 'year_built')
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
                                           "b": building,
                                           "locations": search_locations
                                           })
