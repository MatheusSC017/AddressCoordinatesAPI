from dotenv import load_dotenv
import pymongo
import os
import jwt
import json

load_dotenv()


def create_user(name):
    mongo_uri = os.getenv("MONGO_URI").split("/")
    client = pymongo.MongoClient("/".join(mongo_uri[:-1]))
    users_collection = client[mongo_uri[-1]].users
    result = users_collection.insert_one({"user": name})
    return result.inserted_id


def get_jwt_token(user_id):
    return jwt.encode(payload={"user_id": str(user_id)}, key=os.getenv("SECRET_KEY"), algorithm="HS256")


if __name__ == "__main__":
    print("Type the name of your application: ")
    user_id = create_user(input())
    token = get_jwt_token(user_id)
    print(f"Use this token to access the API: {token}")
