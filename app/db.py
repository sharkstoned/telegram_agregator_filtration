import aioredis


conn = None

async def establish_connction(params):
    global conn
    conn = await aioredis.create_redis(**params)
    return conn


async def get_votes_number(message_id):
    return await conn.scard(message_id)


async def trigger_vote(message_id, user_id):
    if await conn.sismember(message_id, user_id):
        await conn.srem(message_id, user_id)
    else:
        await conn.sadd(message_id, user_id)

    return await get_votes_number(message_id)


async def set_latest_msg_id(chat_id, message_id):
    await conn.set(f'{chat_id}:latest_msg', message_id)


async def get_latest_msg_id(chat_id):
    return await conn.get(f'{chat_id}:latest_msg')
