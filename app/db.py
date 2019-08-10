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

