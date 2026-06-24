from config import MAIN_CHANNEL_ID, BACKUP_JOIN_CHANNEL_ID


async def check_channel_membership(client, user_id: int) -> dict:
    try:
        main_member = await client.get_chat_member(MAIN_CHANNEL_ID, user_id)
        backup_member = await client.get_chat_member(BACKUP_JOIN_CHANNEL_ID, user_id)
        main_joined = main_member.status not in ["left", "kicked"]
        backup_joined = backup_member.status not in ["left", "kicked"]
        return {"main": main_joined, "backup": backup_joined, "both": main_joined and backup_joined}
    except Exception:
        return {"main": False, "backup": False, "both": False}
