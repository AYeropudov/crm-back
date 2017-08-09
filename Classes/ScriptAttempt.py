import datetime
from crm import mongoClient
from bson.objectid import ObjectId

class Attempt():
    def __init__(self, script, client):
        self.script = ObjectId(script.id)
        self.client = client
        self.createdAt = datetime.datetime.utcnow()
        self.timeEnd = None
        self.completed = False

        tmp = mongoClient.db.scriptsAttempts.insert_one(self.__dict__).inserted_id
        if tmp is not None:
            self.id = str(tmp)

    def complete(id):
        mongoClient.db.scriptsAttempts.update_one({"_id": ObjectId(id)}, {"$set":{"completed": True, "timeEnd": datetime.datetime.utcnow()}})