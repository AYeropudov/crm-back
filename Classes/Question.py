from crm import mongoClient
from bson.objectid import ObjectId
from Classes import Answer
class question():
    def __init__(self, id):
        question = mongoClient.db.questions.find_one({"_id": ObjectId(id)})
        if question is not None:
            self.id = str(question['_id'])
            self.type = question['type']
            self.text = question['text']
            self.answers = self.get_answers()
            self.key = str(question['_id'])

    def get_answers(self):
        answers = mongoClient.db.answersToQuestionRelations.find({"question": ObjectId(self.id)})
        result = []
        if answers is not None:
            result = [Answer.answer(item).__dict__ for item in answers]
        return result