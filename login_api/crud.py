from pymongo.database import Database
import pymongo

from . import schemas

def verify_collection(db: Database, collection: str):
    if (collection in db.list_collection_names()):
        return True
    return False


def get_user(db: Database, username: str) -> schemas.UserInDB:
    if not verify_collection(db, 'users'):
        return None

    user = db['users'].find_one({'username':username})
    if(user==None):
        return None
    return schemas.UserInDB(**user)

def create_user(db: Database, user: schemas.UserInDB):
    db['users'].insert_one(dict(user.dict()))
    return True

def update_user(db: Database, user: schemas.UserInDB, data: schemas.UserUpdatingData):
    if not verify_collection(db, 'users'):
        return None

    db['users'].update_one({'username': user.username}, { "$set": { key:value for key, value in data.dict().items() if (value!=None) } } )
    return get_user(db, user.username)
