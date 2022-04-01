from markets import Exchange
from screener.screener import Scrapper
from utils import *
import telegram_send

class Wallet():
    def __init__(self):
        pass

    def update(self):
        raise NotImplementedError

    def get_balance(self, tick):
        raise NotImplementedError

    def telegram_update(self, scrapper):
        raise NotImplementedError
    
    def compare(self):
        raise NotImplemented

# Exchange Wallet with specific feature related to the exchange
class BinanceWallet(Wallet):
    def __init__(self, exchange:Exchange, scrapper:Scrapper, kwargs, origin):
        super().__init__()
        self.wallet_name = f'{exchange.name} wallet'
        self.exchange = exchange
        self.scrapper = scrapper
        self.total_balance = self._total_balance()
        total = self.total_balance
        self.balance_capture = total
        self.args = kwargs
        self.ref_token = kwargs['ref_token']
        usdt, eur = self.eur_spot_balance()
        self.eur_balance = eur
        self.origin_wallet = origin.wallet
        self.origin_quantity = origin.quantity

    def update(self):
        """
        Wrapper around _total_balance()
        """
        self.total_balance = self._total_balance()

    def _total_balance(self):
        """
        Updating the current balance with latest market values
        Filtering on assets that have positive quantity in your portfolio
        """
        all_balance = self.exchange.fetch_balance()
        balances = all_balance['info']['balances']
        total_balance = dict(
            [(d['asset'], (
                float(d['free']),float(self.scrapper.convert(symbol(d['asset']),
                                                             float(d['free']))               
                        )
                )) for d in balances if float(d['free']) > 0]
            )
        return total_balance

    def get_balance(self, tick):
        """ Getting balance """
        self.update()
        return self.total_balance[tick]

    def eur_spot_balance(self):
        """ Getting total balance of portfolio in euro """
        net_usdt = sum([self.total_balance[tick][1] for tick in self.total_balance.keys()])
        net_eur = self.scrapper.convert(self.ref_token, net_usdt, EUR=True)
        return net_usdt, net_eur
    
    def compare(self, tick):
            """ 
            Function to compute daily evolution of a token
            Renders a pourcentage
            """
            return (
                (self.total_balance[tick][1] - self.balance_capture[tick][1])
                /
                self.balance_capture[tick][1]
            )
    
    

