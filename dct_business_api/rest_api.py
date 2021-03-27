import requests

from dct_business_api.base import ApiException, Base


def handle_response(res):
    data = res.json()
    if data.get('code') == ApiException.SUCCESS:
        return data['data']
    raise ApiException(data)


class RestClient(Base):
    def __init__(self, user_name, password, rest_base):
        super(RestClient, self).__init__(user_name, password, rest_base, None)

    def __token_url(self, url):
        return f'{url}&access_token={self.get_access_token()}'

    def get_order(self, order_id):
        url = self.__token_url(f'{self.rest_base}/thirdParty/getOrder?orderId={order_id}')
        return handle_response(requests.get(url))

    def get_order_trades(self, order_id):
        """
        :return: 获取订单成交信息。若无则返回[]
        """
        url = self.__token_url(f'{self.rest_base}/thirdParty/getOrderTrades?orderId={order_id}')
        return handle_response(requests.get(url))

    def get_account_balance(self, exch, account_name):
        url = self.__token_url(
            f'{self.rest_base}/thirdParty/getAccountBalance?exch={exch}&accountName={account_name}')
        return handle_response(requests.get(url))

    def create_order(self, exch, account_name,client_order_id, symbol, side, type, time_in_force, quantity, price):
        """

        :param client_order_id: 客户方订单id，针对同一个id，服务端只会处理一次
        """
        param = {
            'exch': exch,
            'accountName': account_name,
            'clientId': client_order_id,
            'symbol': symbol,
            'side': side,
            'type': type,
            'timeInForce': time_in_force,
            'quantity': quantity,
            'price': price
        }
        return self.__create_order(**param)

    def cancel_order(self, order_id):
        url = self.rest_base + '/thirdParty/cancelOrderById'
        param = {
            'access_token': self.get_access_token(),
            'orderId': order_id
        }
        return handle_response(
            requests.post(url, data=param)
        )

    def cancel_all_orders(self, exch, symbol, account_name):
        url = self.rest_base + '/thirdParty/cancelAllOrders'
        param = {
            'access_token': self.get_access_token(),
            'exch': exch,
            'symbol': symbol,
            'accountName': account_name
        }
        return handle_response(
            requests.post(url, data=param)
        )

    def __create_order(self, **kwargs):
        url = self.rest_base + "/thirdParty/createOrder"
        access_token = self.get_access_token()
        param = {
            'access_token': access_token,
            **kwargs
        }
        res = requests.post(url, data=param)
        return handle_response(res)
