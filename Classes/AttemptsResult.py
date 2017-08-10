import datetime
from crm import mongoClient
from bson.objectid import ObjectId

class AttemptsResult:
    def __init__(self, resultDict):
        self.answer = resultDict["answer"]
        self.question = resultDict["question"]
        self.created_at = datetime.datetime.utcnow()
        self.attempt = ObjectId(resultDict['attempt'])
        self.client = ObjectId(resultDict['client'])

        tmp = mongoClient.db.scriptsAttempts.insert_one(self.__dict__).inserted_id
