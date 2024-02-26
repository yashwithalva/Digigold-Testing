from pymongo import MongoClient
from digigold_testing.config import *
import random


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
        return result[0]['userId'] if result else self.collection.find_one()['userId']

    def get_sale_eligible_random_user(self, amount):
        query = {"amount_spent": {"$gt": amount}}
        result = list(self.collection.find(query))
        if len(result) == 0:
            return '-1'
        rand = random.choice(result)
        return rand.get("userId")

    def increment_amount_spent(self, query, amount_to_increment):
        update_data = {"$inc": {"amount_spent": amount_to_increment}}
        result = self.collection.update_one(query, update_data)
        print('Incremented Amount: ' + str(result))

    def increment_amount_withdrawn(self, query, amount_to_increment):
        update_data = {"$inc": {"amount_withdrawn": amount_to_increment}}
        result = self.collection.update_one(query, update_data)
        print('Incremented Withdraw Amount: ' + str(result))

    def increment_gold_volume(self, query, volume_to_increment):
        update_data = {"$inc": {"balance_gold": volume_to_increment}}
        result = self.collection.update_one(query, update_data)
        print('Incremented Volume: ' + str(result))

    def decrement_gold_volume(self, query, volume_to_decrement):
        if volume_to_decrement <= 0:
            print("Not incrementing the gold volume")
            return
        update_data = {"$inc": {"balance_gold": -volume_to_decrement}}
        result = self.collection.update_one(query, update_data)
        print('Decrement Volume: ' + str(result))

    def close_connection(self):
        self.client.close()
