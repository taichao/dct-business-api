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
        sd.sub_user_update(ApiConstants.TRANSACTION_TYPE_SPOT, on_order_update=p, on_account_update=p),
        sd.sub_depth(ApiConstants.TRANSACTION_TYPE_SPOT, "BTCUSDT", 10, p),
        sd.sub_trade(ApiConstants.TRANSACTION_TYPE_SPOT, 'BTCUSDT', None),
        sd.sub_book_ticker(ApiConstants.TRANSACTION_TYPE_SPOT, 'btcusdt', None)

    )


if __name__ == '__main__':
    logging.config.fileConfig('config/logging.cfg', )

    asyncio.run(main())
