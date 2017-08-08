from crm import mongoClient
from bson.objectid import ObjectId

class scripts_list():
    def __init__(self):
        scriptsList = mongoClient.db.scripts.find({})
        self.scripts = [{"id" : str(item['_id']), "title": item['title'], "countQuestions": len(item['questions'])} for item in scriptsList]
