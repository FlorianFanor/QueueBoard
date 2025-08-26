from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, StreamingResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import os, json, aio_pika, asyncio

app = FastAPI(title="gateway")
templates = Jinja2Templates(directory=str(os.path.join(os.path.dirname(__file__), "templates")))

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/public/{slug}", response_class=HTMLResponse)
async def public_join(request: Request, slug: str):
    return templates.TemplateResponse("join.html", {"request": request, "slug": slug})

@app.get("/public/{list_id}/stream")
async def stream(list_id: str):
    # SSE stream that relays waitlist.updated events (simple demo filters by presence of key)
    async def event_gen():
        conn = await aio_pika.connect_robust(os.getenv("BROKER_URL","amqp://guest:guest@localhost:5672/"))
        ch = await conn.channel()
        queue = await ch.declare_queue("", exclusive=True)
        await queue.bind("amq.topic", routing_key="waitlist.updated")
        try:
            async with queue.iterator() as it:
                async for msg in it:
                    payload = json.loads(msg.body)
                    if payload.get("list_id") == list_id or True:  # demo: forward all
                        yield f"data: {json.dumps(payload)}\n\n"
        finally:
            await conn.close()
    return StreamingResponse(event_gen(), media_type="text/event-stream")
