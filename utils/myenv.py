from dotenv import load_dotenv
import os

load_dotenv()

ENV = {
    'SQLALCHEMY_DATABASE_URL': os.environ.get('SQLALCHEMY_DATABASE_URL'),
    'REDIS_HOST': os.environ.get('REDIS_HOST'),
    'REDIS_PORT': os.environ.get('REDIS_PORT'),
    'REDIS_PASSWORD': os.environ.get('REDIS_PASSWORD')
}

