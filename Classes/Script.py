from crm import mongo_client
from bson.objectid import ObjectId
from Classes.ScriptAttempt import Attempt


class script:
    # инициализируем скрипт по его id
    def __init__(self, id):
        result = mongo_client.db.scripts.find_one({"_id": ObjectId(id)})
        if result is not None:
            self.id = str(result["_id"])
            self.title = result['title']
            self.questions = [str(item) for item in result['questions']]

    def start(self, client):
        new_script_attempt = Attempt(self, client.id)
        return new_script_attempt
