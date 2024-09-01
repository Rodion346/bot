import os

from dotenv import load_dotenv

load_dotenv()

DB_HOST: str = os.environ.get('DB_HOST', 'localhost')
DB_PORT: str = os.environ.get('DB_PORT', '5432')
DB_NAME: str = os.environ.get('DB_NAME', 'my_database')
DB_USER: str = os.environ.get('DB_USER', 'my_user')
DB_PASS: str = os.environ.get('DB_PASS', 'my_password')

APIKEY_CLOTHOFF: str = os.environ.get('APIKEY_CLOTHOFF', '')

BASE_REF_LINK: str = os.environ.get('BASE_REF_LINK', "")

BASE_URL_API: str = os.environ.get('BASE_URL_API', '')
TOKEN_BOT: str = os.environ.get('TOKEN_BOT', "")