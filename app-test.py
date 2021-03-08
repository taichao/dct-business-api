import asyncio
import logging.config
from private_params import *
from dct_business_api.dct_business_api import ApiClient, ApiConstants



def p(res):
    print(res)

async def main():
    api = ApiClient()
    sd = api.subscribe_data(user_name, password, url_base, ws_base)

    await asyncio.gather(
        sd.sub_user_update(ApiConstants.EXCHANGE_BINANCE, ApiConstants.TRANSACTION_TYPE_SPOT, on_order_update=p, on_account_update=p),
        # sd.sub_depth(ApiConstants.EXCHANGE_BINANCE, ApiConstants.TRANSACTION_TYPE_SPOT, ApiConstants.SYMBOL_BTCUSDT, 10, p),
        # sd.sub_trade(ApiConstants.EXCHANGE_BINANCE, ApiConstants.TRANSACTION_TYPE_SPOT, ApiConstants.SYMBOL_BTCUSDT, p),
        # sd.sub_book_ticker(ApiConstants.EXCHANGE_BINANCE, ApiConstants.TRANSACTION_TYPE_SPOT, ApiConstants.SYMBOL_BTCUSDT, p),

    )


if __name__ == '__main__':
    logging.config.fileConfig('config/logging.cfg', )

    asyncio.run(main())
