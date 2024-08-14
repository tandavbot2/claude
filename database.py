from pymongo import MongoClient
from pymongo.errors import PyMongoError
from configs import cfg
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    client = MongoClient(cfg.MONGO_URI)
    db = client['main']
    users = db['users']
    groups = db['groups']
    logger.info("Successfully connected to MongoDB")
except PyMongoError as e:
    logger.error(f"Error connecting to MongoDB: {e}")
    raise

def already_db(user_id):
    try:
        user = users.find_one({"user_id": str(user_id)})
        return user is not None
    except PyMongoError as e:
        logger.error(f"Error checking user existence: {e}")
        return False

def already_dbg(chat_id):
    try:
        group = groups.find_one({"chat_id": str(chat_id)})
        return group is not None
    except PyMongoError as e:
        logger.error(f"Error checking group existence: {e}")
        return False

def add_user(user_id):
    try:
        if not already_db(user_id):
            users.insert_one({"user_id": str(user_id)})
            logger.info(f"User {user_id} added to database")
    except PyMongoError as e:
        logger.error(f"Error adding user: {e}")

def remove_user(user_id):
    try:
        if already_db(user_id):
            users.delete_one({"user_id": str(user_id)})
            logger.info(f"User {user_id} removed from database")
    except PyMongoError as e:
        logger.error(f"Error removing user: {e}")

def add_group(chat_id):
    try:
        if not already_dbg(chat_id):
            groups.insert_one({"chat_id": str(chat_id)})
            logger.info(f"Group {chat_id} added to database")
    except PyMongoError as e:
        logger.error(f"Error adding group: {e}")

def all_users():
    try:
        return users.count_documents({})
    except PyMongoError as e:
        logger.error(f"Error counting users: {e}")
        return 0

def all_groups():
    try:
        return groups.count_documents({})
    except PyMongoError as e:
        logger.error(f"Error counting groups: {e}")
        return 0

def get_all_users():
    try:
        return list(users.find({}, {"_id": 0, "user_id": 1}))
    except PyMongoError as e:
        logger.error(f"Error fetching all users: {e}")
        return []

def get_all_groups():
    try:
        return list(groups.find({}, {"_id": 0, "chat_id": 1}))
    except PyMongoError as e:
        logger.error(f"Error fetching all groups: {e}")
        return []

def update_user_data(user_id, data):
    try:
        users.update_one({"user_id": str(user_id)}, {"$set": data}, upsert=True)
        logger.info(f"User data updated for {user_id}")
    except PyMongoError as e:
        logger.error(f"Error updating user data: {e}")

def get_user_data(user_id):
    try:
        return users.find_one({"user_id": str(user_id)})
    except PyMongoError as e:
        logger.error(f"Error fetching user data: {e}")
        return None
