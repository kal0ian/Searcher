from bs4 import BeautifulSoup
import urllib.request
import requests
from urllib.parse import urlparse

scanned_urls = []


def get_domain(url):
    parsed_uri = urlparse(url)
    base_url = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    return base_url


def is_outgoing(domain, url):
    if domain in url:
        return False
    return True


def prepare_link(url, href):
    return urllib.parse.urljoin(url, href)


def scan_page(domain, url):
    if url in scanned_urls:
        return
    print (url)
    scanned_urls.append(url)
    r = requests.get(url)
    html = r.text
    soup = BeautifulSoup(html)
    for link in soup.find_all('a'):
        new_link = prepare_link(url, link.get('href'))
        if not is_outgoing(domain, new_link):
            scan_page(domain, new_link)


def scan_website(domain):
    url = "http://" + domain
    scan_page(url)


def search():
    url = "http://hackbulgaria.com/"
    domain = get_domain(url)
    scan_page(domain, url)
