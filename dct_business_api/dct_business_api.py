import logging, websockets, json, asyncio, requests
from datetime import *

CODE_SUCCESS = 'success'
CODE_PLATFORM_ERROR = 'platform_api_business_error'

class ApiClient:
    def __init__(self):
        self.__cache = dict()

    def subscribe_data(self, user_name, password, rest_base, ws_base):
        if user_name in self.__cache is not None:
            sd = self.__cache[user_name]
        else:
            sd = SubscribeData(user_name, password, rest_base, ws_base)
            if sd.get_access_token() is not None:
                self.__cache[user_name] = sd
                logging.info('new SubscribeData')
            else:
                raise Exception('login error')
        return sd


class Base:
    def __init__(self, user_name, password, rest_base, ws_base):
        self.user_name = user_name
        self.password = password
        self.rest_base = rest_base
        self.ws_base = ws_base
        self.access_token = None
        self.expire_time = None
        self.logger = logging.getLogger("dct_business_api")

    def handle_response(res):
        data = res.json()
        if 'code' in data:
            if CODE_SUCCESS == data['code']:
                return CODE_SUCCESS, data['data']
            else:
                logging.error(data)
                return data['code'], None
        return None

    def __login(self):
        url = self.rest_base + "/login"
        self.logger.info(f'login - {url} {self.user_name} {self.password}')
        r = requests.post(url, data={'userName': self.user_name, 'password': self.password})
        if (r.json()['code']) == 'success':
            return r.json()['data']['access_token']
        else:
            logging.error('login_error:%s', r.json())
            return

    def get_access_token(self):
        if self.access_token is not None and self.expire_time is not None and datetime.now() < self.expire_time:
            return self.access_token
        else:
            self.access_token = self.__login()
            if self.access_token is not None:
                self.expire_time = datetime.now() + timedelta(days=1)
                return self.access_token


class SubscribeData(Base):

    def __init__(self, user_name, password, rest_base, ws_base):
        super(SubscribeData,self).__init__(user_name, password, rest_base, ws_base)

    async def sub_depth(self, type, symbol, level, callback_func):
        """
        Args:
            type: 参见sub_topic
            level: 层级 5 15 20
        """
        p = f'symbol={symbol}&level={level}'
        await self.sub_topic("DEPTH", type, p, callback_func)

    def check_and_get_user_data(self, data, transaction_type, event_type, data_name):
        if 'transactionType' in data and transaction_type == data[
            'transactionType'] and 'eventType' in data and event_type == data['eventType']:
            if (data[data_name] in data):
                return data[data_name]

    async def sub_order_update(self, type, callback_func):
        def process_order_update(data):
            data = self.check_and_get_user_data(data, type, 'ORDER_UPDATE', 'orderUpdate')
            if data and callable(callback_func):
                callback_func(data)

        await self.sub_user_update(type, process_order_update)

    async def sub_account_update(self, type, callback_func):
        def process_account_update(data):
            data = self.check_and_get_user_data(data, type, 'ACCOUNT_UPDATE', 'accountUpdate')
            if data and callable(callback_func):
                callback_func(data)

        await self.sub_user_update(type, process_account_update)

    async def sub_user_update(self, type, **kwargs):
        def process_data(data):
            try:
                if 'accountUpdate' in data and 'on_account_update' in kwargs:
                    logging.info(f'accountUpdate - {data}')
                    if callable(kwargs['on_account_update']):
                        kwargs['on_account_update'](data['accountUpdate'])
                elif 'orderUpdate' in data and 'on_order_update' in kwargs:
                    logging.info(f'orderUpdate - {data}')
                    if (callable(kwargs['on_order_update'])):
                        kwargs['on_order_update'](data['orderUpdate'])
                else:
                    self.logger.error(f'unknown - {data}')
            except Exception as e:
                self.logger.error(e)

        await self.sub_topic('USER', type, 'test=test', process_data)

    async def sub_trade(self, type, symbol, callback_func):
        p = f'symbol={symbol}'
        await self.sub_topic("TRADE", type, p, callback_func)

    async def sub_book_ticker(self, type, symbol, callback_func):
        p = f'symbol={symbol}'
        await self.sub_topic("BOOK_TICKER", type, p, callback_func)

    async def sub_topic(self, stream_name, type, extra_param_str, callback_func):
        """
        Args:
            type: 交易类型，可选值包括SPOT, USD_FUTURE, COIN_FUTURE,
        """
        access_token = self.get_access_token()
        url = f'{self.ws_base}/ws/topic?type={type}&streamName={stream_name}&{extra_param_str}&access_token={access_token}'

        while True:
            try:
                async with websockets.connect(url) as websocket:
                    self.logger.info(url)
                    while not websocket.closed:
                        res = await websocket.recv()
                        res = json.loads(res)
                        if (callable(callback_func)):
                            callback_func(res)
            except Exception as e:
                await asyncio.sleep(5)
                self.logger.error('connect error，try later: %s', url)
                self.logger.exception(e)

class ApiConstants:

    TRANSACTION_TYPE_SPOT = 'SPOT'
    TRANSACTION_TYPE_USD_FUTURE = 'USD_FUTURE'
    TRANSACTION_TYPE_COIN_FUTURE = 'COIN_FUTURE'