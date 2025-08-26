from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os, json, asyncio, motor.motor_asyncio, aio_pika
from datetime import datetime

app = FastAPI(title="waitlist-svc")
client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("MONGO_URL","mongodb://localhost:27017/queueboard"))
db = client.get_default_database()

class JoinIn(BaseModel):
    business_id: str
    list_id: str
    name: str
    size: int = 1
    contact: str | None = None

@app.get("/healthz")
async def healthz():
    return {"ok": True}

async def publish(routing_key: str, payload: dict):
    conn = await aio_pika.connect_robust(os.getenv("BROKER_URL","amqp://guest:guest@localhost:5672/"))
    ch = await conn.channel()
    ex = await ch.declare_exchange("amq.topic", aio_pika.ExchangeType.TOPIC)
    await ex.publish(aio_pika.Message(body=json.dumps(payload).encode()), routing_key=routing_key)
    await conn.close()

@app.post("/join")
async def join(body: JoinIn):
    doc = body.dict() | {"status":"WAITING", "created_at": datetime.utcnow(), "position": None, "eta_minutes": None}
    res = await db.entries.insert_one(doc)
    entry_id = str(res.inserted_id)
    await publish("waitlist.joined", {"entry_id": entry_id, **body.dict()})
    return {"entry_id": entry_id, "status":"WAITING"}
