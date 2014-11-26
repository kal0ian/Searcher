from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import relationship

# A class that maps to a table, inherits from Base
Base = declarative_base()


# Our class will be mapped to a table with name student
# Each field is a Column with the given type and constraints
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
    desc = Column(String)
    SSL = Column(Integer)
    multi_lang = Column(Integer)
    rating = Column(Integer)

def define_rating(this_page):
	rating = 0
	if this_page.SSL != 0:
		rating += 1
	rating += this_page.pages_count // 10
	rating += this_page.HTML_version
	return rating



engine = create_engine("sqlite:///orm.db")
# will create all tables
Base.metadata.create_all(engine)
