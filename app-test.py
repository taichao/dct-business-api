import asyncio
import logging.config
from private_params import *
from dct_business_api import ApiClient, ApiConstants
from dct_business_api.handler_example import MDhandler


def p(res):
    print(res.__dict__)

def p1(res):
    print(res)


async def main():
    api = ApiClient()
    sd = api.subscribe_data(user_name, password, url_base, ws_base)
 
    md_handler = MDhandler()

    await asyncio.gather(
        sd.sub_user_update(ApiConstants.EXCHANGE_BINANCE, ApiConstants.TRANSACTION_TYPE_SPOT,
                           on_account_update=p,
                           on_order_filled=p,
                           on_order_canceled=p,
                           on_order_created=p),
        # sd.sub_depth(ApiConstants.EXCHANGE_BINANCE, ApiConstants.TRANSACTION_TYPE_SPOT, ApiConstants.SYMBOL_BTCUSDT, 20, p1),
        # sd.sub_trade(ApiConstants.EXCHANGE_BINANCE, ApiConstants.TRANSACTION_TYPE_SPOT, ApiConstants.SYMBOL_BTCUSDT, p1),
        # sd.sub_trade(ApiConstants.EXCHANGE_BINANCE, ApiConstants.TRANSACTION_TYPE_SPOT, ApiConstants.SYMBOL_BTCUSDT, md_handler.tradeUpdate),
        # sd.sub_book_ticker(ApiConstants.EXCHANGE_BINANCE, ApiConstants.TRANSACTION_TYPE_SPOT, ApiConstants.SYMBOL_BTCUSDT, p1),
        # sd.sub_book_ticker(ApiConstants.EXCHANGE_BINANCE, ApiConstants.TRANSACTION_TYPE_SPOT, ApiConstants.SYMBOL_BTCUSDT, md_handler.insideUpdate),

    )


if __name__ == '__main__':
    logging.config.fileConfig('config/logging.cfg', )

    asyncio.run(main())
