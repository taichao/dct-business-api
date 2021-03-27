import asyncio
import logging.config
from private_params import *
from dct_business_api import ApiClient, ApiConstants


class MDClient:
    def __init__(self,data_sub_api,handler=None):
        self.handler = handler
        self.sd = data_sub_api
    
    def set_handler(self,handler):
        self.handler = handler

    async def subscribe(self,exch,inst,level):
        if level.upper() == 'L1':
            await self.sd.sub_book_ticker(exch, ApiConstants.TRANSACTION_TYPE_SPOT,inst, self.handler.insideUpdate)
        elif level.upper() == 'T':
            await self.sd.sub_trade(exch, ApiConstants.TRANSACTION_TYPE_SPOT, inst, self.handler.tradeUpdate)
        elif level.upper() == 'USER':
            await self.sd.sub_user_update(exch, ApiConstants.TRANSACTION_TYPE_SPOT,self.handler)
        else:
            print('unknown type subscription')
    
if __name__ == '__main__':

    class MDhandler:
    
        def __init__(self):
            pass


        def insideUpdate(self,msg):
            print(msg)

        def tradeUpdate(self,msg):
            print(msg)


    async def main():
        handler = MDhandler()
        md_client = MDClient(user_name,password,url_base,ws_base,handler)
        await asyncio.gather(
            md_client.subscribe(ApiConstants.EXCHANGE_BINANCE,ApiConstants.SYMBOL_BTCUSDT,'l1'),
            md_client.subscribe(ApiConstants.EXCHANGE_BINANCE,ApiConstants.SYMBOL_BTCUSDT,'t')
        )
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
