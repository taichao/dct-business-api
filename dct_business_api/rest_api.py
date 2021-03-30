import requests
import asyncio
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

    def get_ufuture_account_and_position(self, account_name, symbol, margin_type):
        url = self.__token_url(
            f'{self.rest_base}/ufuture/getBalanceAndPosition?symbol={symbol}&accountName={account_name}&marginType={margin_type}')
        return handle_response(requests.get(url))



    def create_order(self, exch, account_name,client_order_id, symbol, side, type, time_in_force, quantity, price, expire_after, expire_at=None, remark=None):
        """
        :param expire_after: !!!单位为秒 优先级expire_after>expire_at!!! 服务端下单发送成功后，expire_after后会出发取消逻辑（如果订单处于可取消状态）
        :param expire_at: !!!单位为毫秒时间戳!!!服务端提供自动取消功能。此字段表示自动取消的时间。格式为长度13的毫秒时间戳。 例如：int(time.time()) * 1000 + 2 * 60 * 1000 2分钟后自动过期。
                如果未传或小于当前时间，则不自动取消
        :param remark: 说明文字，仅做存储，查询
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
            'price': price,
            'expireAfter':expire_after,
            'expireAt': expire_at,
            'remark': remark
        }
        res = self.__create_order(**param)
        return res
    def cancel_order(self, order_id):
        url = self.rest_base + '/thirdParty/cancelOrderById'
        param = {
            'access_token': self.get_access_token(),
            'orderId': order_id
        }
        return handle_response(
            requests.post(url, data=param)
        )
    async def cancel_order_later(self,order_id,timeout=None):
        if timeout:
            await asyncio.sleep(timeout)
            self.cancel_order(order_id)

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

    def set_leverage(self, exch, account_name, symbol, leverage):
        """
        设置合约杠杆
        :param leverage: int类型 1 -> 125
        :return:
        """
        url = self.__token_url(
            f'{self.rest_base}/ufuture/setLeverage?exch={exch}&accountName={account_name}&symbol={symbol}&leverage={leverage}'
        )
        return handle_response(requests.post(url))

    def send_wechat(self, account_name, msg):
        url = self.__token_url(
            f'{self.rest_base}/thirdParty/sendWechat?accountName={account_name}&msg={msg}'
        )
        return handle_response(requests.post(url))
