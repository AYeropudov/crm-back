import collections
from crm import mongo_client

class References:
    __slots__ = ['collection']

    def __init__(self):
        self.collection = collections.defaultdict(list)

    def get_collections_from_db(self):
        return mongo_client.db.references.find({})

    def fill_collection(self):
        for ref in self.get_collections_from_db():
            self.collection[ref['code']].append(ref)
        return self