import os
from dotenv import load_dotenv

load_dotenv()

FMP_URL = "https://financialmodelingprep.com/api/v3"
FMP_API_KEY = os.getenv("FMP_API_KEY")
FMP_API_KEY_POS = os.getenv("FMP_API_KEY_POS")

BING_API_KEY = os.getenv("BING_API_KEY")

KEYWORDS_POSITIVE = ["beat expectations", "strong", "growth", "record", "above estimate", "profit"]
KEYWORDS_NEGATIVE = ["missed expectations", "weak", "decline", "below estimate", "loss", "cut guidance"]

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

GOOGLE_TRENDS_API_KEY = os.getenv("GOOGLE_TRENDS_API_KEY")

GNEWS_API_KEY = os.getenv("GNEWS_API_KEY")

GNEWS_LOOKBACK_DAYS = 28

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Timeframes
DEFAULT_TIMEFRAME = 30  # days for news & forecast
LONG_TERM_TIMEFRAME = 90
SHORT_TERM_TIMEFRAME = 7

# Valuation Defaults
WACC = 0.085
TERMINAL_GROWTH = 0.025

REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_SECRET = os.getenv("REDDIT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")
REDDIT_USERNAME = os.getenv("REDDIT_USERNAME")
REDDIT_PASSWORD = os.getenv("REDDIT_PASSWORD")

# News config
NEWS_PAGE_SIZE = 10

# Satellite
SATELLITE_REFRESH_HOURS = 24  # if you cache satellite data

# FastAPI Metadata
APP_NAME = "AlphaHub Backend"
VERSION = "0.1.0"
