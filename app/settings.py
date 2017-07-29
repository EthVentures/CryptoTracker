import os
from dotenv import Dotenv
dotenv = Dotenv(os.path.join(os.path.dirname(__file__), ".env"))
os.environ.update(dotenv)

MARKET_REFRESH_RATE=15
ORDER_BOOK_REFRESH=60
CANDLE_REFRESH_RATE=60
RETRY_RATE=20

GDAX_API_URL = os.environ.get("GDAX_API_URL")
GEMINI_API_URL = os.environ.get("GEMINI_API_URL")

LOGLEVEL = os.environ.get("TRACKER_LOG_LEVEL")
INITIAL_SLEEP = int(os.environ.get("INITIAL_SLEEP"))

ELASTICSEARCH_CONNECT_STRING = os.environ.get("ELASTICSEARCH_CONNECT_STRING")
INITIAL_INDEX_ARRAY = ['eth.gdax.ticker','eth.gemini.ticker']
