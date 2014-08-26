import sys
import requests
import requests_cache
import si_estate.settings

if si_estate.settings.DEBUG:        # Don't enable in production
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