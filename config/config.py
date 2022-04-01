# This is where you need to import you keys
# For instance, add a .env file that you import here
#In the import keys is supposed to be a dictionnary containing your public and secret keys
from wherever_you_want import keys

config = {
    "savename": "main", # Prefix of saved models
    "models": 'models', # Path to models that need to be saved
    "exchange": "binance",
    "exchange_kwargs": dict(
        apiKey= keys["BINANCE_API_KEY"],
        secret= keys["BINANCE_SECRET_KEY"],
        enableRateLimit= True,
    ),
    "ref_token": "USDT", # Computations are based on that token
    "watch_list": ["BTC/USDT",
                   "ETH/USDT",
                   "SOL/USDT",
                   "AVAX/USDT",
                   "GLMR/USDT",
                   "MANA/USDT"
                   ],
    "origin_wallet_path": "origin/original.py", # Path or None if no orogin_wallet
    "gain_val": 4,
}
