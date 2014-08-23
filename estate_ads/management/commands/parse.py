# -*- coding: utf-8 -*-

from Queue import Queue
import json
import sys
from django.core.management import BaseCommand
from django.db import IntegrityError
from django.utils import timezone
from lxml import etree
from estate_ads.models import EstateAd, AdPicture
from estate_ads.models import REGIONS
from estate_ads.models import AD_TYPES
from estate_ads.models import BUILDING_TYPES
import requests
import locale
import requests_cache

BASE_URL = "http://www.nepremicnine.net"
TOP_SITE_URL = BASE_URL + "/nepremicnine.html?last=1"

# For number parsing
locale.setlocale(locale.LC_NUMERIC, "sl_SI")

requests_cache.install_cache('parse_cache')
requests_session = requests.Session()

# Proxy detection is broken on OS X 10.9 in python currently causing the process to hang
# Hence we disable all proxy detection code in Requests and urllib2-related calls here
if sys.platform == "darwin":
    requests_session.trust_env = False

def get_site(url):
    if sys.platform == "darwin":
        response = requests_session.get(url, proxies={})
    else:
        response = requests_session.get(url)
    response.encoding = response.apparent_encoding
    return response.text


class Command(BaseCommand):
    """
    Parses last 24 hours of ads on the site
    """

    def parse_float(self, number_string):
        return locale.atof(number_string.strip().replace('.', ''))

    def parse_type(self, raw_data):
        ad_type = None
        building_type = None

        if "posr" in raw_data:
            ad_type_string = raw_data["posr"][:raw_data["posr"].find(":")]
            # TODO: Make this not ugly / more elegant
            if ad_type_string == "Prodaja":
                ad_type = AD_TYPES[0][0]
            elif ad_type_string == "Nakup":
                ad_type = AD_TYPES[1][0]
            elif ad_type_string == "Oddaja":
                ad_type = AD_TYPES[2][0]
            elif ad_type_string == "Najem":
                ad_type = AD_TYPES[3][0]

            if ad_type is None:
                print "Unknown ad type: " + ad_type_string

            building_type_string = raw_data["posr"][raw_data["posr"].find(":") + 1:].strip()
            if building_type_string == u"Stanovanje":
                building_type = BUILDING_TYPES[0][0]
            elif building_type_string == u"Hiša":
                building_type = BUILDING_TYPES[1][0]
            elif building_type_string == u"Posest":
                building_type = BUILDING_TYPES[2][0]
            elif building_type_string == u"Poslovni prostor":
                building_type = BUILDING_TYPES[3][0]
            elif building_type_string == u"Garaža":
                building_type = BUILDING_TYPES[4][0]
            elif building_type_string == u"Počitniški objekt" or building_type_string == u"Vikend":
                building_type = BUILDING_TYPES[5][0]

            if building_type is None:
                print "Unknown building type " + building_type_string

        return ad_type, building_type

    def parse_size(self, raw_data):
        if "velikost" in raw_data and raw_data["velikost"] is not None:
            try:
                return self.parse_float(raw_data["velikost"][:raw_data["velikost"].find("m2")]) # Ugly hack, can we parse these numbers better?
            except ValueError:
                print "Wrong size value: " + raw_data["velikost"]

        return None

    def parse_price(self, raw_data, size):
        if not "cena" in raw_data or raw_data["cena"] is None:
            return None, None

        # Check for "price/m2"
        price = raw_data["cena"]
        if u"\u20ac/m2" in price:
            try:
                price_m2_num = self.parse_float(price[:price.find(u"\u20ac/m2")])
            except ValueError:
                return (None, None)

            price_num = None
            if size is not None:
                price_num = price_m2_num * size

            return price_num, price_m2_num

        else:
            price_num = self.parse_float(price[:price.find(u"\u20ac")])
            price_m2_num = None
            if size is not None:
                price_m2_num = price_num / size

            return price_num, price_m2_num

        return None, None


    def parse_year(self, raw_data):
        if not "leto" in raw_data or raw_data["leto"] is None:
            return None

        return int(self.parse_float(raw_data["leto"]))

    def handle(self, *args, **options):

        parse_queue = Queue()

        for region_num, region_name in REGIONS:
            print " == " + region_name + " == "
            parse_queue.put(TOP_SITE_URL + "&r=" + str(region_num))

            while not parse_queue.empty():
                url = parse_queue.get()
                print "Parsing " + url
                site_html = get_site(url)
                tree = etree.fromstring(site_html, etree.HTMLParser())

                raw_ads = tree.xpath('//body/div/div/div[@id="content"]//div[@class="oglas_container"]')
                for raw_ad in raw_ads:
                    ad_id = raw_ad.attrib["id"]
                    if EstateAd.objects.filter(ad_id=ad_id).exists():
                        continue

                    ad = EstateAd()
                    ad.region = region_num
                    ad.publish_date = timezone.now()    # We're parsing last 24 hours so set publish date to now
                    ad.ad_id = ad_id
                    ad.title = raw_ad.xpath('div[@class="teksti_container"]/h2/a')[0].text
                    ad.link = BASE_URL + raw_ad.xpath('div[@class="teksti_container"]/h2/a')[0].attrib["href"]

                    thumbnail_url = raw_ad.xpath('div[@class="slika"]/a/img')[0].attrib["src"]
                    if thumbnail_url and not thumbnail_url.startswith('/images/n-'): # N-something are placeholders
                        ad.thumbnail = AdPicture(picture_url=thumbnail_url)
                        ad.thumbnail.save()

                    data = raw_ad.xpath('div[@class="teksti_container"]/div[@class="main-data"]/span')

                    raw_data = {}
                    for data_span in data:
                        name = data_span.attrib["class"]
                        value = data_span.text
                        raw_data[name] = value

                    raw_attributes = raw_ad.xpath('div[@class="teksti_container"]/div[@class="atributi"]/span')
                    for raw_attribute in raw_attributes:
                        name = raw_attribute.text[:raw_attribute.text.find(':')].lower()
                        value = raw_attribute.find("strong").text
                        raw_data[name] = value

                    ad.raw_data = json.dumps(raw_data)
                    ad.type, ad.building_type = self.parse_type(raw_data)
                    ad.size_m2 = self.parse_size(raw_data)
                    ad.price, ad.price_m2 = self.parse_price(raw_data, ad.size_m2)

                    ad.year_built = self.parse_year(raw_data)
                    ad.floor = raw_data.get("nadstropje", "")

                    ad.short_description = raw_ad.xpath('div[@class="teksti_container"]/div[@class="kratek"]')[0].text
                    ad.author_name = raw_ad.xpath('div[@class="teksti_container"]/div[@class="povezave"]/div')[0].attrib["title"]
                    ad.raw_html = etree.tostring(raw_ad)

                    try:
                        ad.save()
                    except IntegrityError as e:
                        print e
                        print "Ad with id %s already exists in database!" % (ad.ad_id, )

                # Grab next page link
                try:
                    next_page_link = BASE_URL + tree.xpath('//div[@id="pagination" and @class="fr"]/ul/li/a[@class="next"]')[0].attrib["href"]
                    parse_queue.put(next_page_link)
                except:
                    pass