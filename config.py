import os

from dotenv import load_dotenv

load_dotenv()

DB_HOST: str = os.environ.get('DB_HOST', 'localhost')
DB_PORT: str = os.environ.get('DB_PORT', '5432')
DB_NAME: str = os.environ.get('DB_NAME', 'my_database')
DB_USER: str = os.environ.get('DB_USER', 'my_user')
DB_PASS: str = os.environ.get('DB_PASS', 'my_password')

APIKEY_CLOTHOFF: str = os.environ.get('APIKEY_CLOTHOFF', '')
PRICE_CLOT: int = os.environ.get('PRICE_CLOT', 0)
PRICE_SIMPLE: int = os.environ.get('PRICE_CLOT', 0)