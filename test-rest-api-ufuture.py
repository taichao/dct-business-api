from dct_business_api import ApiConstants, ApiException, ApiClient
from private_params import account_name, url_base, user_name, password
import logging,time
import logging.config
import time
import asyncio

def test_create_order(rest_client):
    try:
        res = rest_client.create_order(
            ApiConstants.EXCH_BINAS,
            account_name,
            int(time.time()),
            ApiConstants.SYMBOL_BTCUSDT,
            ApiConstants.ORDER_SIDE_BUY,
            ApiConstants.ORDER_TYPE_LIMIT,
            ApiConstants.ORDER_TIME_IN_FORCE_GTC,
            0.004,
            50000,
            expire_at= int(time.time()) * 1000 + 2 * 60 * 1000,
            remark='test'
        )
        print(res)
        oid = res['orderId']
        #asyncio.ensure_future(rest_client.cancel_order_later(oid,1))
        return oid
    except ApiException as e:
        print(e.code)
        print(e.message)
        print(e.extra)

def get_ufuture_account_and_position(rest_client):
    """
    查询U本位合约仓位
    :param rest_client:
    :return: 'techself01', 'balanceList': [{'accountName': 'techself01', 'asset': 'USDT', 'balance': 117.07660843, 'availableBalance': 117.07660843}], 'position': {'accountId': 6, 'accountName': 'techself01', 'symbol': 'BTCUSDT', 'marginType': 'cross', 'deposit': 0.0, 'positionAmt': -0.004, 'entryPrice': 55918.41, 'cumRealizedProfit': 18.35948, 'unrealizedProfit': 0.05611069, 'positionSide': 'BOTH'}}'techself01', 'balanceList': [{'accountName': 'techself01', 'asset': 'USDT', 'balance': 117.07660843, 'availableBalance': 117.07660843}], 'position': {'accountId': 6, 'accountName': 'techself01', 'symbol': 'BTCUSDT', 'marginType': 'cross', 'deposit': 0.0, 'positionAmt': -0.004, 'entryPrice': 55918.41, 'cumRealizedProfit': 18.35948, 'unrealizedProfit': 0.05611069, 'positionSide': 'BOTH'}}
    """
    res = rest_client.get_ufuture_account_and_position(account_name, ApiConstants.SYMBOL_BTCUSDT, ApiConstants.MARGIN_TYPE_CROSS)
    print(res)

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

def test_cancel_all_orders(rest_client, exch, symbol, account_name):
    try:
        rest_client.cancel_all_orders(exch,symbol, account_name)
        print('未报异常，说明操作成功')
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

    # get_ufuture_account_and_position(rest_client)
    # order_id = test_create_order(rest_client)
    # test_get_order(rest_client,order_id)
    # test_cancel_order(rest_client,order_id)
    # test_get_order(rest_client,order_id)
    #
    # order_id = test_create_order(rest_client)
    # test_cancel_all_orders(rest_client, ApiConstants.EXCH_BINAS, ApiConstants.SYMBOL_BTCUSDT, account_name)
    # test_get_order_trades(rest_client, 'bina:1375365963138002945')
    # test_get_account(rest_client, ApiConstants.EXCH_BINA, account_name)

