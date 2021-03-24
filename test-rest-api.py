from dct_business_api import ApiConstants, ApiException, ApiClient
from private_params import account_name, url_base, user_name, password
import logging
import logging.config
import time
import asyncio

def test_create_order(rest_client):
    try:
        res = rest_client.create_order(
            ApiConstants.EXCHANGE_BINANCE,
            ApiConstants.TRANSACTION_TYPE_SPOT,
            account_name,
            time.time(),
            ApiConstants.SYMBOL_BTCUSDT,
            ApiConstants.ORDER_SIDE_BUY,
            ApiConstants.ORDER_TYPE_LIMIT,
            ApiConstants.ORDER_TIME_IN_FORCE_GTC,
            0.0002,
            53000
        )
        print(res)
        oid = res['orderId']
        #asyncio.ensure_future(rest_client.cancel_order_later(oid,1))
        return oid
    except ApiException as e:
        print(e.code)
        print(e.message)
        print(e.extra)


def test_cancel_order(rest_client, order_id):
    """

    code=order_delete_not_supported 时，订单状态已是终态，不支持进一步的操作。此时e.data为订单信息

    """
    try:
        res = rest_client.cancel_order(order_id)
        print(res)
    except ApiException as e:
        print(e.code)
        print(e.data)
        print(e.message)
        print(e.extra)


def test_get_order(rest_client, order_id):
    res = rest_client.get_order(order_id);
    print(res)


def test_get_order_trades(rest_client, order_id):
    res = rest_client.get_order_trades(order_id);
    print(res)


def test_get_account(rest_client, exchange, account_name):
    res = rest_client.get_account_balance(exchange, account_name)
    print(res)


if __name__ == '__main__':

    logging.config.fileConfig('config/logging.cfg', )
    rest_client = ApiClient().rest_client(user_name, password, url_base);
    #orderid = test_create_order(rest_client)
    
    #test_get_order(rest_client,1374198349200134145)
    # test_get_order_trades(rest_client, 1369944153596739585)
    #test_get_account(rest_client, ApiConstants.EXCHANGE_BINANCE, account_name)
    test_cancel_order(rest_client,1374522371892854786)
    test_get_account(rest_client, ApiConstants.EXCHANGE_BINANCE, account_name)
