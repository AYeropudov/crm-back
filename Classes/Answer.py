from crm import mongoClient
from bson.objectid import ObjectId

class answer():
    def __init__(self, object):
        result = mongoClient.db.answers.find_one({"_id": object["answer"]})
        if result is not None:
            self.id = str(result["_id"])
            self.type = result['type']
            self.text = result['text']
            self.next = str(object["relQuestion"])