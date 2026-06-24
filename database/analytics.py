from datetime import datetime


class AnalyticsDB:
    def __init__(self, db):
        self.collection = db["analytics"]
        self.downloads_collection = db["downloads"]

    async def track_view(self, movie_id: str, user_id: int):
        await self.collection.update_one(
            {"movie_id": movie_id, "type": "view"},
            {
                "$inc": {"count": 1},
                "$addToSet": {"unique_users": user_id},
                "$setOnInsert": {"created_at": datetime.utcnow()}
            },
            upsert=True
        )

    async def track_download(self, movie_id: str, user_id: int):
        download_data = {
            "user_id": user_id,
            "movie_id": movie_id,
            "timestamp": datetime.utcnow()
        }
        await self.downloads_collection.insert_one(download_data)

        await self.collection.update_one(
            {"movie_id": movie_id, "type": "download"},
            {
                "$inc": {"count": 1},
                "$addToSet": {"unique_users": user_id},
                "$setOnInsert": {"created_at": datetime.utcnow()}
            },
            upsert=True
        )

    async def get_movie_analytics(self, movie_id: str):
        views = await self.collection.find_one(
            {"movie_id": movie_id, "type": "view"}
        )
        downloads = await self.collection.find_one(
            {"movie_id": movie_id, "type": "download"}
        )
        
        return {
            "views": views["count"] if views else 0,
            "unique_views": len(views.get("unique_users", [])) if views else 0,
            "downloads": downloads["count"] if downloads else 0,
            "unique_downloads": len(downloads.get("unique_users", [])) if downloads else 0
        }

    async def get_total_analytics(self):
        views_pipeline = [
            {"$match": {"type": "view"}},
            {"$group": {"_id": None, "total": {"$sum": "$count"}}}
        ]
        downloads_pipeline = [
            {"$match": {"type": "download"}},
            {"$group": {"_id": None, "total": {"$sum": "$count"}}}
        ]
        
        views_result = await self.collection.aggregate(views_pipeline).to_list(1)
        downloads_result = await self.collection.aggregate(downloads_pipeline).to_list(1)
        
        return {
            "total_views": views_result[0]["total"] if views_result else 0,
            "total_downloads": downloads_result[0]["total"] if downloads_result else 0
        }

    async def get_recent_downloads(self, limit: int = 10):
        cursor = self.downloads_collection.find().sort("timestamp", -1).limit(limit)
        return await cursor.to_list(length=limit)
