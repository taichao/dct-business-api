import logging
import requests
from datetime import *


class Base:
    def __init__(self, user_name, password, rest_base, ws_base):
        self.user_name = user_name
        self.password = password
        self.rest_base = rest_base
        self.ws_base = ws_base
        self.access_token = None
        self.expire_time = None
        self.logger = logging.getLogger("dct_business_api")

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


class ApiConstants:
    # 币安现货
    EXCH_BINA = "bina"

    EXCHANGE_BINANCE = 'BINANCE'

    SYMBOL_BTCUSDT = 'BTC/USDT'

    TRANSACTION_TYPE_SPOT = 'SPOT'
    TRANSACTION_TYPE_USD_FUTURE = 'USD_FUTURE'
    TRANSACTION_TYPE_COIN_FUTURE = 'COIN_FUTURE'

    ORDER_SIDE_BUY = 'BUY'
    ORDER_SIDE_SELL = 'SELL'
    ORDER_TYPE_LIMIT = 'LIMIT'
    ORDER_TIME_IN_FORCE_GTC = 'GTC'
    ORDER_TIME_IN_FORCE_IOC = 'IOC'

    KLINE_INTERVAL_MIN5 = "MIN5"


class ApiException(Exception):
    SUCCESS = 'success'
    PARAM_ERROR = 'param_error'
    # 调用交易所api异常
    PLATFORM_API_BUSINESS_ERROR = 'platform_api_business_error'
    # 未知异常，联系服务提供者
    RUNTIME_ERROR = 'runtime_error'
    # 订单不支持取消
    ORDER_DELETE_NOT_SUPPORTED = 'order_delete_not_supported'

    def __init__(self, response):
        # 关键字段，可做逻辑判断使用
        self.code = response.get('code', 'unknown')
        # 具体错误信息展示
        self.message = response.get('message', 'unknown')
        # 仅供debug使用，不可用作逻辑判断
        self.extra = response.get('extra', 'unknown')
        self.data = response.get('data', '')

    def __str__(self):
        return f'code={self.code} message={self.message} extra={self.extra}'
