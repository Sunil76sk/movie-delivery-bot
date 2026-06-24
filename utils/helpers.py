def format_file_size(size_bytes: int) -> str:
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 ** 2:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 ** 3:
        return f"{size_bytes / (1024 ** 2):.1f} MB"
    else:
        return f"{size_bytes / (1024 ** 3):.1f} GB"


def create_movie_caption(movie_data: dict) -> str:
    caption = f"🎬 **{movie_data.get('title', 'Unknown')}**\n\n"
    caption += f"⭐ Rating: {movie_data.get('rating', 'N/A')}/10\n"
    caption += f"🗣️ Language: {movie_data.get('language', 'N/A')}\n"
    caption += f"📅 Year: {movie_data.get('year', 'N/A')}\n"
    caption += f"🎭 Genre: {movie_data.get('genre', 'N/A')}\n"
    caption += f"📂 Size: {movie_data.get('file_size', 'N/A')}\n"
    return caption


def generate_short_url(long_url: str, api_key: str, api_url: str) -> str:
    import aiohttp
    import asyncio

    async def shorten():
        async with aiohttp.ClientSession() as session:
            params = {"api": api_key, "url": long_url}
            async with session.get(api_url, params=params) as resp:
                data = await resp.json()
                return data.get("shortenedUrl", long_url)
    
    return asyncio.get_event_loop().run_until_complete(shorten())
