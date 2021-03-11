import logging,time, websockets, json, asyncio

from dct_business_api.base import Base



class SubscribeData(Base):

    def __init__(self, user_name, password, rest_base, ws_base):
        super(SubscribeData, self).__init__(user_name, password, rest_base, ws_base)

    def check_and_get_user_data(self, data, transaction_type, event_type, data_name):
        if data.get('transactionType') == transaction_type and data.get('eventType') == event_type:
            return data.get(data_name)

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

    async def sub_user_update(self, exchange, type, **kwargs):
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

        await self.sub_topic('USER', exchange, type, 'test=test', process_data)

    async def sub_depth(self, exchange, type, symbol, level, callback_func):
        """
        Args:
            type: 参见sub_topic
            level: 层级 5 15 20
        """
        p = f'symbol={symbol}&level={level}'
        await self.sub_topic("DEPTH", exchange, type, p, callback_func)

    async def sub_trade(self, exchange, type, symbol, callback_func):
        p = f'symbol={symbol}'
        await self.sub_topic("TRADE", exchange, type, p, callback_func)

    async def sub_book_ticker(self, exchange, type, symbol, callback_func):
        p = f'symbol={symbol}'
        await self.sub_topic("BOOK_TICKER", exchange, type, p, callback_func)

    def _insideUpdate(self, msg, cb, exch, symbol):
        ium = {}
        ium['ts'] = time.time()
        ium['ap'] = msg['marketData']['askPrice']
        ium['aq'] = msg['marketData']['askQty']
        ium['bp'] = msg['marketData']['bidPrice']
        ium['bq'] = msg['marketData']['askQty']
        ium['exch'] = exch
        ium['symbol'] = symbol
        cb(ium)

    def _tradeUpdate(self, msg, cb, exch, symbol):
        tum = {}
        tum['ts'] = time.time()
        tum['p'] = msg['marketData']['price']
        tum['q'] = msg['marketData']['quantity']
        tum['chi'] = 1 if msg['marketData']['isBuyerMaker'] else -1
        tum['exch'] = exch
        tum['symbol'] = symbol
        cb(tum)

    async def sub_topic(self, stream_name, exchange, type, extra_param_str, callback_func):
        """
        Args:
            type: 交易类型，可选值包括SPOT, USD_FUTURE, COIN_FUTURE,
        """
        access_token = self.get_access_token()
        url = f'{self.ws_base}/ws/topic?type={type}&streamName={stream_name}&exchange={exchange}&{extra_param_str}&access_token={access_token}'

        while True:
            try:
                async with websockets.connect(url) as websocket:
                    self.logger.info(url)
                    while not websocket.closed:
                        res = await websocket.recv()
                        res = json.loads(res)
                        if (callable(callback_func)):
                            if stream_name == 'BOOK_TICKER':
                                res['type'] = 'inside'
                                self._insideUpdate(res, callback_func, exchange, extra_param_str)
                            elif stream_name == 'TRADE':
                                res['type'] = 'trade'
                                self._tradeUpdate(res, callback_func, exchange, extra_param_str)
                            else:
                                res['type'] = stream_name
                                callback_func(res)
            except Exception as e:
                await asyncio.sleep(5)
                self.logger.error('connect error，try later: %s', url)
                self.logger.exception(e)