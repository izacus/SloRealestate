from estate_ads.models import EstateAd, AdPicture
from estate_ads.utils import get_site
from pyquery import PyQuery as pq

def read_ad_details(ad_id):
    ad = EstateAd.objects.get(pk=ad_id)

    # Now download ad
    if ad.link is None: return

    print "-- Detail: " + ad.link
    ad_html = get_site(ad.link)
    tree = pq(ad_html)

    gallery_links = tree.find('#galerija a')
    for link in gallery_links:
        try:
            image = AdPicture(picture_url=link.attrib["href"])
            image.ad = ad
            image.save()
        except KeyError:    # Missing href
            continue

    ad.description = tree.find('.web-opis').text()

    try:
        ad.administrative_unit = tree.find('.more_info').text().split(' | ')[3].lstrip('Upravna enota:').strip()
    except IndexError:
        pass

    if ad.administrative_unit is None:
        ad.administrative_unit = ""

    try:
        ad.county = tree.find('.more_info').text().split(' | ')[4].lstrip(u'Ob\u010dina:').strip()
    except IndexError:
        pass

    if ad.county is None:
        ad.county = ""

    ad.raw_detail_html = ad_html

    ad.save()