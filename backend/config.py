import os
from dotenv import find_dotenv, load_dotenv

# set enviroment variable
# find_dotenv():    returns absolute path of first
#                   .env file found recursively going to higher directories
load_dotenv(dotenv_path=find_dotenv())

SECRET_KEY = str(os.getenv("SECRET_KEY"))
ALGORITHM = str(os.getenv("ALGORITHM"))
ACCESS_TOKEN_EXPIRE_MINUTES = float(str(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))
