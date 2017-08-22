from Dicts import db_adapter
from Dicts.simple import Simple


class SimpleCollection:
    def __init__(self, data, code):
        self.__code = "dict" + code
        self.__collection = []
        self.make_patch(data)

    def make_patch(self, data):
        list_of_new_simple_dicts = []
        for item in data:
            list_of_new_simple_dicts.append(Simple(item, self.__code))
        self.__collection = list_of_new_simple_dicts

    def save_many(self):
        result = db_adapter.db[self.__code].insert_many(self.__collection)
        return result.inserted_ids