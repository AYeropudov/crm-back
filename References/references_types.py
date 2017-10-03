from crm import mongo_client

class ReferencesTypes:

    def __init__(self):
        self.collection = list()

    @property
    def fill_collection(self):
        return mongo_client.db.references_types.find({})

    def get_types_from_db(self):
        for ref_type in self.fill_collection:
            self.collection.append(ref_type)
        return self
