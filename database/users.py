from datetime import datetime


class UsersDB:
    def __init__(self, db):
        self.collection = db["users"]

    async def add_user(self, user_id: int, username: str = None):
        existing = await self.collection.find_one({"user_id": user_id})
        if existing:
            return existing["_id"]
        user_data = {
            "user_id": user_id,
            "username": username,
            "joined_date": datetime.utcnow()
        }
        result = await self.collection.insert_one(user_data)
        return result.inserted_id

    async def get_user(self, user_id: int):
        return await self.collection.find_one({"user_id": user_id})

    async def get_user_count(self):
        return await self.collection.count_documents({})
