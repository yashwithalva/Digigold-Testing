import json
import requests
from digigold_testing.helpers.utils.calculation import round_down
from digigold_testing.user_transaction_flow.dto import sell_dto
from digigold_testing.config import *


class UserSellFlow:
    def __init__(self, mongo_manager, sell_order_no=1):
        self.rate_id = ''
        self.asset_price = 0
        self.sell_order_no = sell_order_no
        self.order_id = ''
        self.mongo = mongo_manager

    def get_sell_price(self) -> bool:
        req_param = {
            'materialCode': MATERIAL_CODE
        }
        res = requests.get(HOST + SELL_PRICE_URL, headers=HEADER_INFO, params=req_param)
        print(res.json())
        if not res.json().get('success'):
            return False

        self.rate_id = res.json()['data']['id']
        self.asset_price = res.json()['data']['assetPrice']
        return True

    def sell_verify(self, sell_price, user_id) -> any:
        if not self.rate_id or not self.asset_price:
            return False

        volume = self._get_volume_from_price(sell_price)
        sell_dto.sell_verify['rateId'] = self.rate_id
        sell_dto.sell_verify['userId'] = user_id
        sell_dto.sell_verify['volume'] = volume
        sell_dto.sell_verify['amount'] = sell_price
        sell_dto.sell_verify['merchantOrderId'] = f'{SELL_MERCHANT_ORDER_PREFIX}{self.sell_order_no}'

        json_body = json.dumps(sell_dto.sell_verify)
        res = requests.post(HOST + SELL_VERIFY_URL, headers=HEADER_INFO, data=json_body)
        print(res.json())
        if not res.json().get('success'):
            return False

        self.order_id = res.json()['data']['orderId']
        self.sell_order_no += 1
        return volume

    def sell_confirm(self, user_id) -> any:
        if not self.order_id or len(user_id) == 0:
            return False
        sell_dto.sell_confirm['userId'] = user_id
        sell_dto.sell_confirm['orderId'] = self.order_id
        json_body = json.dumps(sell_dto.sell_confirm)
        res = requests.post(HOST+SELL_CONFIRM_URL, headers=HEADER_INFO, data=json_body)
        if not res.json()['success']:
            return False
        print(res.json()['data'])
        return res.json()['data']['status']

    def sell_status(self, user_id) -> any:
        if not self.order_id or len(user_id) == 0:
            return False
        sell_dto.sell_status['userId'] = user_id
        sell_dto.sell_status['orderId'] = self.order_id
        res = requests.post(HOST+SELL_STATUS_URL, headers=HEADER_INFO, params=sell_dto.sell_status)
        if not res.json()['success']:
            return False
        print(res.json()['data'])
        return res.json()['data']['status']

    def _get_volume_from_price(self, sell_price) -> int:
        total_price = round(self.asset_price, 2)
        volume = round_down(sell_price/total_price, 4)
        print(f"Volume for order id: {SELL_MERCHANT_ORDER_PREFIX}{self.sell_order_no} is {volume} for amount {sell_price}.")
        return volume
