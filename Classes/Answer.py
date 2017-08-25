from crm import mongo_client
from bson.objectid import ObjectId

class answer():
    def __init__(self, object=None, id=None):
        if id is not None:
            result = mongo_client.db.answersToQuestionRelations.find_one({"_id": ObjectId(id)})
            if result is not None:
                self.id = result["_id"]
                self.question = result["question"]
                self.answer = result["answer"]
        else:
            result = mongo_client.db.answers.find_one({"_id": object["answer"]})
            if result is not None:
                self.id = str(object["_id"])
                self.type = result['type']
                self.text = result['text']
                self.next = str(object["relQuestion"])
