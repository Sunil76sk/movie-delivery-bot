from datetime import datetime


class MoviesDB:
    def __init__(self, db):
        self.collection = db["movies"]

    async def add_movie(self, movie_data: dict):
        movie_data["created_at"] = datetime.utcnow()
        movie_data["views"] = 0
        movie_data["downloads"] = 0
        result = await self.collection.insert_one(movie_data)
        return result.inserted_id

    async def get_movie(self, movie_id: str):
        return await self.collection.find_one({"_id": movie_id})

    async def get_movie_by_file_unique_id(self, file_unique_id: str):
        return await self.collection.find_one({"file_unique_id": file_unique_id})

    async def get_all_movies(self, limit: int = 50, skip: int = 0):
        cursor = self.collection.find().sort("created_at", -1).skip(skip).limit(limit)
        return await cursor.to_list(length=limit)

    async def search_movies(self, query: str, limit: int = 20):
        cursor = self.collection.find(
            {"$text": {"$search": query}}
        ).limit(limit)
        return await cursor.to_list(length=limit)

    async def increment_views(self, movie_id: str):
        await self.collection.update_one(
            {"_id": movie_id},
            {"$inc": {"views": 1}}
        )

    async def increment_downloads(self, movie_id: str):
        await self.collection.update_one(
            {"_id": movie_id},
            {"$inc": {"downloads": 1}}
        )

    async def delete_movie(self, movie_id: str):
        return await self.collection.delete_one({"_id": movie_id})

    async def get_movie_count(self):
        return await self.collection.count_documents({})
