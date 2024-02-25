from digigold_testing import config

buy_verify = {
    'rateId': '',
    'userId': '',
    'volume': 0,
    'amount': 0,
    'code': config.MATERIAL_CODE,
    'merchantOrderId': '',
    'calculationType': 'BY_AMOUNT'
}

buy_confirm = {
    'userId': '',
    'orderId': '',
    'code': config.MATERIAL_CODE
}

buy_status = {
    'orderId': '',
    'userId': ''
}