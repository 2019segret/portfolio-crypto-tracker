from email.policy import default
from numpy import empty
import pandas as pd
import click
import importlib
import warnings
import os
import schedule
import shutil
import time
from datetime import datetime
import telegram_send
from utils import *
from getters import get_exchange, get_messager, get_scrapper, get_wallet, get_origin_wallet


pd.set_option('display.max_rows', None)
warnings.filterwarnings('ignore')

@click.command()
@click.option('-c', '--config', type=click.Path(exists=True))
@click.option('-s', '--save', is_flag=True)
def launcher(config, save):
    
    # Load config as dict
    config_path = config
    config_module_name = os.path.splitext(config)[0].replace('/', '.')
    config = importlib.import_module(config_module_name).config

    model_dir = config["models"]

    if save:
        if not os.path.exists(model_dir):
            os.makedirs(model_dir)
        timestamp = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        shutil.copy(config_path, f'{model_dir}/config_{config["savename"]}_{timestamp}.py')


    main(config)
        

def main(config):
    # -- Connecting to exchange
    print(f'Connecting to {config["exchange"]} ...')
    Exchange = get_exchange(config['exchange'], config["exchange_kwargs"])
    exchange = Exchange.exchange
    markets = Exchange.load_markets()
    # exchange.verbose = True  # uncomment for debugging
    print(f'Connected to {config["exchange"]}')

    # -- Get Scrapper to fetch data
    scrapper = get_scrapper(Exchange, config)
    
    # -- Creating origin wallet instance
    origin_path = config["origin_wallet_path"]
    if origin_path != None:
        origin_module_name = os.path.splitext(origin_path)[0].replace('/', '.')
        origin = importlib.import_module(origin_module_name).origin_wallet
        origin_wallet = get_origin_wallet(origin)
 
    else:
        origin_wallet = {}

    # -- Creating wallet instance
    wallet = get_wallet(Exchange, scrapper, config, origin_wallet)
    
    # -- Creating messager instance
    messager = get_messager(Exchange, wallet, scrapper)

    # -- Reference token for conversion
    ref_token = config["ref_token"]

    # -- Defining Schedulers to run periodical updates
    scheduler_daily = schedule.Scheduler()
    scheduler_daily.every().day.at("17:00").do(messager.daily_update)

    while True:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        start = '08:20:00'
        end = '23:30:00'
        if current_time > start and current_time < end:
            scheduler_daily.run_pending()
            time.sleep(10)


        
if __name__ == "__main__":
    launcher()
