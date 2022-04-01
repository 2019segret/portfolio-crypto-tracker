from ast import Not
import datetime
from this import d
from time import time
from markets import Exchange
import origin
from origin.origin import Origin_wallet
import utils
from utils import drop_message, symbol
import telegram_send

class Scrapper():
    def __init__(self):
        super().__init__()

    def pct_change(self, symbol):
        raise NotImplementedError
    
    def convert(self, symbol, amount):
        raise NotImplementedError

    def pct_ptf(self):
        raise NotImplementedError
    
class BinanceScrapper(Scrapper):
    def __init__(self, exchange:Exchange, config):
        super().__init__()
        self.exchange = exchange
        self.ref_token = config["ref_token"]
        self.watch_list = config["watch_list"]

    def pct_change(self, symbol):
        return self.exchange.fetch_ticker(symbol)["percentage"]

    def convert(self, symbol, amount, EUR=False):
        """
        Convert the value of an asset in USDT, in EUR if set to True
        """
        if EUR:
            symbol = f"EUR/{symbol}"
            return amount/self.exchange.fetch_ticker(symbol)['last']
        if symbol==utils.symbol(self.ref_token):
            return amount
        return amount*self.exchange.fetch_ticker(symbol)['last']
    
    def pct_ptf(self, wallet, val):
        """
        Renders a dict containing (key, value): (tick, [% change since yesterday, position in origin dict list from origin.py])
        Only compares on asset that are in the origin.py dict, where all your investments are supposed to be.
        """
        var = {}
        for tick in wallet.origin_wallet.keys():
            origin_list = wallet.origin_wallet[tick]
            count = 0
            for origin in origin_list:
                change = round(((self.exchange.fetch_ticker(symbol(tick))['last'] - origin)/origin)*100, 2)
                if change > val:
                    var[tick] = (change, count)
                count+=1
        return var
    
