from digigold_testing import config

sell_verify = {
    'rateId': '',
    'userId': '',
    'volume': 0,
    'amount': 0,
    'code': 'SKU1001',
    'merchantOrderId': '',
    'calculationType': 'BY_AMOUNT'
}

sell_confirm = {
    'userId': '',
    'orderId': '',
    'code': config.MATERIAL_CODE,
    'isSync': False
}

sell_status = {
    'orderId': '',
    'userId': ''
}
