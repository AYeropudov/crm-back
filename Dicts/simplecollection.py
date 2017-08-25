from Dicts import db_adapter
from Dicts.simple import Simple


class Simplecollection:
    def __init__(self, data):
        self.collection = []
        self.make_patch(data)

    def make_patch(self, data):
        list_of_new_simple_dicts = []
        for item in data:
            list_of_new_simple_dicts.append(Simple(item).__dict__)
        self.collection = list_of_new_simple_dicts

    def save(self, code):
        result = db_adapter.db["dict_"+code].insert_many(self.collection)
        return result.inserted_ids