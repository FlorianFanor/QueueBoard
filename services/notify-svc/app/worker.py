import os, json, asyncio, aio_pika, httpx

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def send_telegram(to, text):
    if not BOT_TOKEN:
        print("TELEGRAM_BOT_TOKEN not set; skipping send"); return
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    async with httpx.AsyncClient(timeout=10) as client:
        try:
            r = await client.get(url, params={"chat_id": to, "text": text})
            print("telegram:", r.status_code, r.text[:120])
        except Exception as e:
            print("telegram error:", e)

async def run():
    conn = await aio_pika.connect_robust(os.getenv("BROKER_URL","amqp://guest:guest@localhost:5672/"))
    ch = await conn.channel()
    q = await ch.declare_queue("notify.send", durable=True)
    await q.bind("amq.topic", routing_key="notify.send")
    async with q.iterator() as it:
        async for msg in it:
            async with msg.process():
                payload = json.loads(msg.body)
                if payload.get("channel") == "telegram":
                    await send_telegram(payload["to"], payload["template"].format(**payload.get("params", {})))

if __name__ == "__main__":
    asyncio.run(run())
