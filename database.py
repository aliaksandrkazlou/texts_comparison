import imp
from urllib.parse import quote_plus
from bson.objectid import ObjectId
from bson.errors import InvalidId

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import ConnectionFailure


class Database:
    @classmethod
    def from_config(cls, config):
        raise NotImplementedError

    def get_status(self):
        raise NotImplementedError

    def get_query(self, query_id):
        raise NotImplementedError

    def save_query(self, query_document):
        raise NotImplementedError


class MongoDatabase(Database):
    def __init__(self, username, password, cluster, db_name) -> None:
        super().__init__()
        username = quote_plus(username)
        password = quote_plus(password)
        uri = (
            f"mongodb+srv://{username}:{password}@{cluster}"
            "/?retryWrites=true&w=majority"
        )
        self.client = MongoClient(uri, server_api=ServerApi("1"))
        self.db_name = db_name

    @classmethod
    def from_config(cls, config):
        username = config["username"]
        password = config["password"]
        cluster = config["cluster"]
        db_name = config["db_name"]

        return cls(username, password, cluster, db_name)

    def get_status(self):
        try:
            self.client.admin.command("ismaster")
        except ConnectionFailure:
            return False
        return True

    def get_query(self, query_id):
        db = self.client[self.db_name]
        collection = db["queries"]
        try:
            document = collection.find_one(
                {"_id": ObjectId(query_id)}, {"text1": 1, "text2": 1, "_id": 0}
            )
        except InvalidId:
            document = None
        return document

    def save_query(self, query_document):
        db = self.client[self.db_name]
        collection = db["queries"]
        query_id = collection.insert_one(query_document).inserted_id
        return query_id
