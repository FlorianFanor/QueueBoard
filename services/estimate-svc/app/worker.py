import os, json, asyncio, aio_pika, motor.motor_asyncio
from datetime import datetime

MONGO_URL = os.getenv("MONGO_URL","mongodb://localhost:27017/queueboard")

async def run():
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
    db = client.get_default_database()
    conn = await aio_pika.connect_robust(os.getenv("BROKER_URL","amqp://guest:guest@localhost:5672/"))
    ch = await conn.channel()
    ex = await ch.declare_exchange("amq.topic", aio_pika.ExchangeType.TOPIC)
    q = await ch.declare_queue("", exclusive=True)
    await q.bind("amq.topic", routing_key="waitlist.updated")
    async with q.iterator() as it:
        async for msg in it:
            async with msg.process():
                payload = json.loads(msg.body)
                # naive ETA: position * average_cycle_minutes (default 5)
                avg = 5
                eta = (payload.get("position") or 0) * avg
                out = {**payload, "eta_minutes": eta, "at": datetime.utcnow().isoformat()}
                await ex.publish(aio_pika.Message(body=json.dumps(out).encode()), routing_key="waitlist.updated")
                print("eta updated:", out)

if __name__ == "__main__":
    asyncio.run(run())
