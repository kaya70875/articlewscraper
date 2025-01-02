from itemadapter import ItemAdapter
import pymongo
import logging

import pymongo.errors

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
            mongo_db=crawler.settings.get('MONGO_DATABASE'),
            batch_size=crawler.settings.getint('BATCH_SIZE', 100)
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        #Create a unique index on the 'text' field.
        self.db['sentences'].create_index([('text' , pymongo.ASCENDING)] , unique=True)
        logging.info('Created unique index on the text field')

    def close_spider(self, spider):
        if self.items:
            try:
                self.db['sentences'].insert_many(self.items , ordered=False)
                self.inserted_count += len(self.items)
            except pymongo.errors.BulkWriteError as e:
                # Handle duplicate key error
                for error in e.details['writeErrors']:
                    if error['code'] == 11000:
                        logging.warning(f'Duplicate key error: {error["errmsg"]}')
        self.client.close()
        logging.info(f'Total sentences inserted: {self.inserted_count}')

    def process_item(self, item, spider):
        self.items.append(ItemAdapter(item).asdict())
        if len(self.items) >= self.batch_size:
            try:
                self.db['sentences'].insert_many(self.items)
                self.inserted_count += len(self.items)
            except pymongo.errors.BulkWriteError as e:
                # Handle duplicate key error
                for error in e.details['writeErrors']:
                    if error['code'] == 11000:
                        logging.warning(f'Duplicate key error: {error["errmsg"]}')
            self.items = []
        return item