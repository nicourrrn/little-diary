from pymongo import MongoClient
from note import Note


class Database:
    def __init__(self, database_name, collection_name: str):
        self.client = MongoClient("localhost", 27017)
        self.collection = self.client.get_database(database_name).get_collection(collection_name)

    def save_note(self, note: Note):
        self.collection.insert_one(note._asdict())

    def load_notes(self) -> list[Note]:
        return list(
            map(lambda note: Note(**note),
                self.collection.find({}, {"_id": False})))
