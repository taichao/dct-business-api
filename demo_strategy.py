import asyncio
import logging.config
from private_params import *
from dct_business_api import ApiClient, ApiConstants
from MDClient import MDClient
import time

# This demo strategy is intended to test the basic logic/flow of the api
# It sends buy orders at prices 5% below the current mid at every tradeUpdate
# and cancels it immediatly at the following insideUpdate. We send 10 orders in
# total and then stop

class DemoStrategy:
    def __init__(self,md_client,ma_client):
        self._md_client = md_client
        self._ma_client = ma_client
        self._md_client.set_handler(self)
        self._mid = None
        self._pending_orders=[]
        self._total_num_order_sent = 0
    async def _start(self):
        await asyncio.gather(
            self._md_client.subscribe(ApiConstants.EXCHANGE_BINANCE,ApiConstants.SYMBOL_BTCUSDT,'l1'),
            self._md_client.subscribe(ApiConstants.EXCHANGE_BINANCE,ApiConstants.SYMBOL_BTCUSDT,'t'),
            self._md_client.subscribe(ApiConstants.EXCHANGE_BINANCE,ApiConstants.SYMBOL_BTCUSDT,'user')
        )
        
    def insideUpdate(self,msg):
        self._mid = (msg['ap'] + msg['bp'])/2
        if len(self._pending_orders) > 0:
            for oid in self._pending_orders:
                self._ma_client.cancel_order(oid)
        self._pending_orders = []

    def tradeUpdate(self,msg):
        if not self._mid:
            self._mid = 50000
        if self._total_num_order_sent < 3:
            res = self._ma_client.create_order(
                ApiConstants.EXCHANGE_BINANCE,
                ApiConstants.TRANSACTION_TYPE_SPOT,
                account_name,
                time.time(),
                ApiConstants.SYMBOL_BTCUSDT,
                ApiConstants.ORDER_SIDE_BUY,
                ApiConstants.ORDER_TYPE_LIMIT,
                ApiConstants.ORDER_TIME_IN_FORCE_GTC,
                0.0003,
                round(self._mid*0.95,2)
            )
            print('order_sent')
            self._pending_orders.append(res['orderId'])
            self._total_num_order_sent += 1
            

        print(msg)
        

    def on_account_update(self,msg):
        print('ON_ACCOUNT_UPDATE',msg.__dict__)
    
    def on_order_filled(self,msg):
        print('ON_ORDER_FILLED',msg.__dict__)
    
    def on_order_canceled(self,msg):
        print('ON_ORDER_CANCEL',msg.__dict__)

    def on_order_created(self,msg):
        print('ON_ORDER_CREATED',msg.__dict__)


if __name__ == '__main__':

    async def main():
        api = ApiClient()
        data_sub_api = api.subscribe_data(user_name, password, url_base, ws_base)
        ma_api = api.rest_client(user_name, password, url_base)

        md_client = MDClient(data_sub_api)
        strategy = DemoStrategy(md_client,ma_api)
        await strategy._start()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
