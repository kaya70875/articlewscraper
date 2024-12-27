from itemadapter import ItemAdapter
import pymongo
import logging

class MongoPipeline:
    def __init__(self, mongo_uri, mongo_db, batch_size=100):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.batch_size = batch_size
        self.items = []
        self.inserted_count = 0

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        if self.items:
            self.db['sentences'].insert_many(self.items)
            self.inserted_count += len(self.items)
        self.client.close()
        logging.info(f'Total sentences inserted: {self.inserted_count}')

    def process_item(self, item, spider):
        self.items.append(ItemAdapter(item).asdict())
        if len(self.items) >= self.batch_size:
            self.db['sentences'].insert_many(self.items)
            self.inserted_count += len(self.items)
            self.items = []
        return item