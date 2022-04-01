from markets import Binance, Exchange
from account import BinanceWallet, Wallet
from message.message import Messager
from origin.origin import Origin_wallet
from screener import BinanceScrapper, Scrapper

# File reaching to the specific objects necessary to meet requirements from your configuration file.

def get_exchange(exchange: str, market_kwargs: dict):

    if exchange=="binance":
        return Binance(exchange, market_kwargs)

    # elif exhange == "exchange you want"
    else:
        raise NotImplementedError(f'{exchange} not supported yet')

def get_wallet(exchange: Exchange, scrapper:Scrapper, config, origin):
    if exchange.name=="binance":
        return BinanceWallet(exchange.exchange, scrapper, config, origin)
    else:
        raise NotImplementedError(f'{exchange} not supported yet')

def get_scrapper(exchange: Exchange, config):
    if exchange.name=="binance":
        return BinanceScrapper(exchange.exchange, config)
    else:
        raise NotImplementedError(f'{exchange} not supported yet')

def get_messager(exchange: Exchange, wallet:Wallet, scrapper:Scrapper):
    return Messager(exchange, wallet, scrapper)

def get_origin_wallet(origin_wallet: Origin_wallet):
    return Origin_wallet(origin_wallet)