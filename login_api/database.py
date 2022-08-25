import os
from dotenv import load_dotenv # pymongo.database.Database
import pymongo

"""
    docker run --name database -d -p 27017:27017 mongo
"""

load_dotenv()

DATABASE_IP = os.getenv('DATABASE_IP')
DATABASE_PORT = os.getenv('DATABASE_PORT')

myclient = pymongo.MongoClient(f'mongodb://{DATABASE_IP}:{DATABASE_PORT}/')
db = myclient['users']
