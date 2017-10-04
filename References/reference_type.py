from bson import ObjectId
from transliterate import slugify
from crm import mongo_client
class ReferenceType(object):
    __slots__ = ['title', 'children', 'key', '_id']

    def __init__(self):
        self.key = None
        self.title = None
        self.children = []
        self._id = None

    def from_json(self, json_data):
        for key, value in json_data.items():
            try:
                setattr(self, key, value)
                if key == 'title':
                    value = slugify(u'{}'.format(value)) or value
                    setattr(self, 'key', value)
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
    def save_ref_type_to_db(self):
        return bool(str(mongo_client.db.references_types.insert_one(self.to_dict).inserted_id))

    @property
    def update_reference_in_db(self):
        result = mongo_client.db.references.update_one({"_id": ObjectId(self._id)}, {"$set": self.to_dict_for_exist},
                                                       upsert=False)
        return bool(result.modified_count)

    @property
    def remove_reference_from_db(self):
        return bool(mongo_client.db.references.delete_one({"_id": ObjectId(self._id)}).deleted_count)

    @property
    def to_dict(self):
        return {key: getattr(self, key) for key in self.__slots__ if getattr(self, key) is not None}

    @property
    def to_dict_for_exist(self):
        return {key: getattr(self, key) for key in self.__slots__ if
                getattr(self, key) is not None and key is not '_id'}