from crm import mongo_client
from bson.objectid import ObjectId

class Client():
    def __init__(self, dictClient = None):
        if dictClient is not None:
            self.fill_from_db_res(dictClient)
        else:
            pass

    def fill_from_dict(self, dictClient):
        self.title = dictClient["titleInput"]
        self.contact = dictClient["contactInput"]
        self.region = dictClient["regionInput"]
        self.city = dictClient["cityInput"]
        self.phone = dictClient["phoneInput"]
        self.email = dictClient["emailInput"]
        self.id = ''
        if '_id' in dictClient:
            self.id = str(dictClient['_id'])

    def fill_from_db_res(self, dictClient):
        self.title = dictClient["title"]
        self.contact = dictClient["contact"]
        self.region = dictClient["region"]
        self.city = dictClient["city"]
        self.phone = dictClient["phone"]
        self.email = dictClient["email"]
        self.id = ''
        if '_id' in dictClient:
            self.id = str(dictClient['_id'])