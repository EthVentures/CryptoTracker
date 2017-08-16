import os
from dotenv import Dotenv
dotenv = Dotenv(os.path.join(os.path.dirname(__file__), "default.env"))
os.environ.update(dotenv)

#timers in seconds
MARKET_REFRESH_RATE=1
RETRY_RATE=5
API_TIMEOUT=2

BITFINEX_API_URL = os.environ.get("BITFINEX_API_URL")
BITMEX_API_URL = os.environ.get("BITMEX_API_URL")
BITTREX_API_URL = os.environ.get("BITTREX_API_URL")
GDAX_API_URL = os.environ.get("GDAX_API_URL")
GEMINI_API_URL = os.environ.get("GEMINI_API_URL")
KRAKEN_API_URL = os.environ.get("KRAKEN_API_URL")
OKCOIN_API_URL = os.environ.get("OKCOIN_API_URL")
POLONIEX_API_URL = os.environ.get("POLONIEX_API_URL")

LOGLEVEL = os.environ.get("TRACKER_LOG_LEVEL")
INITIAL_SLEEP = int(os.environ.get("INITIAL_SLEEP"))

ELASTICSEARCH_CONNECT_STRING = os.environ.get("ELASTICSEARCH_CONNECT_STRING")
