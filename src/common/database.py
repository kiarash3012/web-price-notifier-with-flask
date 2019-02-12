import pymongo


class Database(object):
    uri = "mongodb://127.0.0.1:27017/WebPriceNotifier"
    # "mongodb://user:pass@subdomain.mongolab.com:123456/testdb"
    DATABASE = None

    @staticmethod
    def initialize():
        clinet = pymongo.MongoClient(Database.uri)
        Database.DATABASE = clinet["WebPriceNotifier"]

    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)

    @staticmethod
    def update(collection, query, data):
        Database.DATABASE[collection].update(query, data, upsert=True)