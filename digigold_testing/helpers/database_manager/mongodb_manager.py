from pymongo import MongoClient
from digigold_testing.config import *


class MongoDBManager:
    def __init__(self, database_name, collection_name):
        """
        Creates a Mongo manager to perform CRUD operations
        :param database_name: Name of the database
        :param collection_name: Name of the collection
        """
        self.client = MongoClient(MONGO_CLIENT)
        self.db = self.client[database_name]
        self.collection = self.db[collection_name]

    def insert_data(self, data):
        result = self.collection.insert_one(data)
        print(f"Data inserted with ObjectId: {result.inserted_id}")

    def insert_many_data(self, data_list):
        result = self.collection.insert_many(data_list)
        print(f"Data inserted with ObjectIds: {result.inserted_ids}")

    def update_data(self, query, update_data):
        result = self.collection.update_one(query, {"$set": update_data})

    def get_random_user(self):
        pipeline = [{"$sample": {"size": 1}}]
        result = list(self.collection.aggregate(pipeline))
        return result[0]['id'] if result else self.collection.find_one()['id']

    def get_sale_eligible_random_user(self):
        result = self.collection.find_one()
        return result['id']

    def increment_amount_spent(self, query, amount_to_increment):
        update_data = {"$inc": {"amount_spent": amount_to_increment}}
        result = self.collection.update_one(query, update_data)

    def increment_gold_volume(self, query, volume_to_increment):
        update_data = {"$inc": {"balance_gold": volume_to_increment}}
        result = self.collection.update_one(query, update_data)

    def close_connection(self):
        self.client.close()
