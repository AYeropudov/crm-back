import datetime
from crm import mongo_client
from bson.objectid import ObjectId

class AttemptsResult:
    def __init__(self, answer, attempt):
        self.answer = ObjectId(answer.answer)
        self.question = ObjectId(answer.question)
        self.created_at = datetime.datetime.utcnow()
        self.attempt = ObjectId(attempt.id)
        self.client = attempt.client.id
        tmp = mongo_client.db.attemptsHistory.insert_one(self.__dict__).inserted_id
