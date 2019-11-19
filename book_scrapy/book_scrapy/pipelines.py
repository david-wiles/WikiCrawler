from psycopg2.pool import SimpleConnectionPool
from scrapy import FormRequest
from scrapy.exceptions import DropItem


class DuplicatesPipeline(object):
    """
    Remove duplicate wikipedia pages based on scraped title.
    Although urls are more likely to be unique, some urls redirect to the same page, so there would be duplicates
    using that method. Almost all Wikipedia articles will have unique titles (since non-unique titles have
    a description in parenthesis)
    """

    def __init__(self):
        self.titles = set()

    # Check if a url is in the set of urls, if so then stop processing it
    def process_item(self, item, spider):
        if item['title'] in self.titles:
            raise DropItem(f"Duplicate title found: {item['title']}")
        else:
            self.titles.add(item['title'])
            return item


class PostgrePipeline(object):
    """
    Save items into a PostgreSQL database. Uses a connection pool of 16 possible connection
    """

    collection_name = 'scrapy_items'

    def __init__(self, dbname, user, password, host, port):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    # Get connection string from settings
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            dbname=crawler.settings.get('PGDATABASE'),
            user=crawler.settings.get('PGUSER'),
            password=crawler.settings.get('PGPASSWORD'),
            host=crawler.settings.get('PGHOST'),
            port=crawler.settings.get('PGPORT')
        )

    # Create a connection pool upon opening a spider. Up to 16 connections
    def open_spider(self, spider):
        self.pool = SimpleConnectionPool(1, 16,
            dbname=self.dbname, user=self.user,
            password=self.password, host=self.host, port=self.port)

    # Close all connections on closing a spider
    def close_spider(self, spider):
        self.pool.closeall()

    # Connect to the database and insert an item
    def process_item(self, item, spider):
        connection = self.pool.getconn()
        cur = connection.cursor()

        table = item.table
        keys_string = ", ".join(item.keys())
        values = tuple(item.values())
        params = ", ".join(['%s' for i in range(len(item))])

        sql = f"INSERT INTO {table} ({keys_string}) VALUES ({params})"
        cur.execute(sql, values)

        connection.commit()
        cur.close()
        self.pool.putconn(connection)
        return item
