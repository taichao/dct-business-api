from dct_business_api import ApiConstants, ApiException, ApiClient
from private_params import account_name, url_base, user_name, password


def test_create_order(rest_client):
    try:
        res = rest_client.create_order(
            ApiConstants.EXCHANGE_BINANCE,
            ApiConstants.TRANSACTION_TYPE_SPOT,
            account_name,
            ApiConstants.SYMBOL_BTCUSDT,
            ApiConstants.ORDER_SIDE_BUY,
            ApiConstants.ORDER_TYPE_LIMIT,
            ApiConstants.ORDER_TIME_IN_FORCE_GTC,
            0.0004,
            45000
        )
        print(res)
    except ApiException as e:
        print(e.code)
        print(e.message)
        print(e.extra)


def test_cancel_order(rest_client, order_id):
    """

    code=order_delete_not_supported 时，订单状态已是终态，不支持进一步的操作。此时e.data为订单信息

    """
    try:
        res = rest_client.cancel_order(1369852686744256513)
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
    rest_client = ApiClient().rest_client(user_name, password, url_base);
    test_create_order(rest_client)
    # test_get_order_trades(rest_client, 1369852686744256513)
    # test_get_account(rest_client, ApiConstants.EXCHANGE_BINANCE, 'prod-spot')
