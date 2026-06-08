import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env")

CHANNEL_ACCESS_TOKEN = os.environ["CHANNEL_ACCESS_TOKEN"]
CHANNEL_SECRET = os.environ["CHANNEL_SECRET"]
MOTC_API = os.environ.get("MOTC_API", "")
TIMEZONE = os.environ.get("TIMEZONE", "Etc/GMT-8")
MYGO_BASE_URL = os.environ.get("MYGO_BASE_URL", "")

DATA_DIR = BASE_DIR / "data"
