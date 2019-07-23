from psycopg2.pool import SimpleConnectionPool
from scrapy.exceptions import DropItem


class DuplicatesPipeline(object):
    """
    Pipeline to remove duplicate items based on response url.
    """

    def __init__(self):
        self.urls = set()

    # Check if a url is in the set of urls, if so then stop processing it
    def process_item(self, item, spider):
        if item['url'] in self.urls:
            raise DropItem(f"Duplicate url found: {item['url']}")
        else:
            self.urls.add(item['url'])
            return item


class PostgrePipeline(object):
    """
    Pipeline to save items into a Postgresql database.
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

    # Create a connection pool upon opening a spider
    def open_spider(self, spider):
        self.pool = SimpleConnectionPool(1, 1000,
            dbname=self.dbname, user=self.user,
            password=self.password, host=self.host, port=self.port)

    # Close all connections on closing a spider
    def close_spider(self, spider):
        self.pool.closeall()

    # Connect to the database and insert an item
    def process_item(self, item, spider):
        conn = self.pool.getconn()
        cur = conn.cursor()

        table = item.table
        keys_string = ", ".join(item.keys())
        values = tuple(item.values())
        params = ", ".join(['%s' for key in item.keys()])

        sql = f"INSERT INTO {table} ({keys_string}) VALUES ({params})"
        cur.execute(sql, values)

        conn.commit()
        cur.close()
        conn.close()
        return item
