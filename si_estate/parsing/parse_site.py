from Queue import Queue
import json
import sys
from lxml import etree
import requests

BASE_URL = "http://www.nepremicnine.net"
TOP_SITE_URL = BASE_URL + "/nepremicnine.html?last=1"

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


parse_queue = Queue()
parse_queue.put(TOP_SITE_URL)

ads = []
while not parse_queue.empty():
    url = parse_queue.get()
    print "Parsing " + url
    site_html = get_site(url)
    tree = etree.fromstring(site_html, etree.HTMLParser())

    raw_ads = tree.xpath('//body/div/div/div[@id="content"]//div[@class="oglas_container"]')

    for raw_ad in raw_ads:
        ad = {}
        ad["id"] = raw_ad.attrib["id"]
        ad["title"] = raw_ad.xpath('div[@class="teksti_container"]/h2/a')[0].text
        ad["link"] = BASE_URL + raw_ad.xpath('div[@class="teksti_container"]/h2/a')[0].attrib["href"]

        ad["picture"] = raw_ad.xpath('div[@class="slika"]/a/img')[0].attrib["src"]

        data = raw_ad.xpath('div[@class="teksti_container"]/div[@class="main-data"]/span')
        ad["raw_data"] = {}
        for data_span in data:
            name = data_span.attrib["class"]
            value = data_span.text
            ad["raw_data"][name] = value

        raw_attributes = raw_ad.xpath('div[@class="teksti_container"]/div[@class="atributi"]/span')
        for raw_attribute in raw_attributes:
            name = raw_attribute.text[:raw_attribute.text.find(':')].lower()
            value = raw_attribute.find("strong").text
            ad["raw_data"][name] = value

        ad["short_desc"] = raw_ad.xpath('div[@class="teksti_container"]/div[@class="kratek"]')[0].text
        ad["seller"] = raw_ad.xpath('div[@class="teksti_container"]/div[@class="povezave"]/div')[0].attrib["title"]

        ad["raw_html"] = etree.tostring(raw_ad)
        ads.append(ad)

    # Grab next page link
    try:
        next_page_link = BASE_URL + tree.xpath('//div[@id="pagination" and @class="fr"]/ul/li/a[@class="next"]')[0].attrib["href"]
        parse_queue.put(next_page_link)
    except:
        pass

print json.dumps(ads).encode("utf-8")
