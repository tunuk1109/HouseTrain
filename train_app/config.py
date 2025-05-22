from dotenv import load_dotenv
import os


load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 40
REFRESH_TOKEN_EXPIRE_DAYS = 3
