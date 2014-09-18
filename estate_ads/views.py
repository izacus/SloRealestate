from datetime import datetime, timedelta, time
from django.shortcuts import render

# Create your views here.
from models import EstateAd


def index_view(request):

    today = datetime.now().date()
    tomorrow = today + timedelta(1)
    today_start = datetime.combine(today, time())
    today_end = datetime.combine(tomorrow, time())

    ads = EstateAd.objects.filter(publish_date__lte=today_end, publish_date__gte=today_start).select_related().all()
    return render(request, "index.html", { "ads": ads })