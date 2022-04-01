import ccxt

class Exchange():
    def __init__(self, exchange_name, kwargs):
        self.name = exchange_name
        self.kwargs = kwargs
        self.exchange = kwargs["exchange"]

    def load_markets(self):
        raise NotImplementedError
    
    def fetch_ticker(self):
        raise NotImplementedError


# Specific class for Binance Market where you can specify particular function related to binance only.
# You can do the same for other exchanges too. 
class Binance(Exchange):

    def __init__(self, exchange_name, kwargs):
        self.name = exchange_name
        self.kwargs = kwargs
        self.exchange = ccxt.binance(self.kwargs)

    def load_markets(self):
        # exchange = ccxt.binance(self.kwargs)
        return self.exchange.load_markets()

    def fetch_ticker(self, tick):
        return self.exchange.fetch_ticker(tick)
