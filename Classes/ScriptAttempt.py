import datetime
from crm import mongoClient
from bson.objectid import ObjectId

class Attempt():
    def __init__(self, script, client):
        self.script = ObjectId(script['_id'])
        self.client = client
        self.createdAt = datetime.datetime.utcnow()
        tmp = mongoClient.db.scriptsAttempts.insert_one(self.__dict__).inserted_id
        if tmp is not None:
            self.id = tmp