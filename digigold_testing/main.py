import time

from config import MONGO_DB_NAME, MONGO_USER_COLLECTION, BUY_SAVE, SELL_SAVE
from helpers.database_manager import mongodb_manager
from helpers.utils.random_generator import *
from helpers.utils.fileop import *
from user.api_handler.user_creation import UserGenerationFlow
import user_transaction_flow.api_handler.user_buy_flow as ub
import user_transaction_flow.api_handler.user_sell_flow as us


def buy_transactions(number_of_transactions) -> None:
    """
    Buy Transaction user flow
    :param number_of_transactions: Number of transactions
    :return: None
    """
    mongo_manager = mongodb_manager.MongoDBManager(MONGO_DB_NAME, MONGO_USER_COLLECTION)
    n = read_order_value(BUY_SAVE) + 1
    buy_flow = ub.UserBuyFlow(3, mongo_manager, buy_order_no=n)

    for i in range(number_of_transactions):
        is_success = buy_flow.get_buy_price()
        if not is_success:
            print("Buy verify failed. Not going to continue")
            return

        amount = get_random_buy_price()
        user_id = mongo_manager.get_random_user()
        is_verified = buy_flow.buy_verify(amount, user_id)
        if not is_verified:
            print("Buy verify failed. Not going to continue")
            write_new_value(BUY_SAVE, buy_flow.buy_order_no)
            return

        value = buy_flow.buy_confirm(user_id)
        print(value)
        if value == 'PROCESSING':
            print("Retry status")
            time.sleep(2)
            ans = buy_flow.buy_status(user_id)
            if ans == 'PROCESSING' or ans == 'FAILED':
                print("Buy status retry failed")
                write_new_value(BUY_SAVE, buy_flow.buy_order_no)
                return
            elif ans == 'COMPLETED':
                print(">> Buy Complete")

        query = {'userId': user_id}
        mongo_manager.increment_amount_spent(query, amount)
        mongo_manager.increment_gold_volume(query, is_verified)

        write_new_value(BUY_SAVE, buy_flow.buy_order_no)


def sell_transactions(number_of_transactions) -> None:
    """
    Sell Transaction user flow
    :param number_of_transactions: Number of transactions
    :return: None
    """
    mongo_manager = mongodb_manager.MongoDBManager(MONGO_DB_NAME, MONGO_USER_COLLECTION)
    n = read_order_value(SELL_SAVE) + 1
    sell_flow = us.UserSellFlow(mongo_manager, sell_order_no=n)

    for i in range(number_of_transactions):
        is_success = sell_flow.get_sell_price()
        if not is_success:
            print("Sell verify failed. Not going to continue")
            return

        amount = get_random_sell_price()
        user_id = mongo_manager.get_sale_eligible_random_user(amount)
        is_verified = sell_flow.sell_verify(amount, user_id)
        if not is_verified:
            print("Sell verify failed. Not going to continue")
            write_new_value(SELL_SAVE, sell_flow.sell_order_no)
            return

        value = sell_flow.sell_confirm(user_id)
        print(value)
        if value == 'PROCESSING':
            print("Retry status")
            time.sleep(2)
            ans = sell_flow.sell_status(user_id)
            if ans == 'PROCESSING' or ans == 'FAILED':
                print("Sell status retry failed")
                write_new_value(SELL_SAVE, sell_flow.sell_order_no)
                return
            elif ans == 'COMPLETED':
                print(">> Sell Complete")

        query = {'userId': user_id}
        mongo_manager.increment_amount_withdrawn(query, amount)
        mongo_manager.decrement_gold_volume(query, is_verified)

        write_new_value(SELL_SAVE, sell_flow.sell_order_no)


def main():
    mongo_manager = mongodb_manager.MongoDBManager(MONGO_DB_NAME, MONGO_USER_COLLECTION)
    xyz = UserGenerationFlow(10, mongo_manager)
    xyz.generate_fixed_user()


if __name__ == '__main__':
    sell_transactions(2)
