import logging
from dct_business_api.sub_api import SubscribeData
from dct_business_api.rest_api import RestClient
from dct_business_api.base import ApiException, ApiConstants


class ApiClient:
    def __init__(self):
        self.__sub_cache = dict()
        self.__rest_cache = dict()

    def subscribe_data(self, user_name, password, rest_base, ws_base):
        if user_name in self.__sub_cache:
            sd = self.__sub_cache[user_name]
        else:
            sd = SubscribeData(user_name, password, rest_base, ws_base)
            if sd.get_access_token() is not None:
                self.__sub_cache[user_name] = sd
                logging.info('new SubscribeData')
            else:
                raise Exception('login error')
        return sd

    def rest_client(self, user_name, password, rest_base):
        if user_name in self.__rest_cache:
            rc = self.__rest_cache[user_name]
        else:
            rc = RestClient(user_name, password, rest_base)
            if rc.get_access_token() is not None:
                self.__rest_cache[user_name] = rc
                logging.info('new rest_client')
            else:
                raise Exception('login error')
        return rc
