import requests
import hmac
import operator

#Major retry
from requests.adapters import HTTPAdapter
from requests.exceptions import ConnectionError

try:
    from urllib import urlencode
# python3
except ImportError:
    from urllib.parse import urlencode

BASE_API_HOST = "https://api.bkex.com"

class BkexAPI:

    def __init__(self, secretkey, accesskey):
        self.__Secret_Key = str(secretkey)
        self.__Access_Key = str(accesskey)

    def __encryption(self, sort_data):
        signature = hmac.new(self.__Secret_Key.encode("utf-8"),sort_data.encode("utf-8"),digestmod="SHA256").hexdigest()
        return signature

    def __create_header(self, sort_data):
        signature = self.__encryption(sort_data)
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
            'Cache-Control': 'no-cache',
            "Content-Type": "application/x-www-form-urlencoded",
            "X_ACCESS_KEY": self.__Access_Key,
            "X_SIGNATURE": signature
        }
        return headers

    def __sort_dict(self, massage):
        return urlencode(dict(sorted(massage.items(), key=operator.itemgetter(0))))

    def __sign(self,method, url, params={}):
        adapter = HTTPAdapter(max_retries=3)
        res = requests.Session()
        res.mount(url, adapter)
        try:
            sort_data = self.__sort_dict(params)
            headers = self.__create_header(sort_data)
            return res.request(method, url, params=params, headers=headers, timeout=30).json()
        except Exception as e:
            return f'the error is {e}'
        except ConnectionError as ce:
            return f'connect timeout error is {ce}'

    def __get_no_sign(self, method, url, params):
        adapter = HTTPAdapter(max_retries=3)
        res = requests.Session()
        res.mount(url, adapter)
        try:
            sort_data = self.__sort_dict(params)
            headers = self.__create_header(sort_data)
            return res.request(method, url, params=sort_data or {},headers=headers, timeout=30).json()
        except Exception as e:
            return f'the error is {e}'
        except ConnectionError as ce:
            return f'connect timeout error is {ce}'

    def get_common_currencys(self,**kwargs):
        path = f'{BASE_API_HOST}/v2/common/currencys'
        return self.__get_no_sign('GET',path,params=kwargs)

    def get_common_symbols(self,**kwargs):
        path = f'{BASE_API_HOST}/v2/common/symbols'
        return self.__get_no_sign('GET',path,params=kwargs)

    def get_kline(self,**kwargs):
        path = f'{BASE_API_HOST}/v2/q/kline'
        return self.__get_no_sign('GET',path,params=kwargs)

    def get_24hr_ticker_price_change_statistics(self,**kwargs):
        path = f'{BASE_API_HOST}/v2/q/tickers'
        return self.__get_no_sign('GET',path,params=kwargs)

    def get_pair_price_ticker(self,**kwargs):
        path = f'{BASE_API_HOST}/v2/q/ticker/price'
        return self.__get_no_sign('GET',path,params=kwargs)

    def get_quotation_depth(self,**kwargs):
        path = f'{BASE_API_HOST}/v2/q/depth'
        return self.__get_no_sign('GET',path,params=kwargs)

    def get_quotation_deals(self,**kwargs):
        path = f'{BASE_API_HOST}/v2/q/deals'
        return self.__get_no_sign('GET', path, params=kwargs)


    def get_wallet_balance(self,**kwargs):
        path = f'{BASE_API_HOST}/v2/u/account/balance'
        return self.__get_no_sign('GET',path,params=kwargs)

    def post_wallet_transfer(self,**kwargs):
        path = f'{BASE_API_HOST}/v2/u/account/transfer'
        return self.__get_no_sign('POST',path,params=kwargs)


    def post_create_new_order(self,**kwargs):
        path = f'{BASE_API_HOST}/v2/u/order/create'
        return self.__sign('POST',path,params=kwargs)

    def get_all_unfinished_order(self,**kwargs):
        path = f'{BASE_API_HOST}/v2/u/order/openOrders'
        return self.__sign('GET',path,params=kwargs)

    def get_all_finished_order(self,**kwargs):
        path = f'{BASE_API_HOST}/v2/u/order/historyOrders'
        return self.__sign('GET',path,params=kwargs)

    def post_cancel_order(self,**kwargs):
        path = f'{BASE_API_HOST}/v2/u/order/cancel'
        return self.__sign('POST',path,params=kwargs)


if __name__ == "__main__":

    access_key = ""
    secret_key = ""

    start = BkexAPI(secret_key,access_key)
    print("币种信息:")
    print(start.get_common_currencys())
    print("交易对信息：")
    print(start.get_common_symbols())
    print("K线信息：")
    print(start.get_kline(symbol='BTC_USDT',period='1m',size=500))
    print("24小时行情：")
    print(start.get_24hr_ticker_price_change_statistics(symbol='BTC_USDT'))
    print("获取当前价格：")
    print(start.get_pair_price_ticker(symbol='BTC_USDT'))
    print("获取深度：")
    print(start.get_quotation_depth(symbol='BTC_USDT'))
    print("获取最新成交：")
    print(start.get_quotation_deals(symbol='BTC_USDT',size=10))
    print("获取余额信息：")
    print(start.get_wallet_balance(currencys='BTC,ETH'))
    print("创建现价单：")
    print(start.post_create_new_order(symbol="BTC_USDT",direction='BID',volume=0.1,price=1000))
    print("创建市价单：")
    print(start.post_create_new_order(symbol="BTC_USDT",direction='BID',volume=0.1,type='MARKET'))
    print("创建计划委托：")
    print(start.post_create_new_order(symbol='BTC_USDT',direction='BID',volume=0.1,price=1001,type='STOP_LIMIT',stopPrice=1000, operator='lte'))



