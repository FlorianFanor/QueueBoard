# QueueBoard — Waitlist & Walk‑In Manager

Services: `gateway`, `waitlist-svc`, `notify-svc`, `estimate-svc` (+ optional `audit-svc`)
Stack: Docker, FastAPI, MongoDB, RabbitMQ, Telegram

## Quickstart
```bash
cp .env.example .env
docker compose up --build
# Open: http://localhost:8080 (gateway)
# RabbitMQ UI: http://localhost:15672  (guest/guest)
```

## Make targets
```bash
make up        # build & run
make down      # stop
make seed      # (placeholder) seed demo data
```

## Repo layout
See the tree below or run `tree` locally.
