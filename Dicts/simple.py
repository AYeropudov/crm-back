from Dicts import db_adapter


class Simple:
    def __init__(self, data):
        if isinstance(data, dict):
            self.make_single(data)

    def make_single(self, data):
        self.__dict__= data

    def save(self, code):
        result = db_adapter.db["dict_"+code].insert_one(self.__dict__)
        return result.inserted_id