from crm import mongo_client
from bson.objectid import ObjectId

class scripts_list():
    def __init__(self):
        scriptsList = mongo_client.db.scripts.find({})
        self.scripts = [{"id" : str(item['_id']), "title": item['title'], "countQuestions": len(item['questions'])} for item in scriptsList]
