import telegram_send
from account.account import Wallet
from markets.markets import Exchange
from screener.screener import Scrapper
from utils import symbol

class Messager():
    def __init__(self, exchange:Exchange, wallet:Wallet, scrapper:Scrapper):
        self.exchange = exchange.exchange
        self.scrapper = scrapper 
        self.wallet = wallet
    
    def daily_update(self):
        """
        Function formating a message to report daily updates on
        your portfolio via telegram. It is basic but can easily be tweaked.
        """
        # Update portfolio with latest values
        self.wallet.update()
        total_balance = self.wallet.total_balance

        # Text message init
        s = "Your daily portofolio updates: \n \n"
        for tick in total_balance:

            # Checking if the token "tick" was in portfolio yesterday
            if tick in self.wallet.balance_capture:

                change = round(self.wallet.compare(tick)*100,3)

                s += f"{tick} : Since yesterday : {change}% to {round(total_balance[tick][1],2)} {self.wallet.ref_token}\n"
                
                # Little loop to compare with original investment
                if tick in self.wallet.origin_wallet.keys():

                    origin_list = self.wallet.origin_wallet[tick]
                    for origin in origin_list:
                        origin_change = round(((self.exchange.fetch_ticker(symbol(tick))['last'] - origin)/origin)*100, 2)
                        s += f"{tick} : Since origin : {origin_change}% from {round(origin, 2)} {self.wallet.ref_token}\n"

            # Otherwise token was just added
            else:
                s.append(f"{tick} newly added")

        self.wallet.balance_capture = total_balance
        s += "\n"

        # Total balance of portfolio
        _, eur = self.wallet.eur_spot_balance()
        s += f"Total balance is {round(eur,2)}€"
        self.wallet.eur_balance = eur

        # Sending message
        telegram_send.send(messages=[s])
