from Dicts import db_adapter


class Simple:
    def __init__(self, data, code):
        self.__code = "dict" + code
        if isinstance(data, dict):
            self.make_single(data)

    def make_single(self, data):
        for key in data.keys():
            self[key] = data[key]

    def save_single(self):
        result = db_adapter.db[self.__code].insert_one(self.__dict__)
        return result.inserted_id