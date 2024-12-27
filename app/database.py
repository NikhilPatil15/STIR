from pymongo import MongoClient
import os
from bson import ObjectId

def get_db_connection():
    """Connect to the MongoDB database and return the db object."""
    database_url = os.getenv('DATABASE_URL')
    client = MongoClient(database_url)
    db = client['trending_data']
    return db

# Save trending data to the database and return the inserted document as JSON
def save_trending_data(record):
    db = get_db_connection()
    collection = db['trending_data']
    
    # Insert the record into MongoDB
    response = collection.insert_one(record)
    
    # Fetch the inserted document using the _id
    inserted_document = collection.find_one({"_id": response.inserted_id})
    
    # Convert ObjectId to string for JSON serialization
    inserted_document["_id"] = str(inserted_document["_id"])
    
  
    
    return inserted_document # Return the inserted document as JSON
