import random
import time

from config import MONGO_DB_NAME, MONGO_USER_COLLECTION
from helpers.database_manager import mongodb_manager
from user.api_handler.user_creation import UserGenerationFlow
from user_transaction_flow.api_handler.user_buy_flow import UserBuyFlow


def write_new_value(value):
    f_extra = open('extra.txt', 'w')
    f_extra.write(str(value))
    f_extra.close()


def get_random_buy_price():
    value = random.randint(0, 5)
    return value * 10


def buy_transactions():
    f_extra = open('digigold_testing/extra.txt', 'r')
    mongo_manager = mongodb_manager.MongoDBManager(MONGO_DB_NAME, MONGO_USER_COLLECTION)
    n = int(f_extra.readline()) + 1
    f_extra.close()
    buy_flow = UserBuyFlow(3, mongo_manager, buy_order_no=int(n))

    for i in range(1):
        is_success = buy_flow.get_buy_price()
        if not is_success:
            print("Buy verify failed. Not going to continue")
            return

        amount = get_random_buy_price()
        user_id = mongo_manager.get_random_user()
        is_verified = buy_flow.buy_verify(amount, user_id)
        print(is_verified)
        if not is_verified:
            print("Buy verify failed. Not going to continue")
            write_new_value(buy_flow.buy_order_no)
            return

        value = buy_flow.buy_confirm(user_id)
        print(value)
        if value == 'PROCESSING':
            print("Retry status")
            time.sleep(3)
            ans = buy_flow.buy_status(user_id)
            if ans == 'PROCESSING' or ans == 'FAILED':
                print("Buy status retry failed")
                write_new_value(buy_flow.buy_order_no)
                return
            elif ans == 'COMPLETED':
                print(">> Buy Complete")

        query = {'_id': user_id}
        mongo_manager.increment_amount_spent(query, amount)
        mongo_manager.increment_gold_volume(query, is_verified)

        write_new_value(buy_flow.buy_order_no)


def main():
    mongo_manager = mongodb_manager.MongoDBManager(MONGO_DB_NAME, MONGO_USER_COLLECTION)
    xyz = UserGenerationFlow(10, mongo_manager)
    xyz.generate_fixed_user()


if __name__ == '__main__':
    buy_transactions()
