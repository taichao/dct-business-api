import logging,time, websockets, json, asyncio
from dct_business_api.sub_api_model import *

from dct_business_api.base import Base


class SubscribeData(Base):

    def __init__(self, user_name, password, rest_base, ws_base):
        super(SubscribeData, self).__init__(user_name, password, rest_base, ws_base)

    async def sub_user_update(self, exchange, type, on_account_update, on_order_created, on_order_filled, on_order_canceled, on_order_create_failed):
        def process_data(data):
            try:
                event = data.get('eventType')
                if 'ACCOUNT_UPDATE' == event and callable(on_account_update):
                    on_account_update(AccountUpdateModel(data))
                elif 'ORDER_CREATED' == event and callable(on_order_created):
                    on_order_created(OrderCreatedModel(data))
                elif 'ORDER_FILLED' == event and callable(on_order_filled):
                    on_order_filled(OrderFilledModel(data))
                elif 'ORDER_CANCELED' == event and callable(on_order_canceled):
                    on_order_canceled(OrderCanceledModel(data))
                elif 'ORDER_CREATE_FAILED' == event and callable(on_order_create_failed):
                    on_order_create_failed(OrderCreateFailedModel(data))
                else:
                    self.logger.error(f"cannot process data:{data}")

            except Exception as e:
                self.logger.error(e)

        await self.sub_topic('USER', exchange, type, 'test=placeholder', process_data)

    async def sub_kline(self, exchange, type, symbol, period, callback_func):
        p = f'symbol={symbol}&period={period}'
        await self.sub_topic("KLINE", exchange, type, p, callback_func)


    async def sub_depth(self, exchange, type, symbol, level, callback_func):
        """
        Args:
            type: 参见sub_topic
            level: 层级 5 15 20
        """
        p = f'symbol={symbol}&level={level}'
        await self.sub_topic("DEPTH", exchange, type, p, callback_func)

    async def sub_trade(self, exchange, type, symbol, callback_func):
    
        await self.sub_topic("TRADE", exchange, type, symbol, callback_func)

    async def sub_book_ticker(self, exchange, type, symbol, callback_func):
        #p = f'symbol={symbol}'
        await self.sub_topic("BOOK_TICKER", exchange, type, symbol, callback_func)

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
        if stream_name in ['BOOK_TICKER','TRADE']:
            symbol = extra_param_str
            extra_param_str = f'symbol={symbol}'    
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
                                self._insideUpdate(res, callback_func, exchange, symbol)
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
