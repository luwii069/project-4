# DB CONNECTION
# ENVIRONMENT VARIABLES
from datetime import datetime, timedelta

from dotenv import load_dotenv

import os

load_dotenv()

conf={
    'dbname':os.getenv('db_name'),
    'user':os.getenv('db_user'),
    'password':os.getenv('db_password'),
    'host':os.getenv('db_host'),
    'port':'6543'
}

class Config:
    SQLALCHEMY_DATABASE_URI=f"postgresql://{conf['user']}:{conf['password']}@{conf['host']}:5432/postgres"
    JWT_SECRET_KEY=os.getenv('jwt_secret_key')
    JWT_ACCESS_TOKEN_EXPIRES=timedelta(hours=20)

     #The provided code snippet demonstrates a typical 
     # setup for configuring database connection details
     #  (conf dictionary) and Flask application settings
     #  (Config class) using environment variables. 
     # It ensures secure database access and JWT token
     #  management by separating sensitive information 
     # from source code and providing flexibility for 
     # different deployment environments.