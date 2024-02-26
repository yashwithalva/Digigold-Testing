import json
import requests
from digigold_testing.helpers.utils.calculation import round_down
from digigold_testing.user_transaction_flow.dto import buy_dto
from digigold_testing.config import *


class UserBuyFlow:
    def __init__(self, tax, mongo_manager, buy_order_no=1):
        self.rate_id = ''
        self.asset_price = 0
        self.tax = tax
        self.buy_order_no = buy_order_no
        self.order_id = ''
        self.mongo = mongo_manager

    def get_buy_price(self) -> bool:
        req_param = {
            'materialCode': MATERIAL_CODE
        }
        res = requests.get(HOST + BUY_PRICE_URL, headers=HEADER_INFO, params=req_param)
        print(res.json())
        if not res.json().get('success'):
            return False

        self.rate_id = res.json()['data']['id']
        self.asset_price = res.json()['data']['assetPrice']
        return True

    def buy_verify(self, buy_price, user_id) -> bool:
        if not self.rate_id or not self.asset_price:
            return False

        volume = self._get_volume_from_price(buy_price)
        buy_dto.buy_verify['rateId'] = self.rate_id
        buy_dto.buy_verify['userId'] = user_id
        buy_dto.buy_verify['volume'] = volume
        buy_dto.buy_verify['amount'] = buy_price
        buy_dto.buy_verify['merchantOrderId'] = f'{BUY_MERCHANT_ORDER_PREFIX}{self.buy_order_no}'

        json_body = json.dumps(buy_dto.buy_verify)
        res = requests.post(HOST + BUY_VERIFY_URL, headers=HEADER_INFO, data=json_body)
        print(res.json())
        if not res.json().get('success'):
            return False

        self.order_id = res.json()['data']['orderId']
        self.buy_order_no += 1
        return volume

    def buy_confirm(self, user_id) -> any:
        if not self.order_id or len(user_id) == 0:
            return False
        buy_dto.buy_confirm['userId'] = user_id
        buy_dto.buy_confirm['orderId'] = self.order_id
        json_body = json.dumps(buy_dto.buy_confirm)
        res = requests.post(HOST+BUY_CONFIRM_URL, headers=HEADER_INFO, data=json_body)
        if not res.json()['success']:
            return False
        print(res.json()['data'])
        return res.json()['data']['status']

    def buy_status(self, user_id) -> any:
        if not self.order_id or len(user_id) == 0:
            return False
        buy_dto.buy_status['userId'] = user_id
        buy_dto.buy_status['orderId'] = self.order_id
        res = requests.post(HOST+BUY_STATUS_URL, headers=HEADER_INFO, params=buy_dto.buy_status)
        if not res.json()['success']:
            return False
        print(res.json()['data'])
        return res.json()['data']['status']

    def _get_volume_from_price(self, buy_price) -> int:
        tax_item = round((self.asset_price * 1.5)/100, 2)
        tax_on_rate = tax_item * 2
        total_price = round(self.asset_price + tax_on_rate, 2)
        vol = buy_price/total_price
        volume = round_down(buy_price/total_price, 4)
        print(f"Volume for order id: {BUY_MERCHANT_ORDER_PREFIX}{self.buy_order_no} is {volume} and amount is {buy_price}")
        return volume
