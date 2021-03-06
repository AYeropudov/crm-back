from Classes import Client
from crm import mongo_client
from bson.objectid import ObjectId

class ClientsDb():

    def addNew(self, client):
        return mongo_client.db.clients.insert_one(client.__dict__).inserted_id

    def get_all(self):
        result = []
        resource = mongo_client.db.clients.find({})
        for each_client in resource:
            result.append(Client.Client(each_client))
        return result

    def get_client_by_id(self, id):
        resource = mongo_client.db.clients.find_one({"_id": ObjectId(id)})
        if resource is not None:
            return  Client.Client(resource)
        return None

    def get_client_for_attempt(self, id):
        resource = mongo_client.db.clients.find_one({"_id": id})
        if resource is not None:
            return  Client.Client(resource)
        return None