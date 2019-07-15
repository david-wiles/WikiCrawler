# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class BookItem(Item):
    url = Field()
    title = Field()
    image = Field()
    author = Field()
    illustrator = Field()
    country = Field()
    language = Field()
    series = Field()
    genre = Field()
    publisher = Field()
    publication_date = Field()
    media_type = Field()
    pages = Field()
    isbn = Field()
    oclc = Field()
    lc_class = Field()
    preceded_by = Field()
    followed_by = Field()
    audio_read_by = Field()
    description = Field()
    unknown = Field()


class AuthorItem(Item):
    url = Field()
    name = Field()
    image = Field()
    born = Field()
    died = Field()
    residence = Field()
    education = Field()
    occupation = Field()
    period = Field()
    genre = Field()
    genres = Field()
    spouse = Field()
    children = Field()
    pen_name = Field()
    citizenship = Field()
    nationality = Field()
    years_active = Field()
    subject = Field()
    notable_works = Field()
    description = Field()
    unknown = Field()
