import asyncio
import logging.config
from private_params import *
from dct_business_api import ApiClient, ApiConstants
from dct_business_api.handler_example import MDhandler

# U本位合约测试


def p(res):
    print(res.__dict__)

def p1(res):
    print(res)

class cb_class:
    def __init__(self):
        pass
    def on_account_update(self,msg):
        p(msg)
    def on_order_filled(self,msg):
        p(msg)
    def on_order_canceled(self,msg):
        p(msg)
    def on_order_created(self,msg):
        p(msg)
    def on_order_create_failed(self, msg):
        p(msg)



async def main():
    api = ApiClient()
    sd = api.subscribe_data(user_name, password, url_base, ws_base)
 
    md_handler = MDhandler()

    await asyncio.gather(
        sd.sub_user_update(ApiConstants.EXCHANGE_BINANCE, ApiConstants.TRANSACTION_TYPE_USD_FUTURE, cb_class()),
        # sd.sub_depth(ApiConstants.EXCHANGE_BINANCE, ApiConstants.TRANSACTION_TYPE_SPOT, ApiConstants.SYMBOL_BTCUSDT, 20, p1),
        # sd.sub_trade(ApiConstants.EXCHANGE_BINANCE, ApiConstants.TRANSACTION_TYPE_SPOT, ApiConstants.SYMBOL_BTCUSDT, p1),
        # sd.sub_trade(ApiConstants.EXCHANGE_BINANCE, ApiConstants.TRANSACTION_TYPE_SPOT, ApiConstants.SYMBOL_BTCUSDT, md_handler.tradeUpdate),
        # sd.sub_book_ticker(ApiConstants.EXCHANGE_BINANCE, ApiConstants.TRANSACTION_TYPE_SPOT, ApiConstants.SYMBOL_BTCUSDT, p1),
        # sd.sub_book_ticker(ApiConstants.EXCHANGE_BINANCE, ApiConstants.TRANSACTION_TYPE_SPOT, ApiConstants.SYMBOL_BTCUSDT, md_handler.insideUpdate),
        # sd.sub_kline(ApiConstants.EXCHANGE_BINANCE, ApiConstants.TRANSACTION_TYPE_USD_FUTURE, ApiConstants.SYMBOL_BTCUSDT, ApiConstants.KLINE_INTERVAL_MIN5, p1)

    )


if __name__ == '__main__':
    logging.config.fileConfig('config/logging.cfg', )

    asyncio.run(main())
