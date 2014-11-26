from bs4 import BeautifulSoup
import urllib.request
import requests


scanned_urls = []

domain = "http://hackbulgaria.com/"

def get_domain(url):
    parsed_uri = urlparse(url)
    base_url = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    print(base_url)
    return base_url


def is_outgoing(url):
    if domain in url:
        return False
    return True


def prepare_link(url, href):
    return urllib.parse.urljoin(url, href)



def scan_page(url):
    if url in scanned_urls:
        return
    print (url)
    scanned_urls.append(url)
    r = requests.get(url)
    html = r.text
    soup = BeautifulSoup(html)
    for link in soup.find_all('a'):
        new_link = prepare_link(url, link.get('href'))
        if not is_outgoing(new_link):
            scan_page(new_link)


def scan_website():
    url = "http://" + domain
    scan_page(url)


def main():
    scan_page("http://hackbulgaria.com/")

if __name__ == '__main__':
    main()
