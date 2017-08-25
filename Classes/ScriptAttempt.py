import datetime

from Classes import ClientsDb, Script
from crm import mongo_client
from bson.objectid import ObjectId

class Attempt():
    def __init__(self, script=None, client=None, id=None):
        if id is not None:
            self.start_by_id(id)
        else:
            self.script = ObjectId(script.id)
            self.client = ObjectId(client)
            self.createdAt = datetime.datetime.utcnow()
            self.timeEnd = None
            self.completed = False

            tmp = mongo_client.db.scriptsAttempts.insert_one(self.__dict__).inserted_id
            if tmp is not None:
                self.id = str(tmp)
                self.script = str(self.script)
                self.client = str(self.client)
                del self._id

    def complete(id):
        mongo_client.db.scriptsAttempts.update_one({"_id": ObjectId(id)}, {"$set":{"completed": True, "timeEnd": datetime.datetime.utcnow()}})

    def start_by_id(self, id):
        result = mongo_client.db.scriptsAttempts.find_one({"_id": ObjectId(id)})
        if result is not None:
            client_db = ClientsDb.ClientsDb()
            self.id = str(result['_id'])
            self.client = client_db.get_client_for_attempt(id=result["client"])
            self.script = Script.script(id=str(result["script"]))
