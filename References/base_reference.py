from bson import ObjectId
from crm import mongo_client

class BaseReference:
    __slots__ = ['code','type', 'value', '_id', 'title', 'external_id']

    def __init__(self):
        self.type = None
        self.value = None
        self._id = None
        self.code = None
        self.title = None
        self.external_id = None

    def from_json(self, json_data):
        for key, value in json_data.items():
            try:
                setattr(self, key, value)
            except AttributeError:
                continue
        return self

    def load_from_mongo(self, mongo_obj):
        for key, value in mongo_obj.items():
            try:
                if type(value) is ObjectId:
                    value = str(value)
                setattr(self, key, value)
            except AttributeError:
                pass
        return self

    @property
    def save_reference_to_db(self):
        return bool(str(mongo_client.db.references.insert_one(self.to_dict).inserted_id))

    @property
    def update_reference_in_db(self):
        result = mongo_client.db.references.update_one({"_id": ObjectId(self._id)}, {"$set": self.to_dict_for_exist}, upsert=False)
        return bool(result.modified_count)

    @property
    def remove_reference_from_db(self):
        return bool(mongo_client.db.references.delete_one({"_id": ObjectId(self._id)}).deleted_count)

    @property
    def to_dict(self):
        return {key:getattr(self, key)  for key in self.__slots__ if getattr(self, key) is not None}

    @property
    def to_dict_for_exist(self):
        return {key: getattr(self, key) for key in self.__slots__ if getattr(self, key) is not None and key is not '_id'}