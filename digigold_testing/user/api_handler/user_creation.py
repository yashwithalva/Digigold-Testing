import json
import requests
from digigold_testing.user.dto import user
from digigold_testing.helpers.random import random
from digigold_testing.config import *
from digigold_testing.helpers.database_manager import mongodb_manager

class UserGenerationFlow:
    def __init__(self, total_user_count, mongo_manager, rate=5, duration=1, pause_interval=5, pause_length=1):
        """
        Generates a new user for a tenant at constant rate.
        The rate at which a user is created can be controlled using rate and duration.
        Can also specify the pause length and pause intervals at which time no users will be generated
        TIME is measured in minutes
        :param total_user_count: Number of users to create
        :param rate: Rate at which users are created
        :param duration: Duration for which the rate is applied
        :param pause_interval: Intervals at which user will not be created
        :param pause_length: Time Length of the pause interval
        """
        self.rate = rate
        self.duration = duration
        self.pause_interval = pause_interval
        self.pause_length = pause_length
        self.total_user_count = total_user_count
        self.mongo_manager = mongo_manager

    @staticmethod
    def create_new_user(user_count=0) -> dict:
        """
        Creates a new user and adds it to database_manager
        :param user_count: User number
        :return: The id of the created user.
        """
        user.create_user_req['firstName'] = f'TestUser-{user_count}'
        user.create_user_req['lastName'] = random.generate_token(5)
        json_body = json.dumps(user.create_user_req)
        res = requests.post(HOST + CREATE_USER_URL, data=json_body, headers=HEADER_INFO)
        print(res.json())
        return res.json()['data']

    def generate_fixed_user(self):
        """
        Generates user at regular intervals
        """
        for i in range(0, self.total_user_count):
            user_data = self.create_new_user(i+1)
            user_data['balance_gold'] = 0
            user_data['amount_spent'] = 0
            user_data['amount_withdrawn'] = 0
            self.mongo_manager.insert_data(user_data)
        return True

    def generate_users_at_rate(self):
        return self.generate_fixed_user()

# All the user created will be added to database_manager.
