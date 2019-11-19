from scrapy import Item, Field


# Attributes specific to a Wikipedia book article
class BookItem(Item):
    table = 'book'
    url = Field()
    title = Field()
    image = Field()
    author = Field()
    country = Field()
    language = Field()
    series = Field()
    genre = Field()
    publisher = Field()
    published = Field()
    media_type = Field()
    pages = Field()
    isbn = Field()
    oclc = Field()
    lc_class = Field()
    dewey_decimal = Field()
    preceded_by = Field()
    followed_by = Field()
    audio_read_by = Field()
    description = Field()
    other = Field()


# Attributes specific to a Wikipedia author article
class AuthorItem(Item):
    table = 'author'
    url = Field()
    name = Field()
    image = Field()
    born = Field()
    died = Field()
    education = Field()
    alma_mater = Field()
    occupation = Field()
    period = Field()
    genre = Field()
    genres = Field()
    spouse = Field()
    children = Field()
    pen_name = Field()
    nationality = Field()
    years_active = Field()
    subject = Field()
    notable_works = Field()
    notable_awards = Field()
    description = Field()
    other = Field()


# Generic post attributes. No information from sidebar
class PostItem(Item):
    table = 'post'
    # url = Field()
    title = Field()
    text = Field()
    # image_urls = Field()
    # images = Field()


# Built from a generic topic page, which may contain some text and many links to
# other articles
class TopicItem(Item):
    table = "topic"
    url = Field()
    title = Field()
    text = Field()
    links = Field()
