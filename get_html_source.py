from bs4 import BeautifulSoup
import urllib.request
import requests
from urllib.parse import urlparse
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import relationship
#from orm import Website

Base = declarative_base()


class Website(Base):
    __tablename__ = "website"
    id = Column(Integer, primary_key=True)
    url = Column(String)
    title = Column(String)
    domain = Column(String)
    pages_count = Column(Integer)
    HTML_version = Column(Float)


class Page(Base):
    __tablename__ = "pages"
    id = Column(Integer, primary_key=True)
    website_url = Column(Integer, ForeignKey("website.url"))
    website = relationship(Website, backref="pages")
    url = Column(String)
    title = Column(String)
    desc = Column(String)
    SSL = Column(Integer)
    multi_lang = Column(Integer)
    rating = Column(Integer)


scanned_urls = []


engine = create_engine("sqlite:///orm.db")
Base.metadata.create_all(engine)

session = Session(bind=engine)


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


def scan_page(domain, url, website):
    if url in scanned_urls:
        return
    print (url)
    #print("Adding new site to the database via the session object")

    scanned_urls.append(url)
    r = requests.get(url)
    html = r.text
    soup = BeautifulSoup(html)
    temp = url

    if(soup.title and soup.description):
        website.pages.append(
            Page(url=temp, title=soup.title.string, desc=soup.description.string))
    elif soup.title:
        website.pages.append(Page(url=temp, title=soup.title.string))
    website.pages.append(Page(url=temp))

    for link in soup.find_all('a'):
        new_link = prepare_link(url, link.get('href'))
        if not is_outgoing(domain, new_link):
            scan_page(domain, new_link, website)


def scan_website(domain):
    url = "http://" + domain
    scan_page(url)


def search():
    url = "http://hackbulgaria.com/"
    url2 = input("Which site do you want to search? ")
    domain = get_domain(url)
    website = Website(url=domain)
    session.add(website)
    scan_page(domain, url, website)
    session.commit()


def search_word(search_word):
    # search_word = input("What do you want to search? ")
    # search_word = search_word.split()
    pages_searched = session.query(Page).filter(
        Page.title.like('%' + search_word + '%')).all()
    # for page in pages_searched:
        # print (page.url)
    return pages_searched


# search()
# search_word()
