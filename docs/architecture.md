# QueueBoard Architecture (stub)

```mermaid
flowchart LR
  Public[Public Join Page] -->|POST /public/{slug}/join| GW[Gateway]
  GW --> WL[waitlist-svc]
  WL -->|waitlist.joined| MQ[(RabbitMQ)]
  WL -->|waitlist.updated| MQ
  MQ --> EST[estimate-svc]
  EST -->|waitlist.updated| MQ
  MQ --> GW
  MQ --> NOTIFY[notify-svc]
  NOTIFY --> Telegram
  subgraph Data
    Mongo[(MongoDB)]
  end
  WL --> Mongo
  EST --> Mongo
  GW --> Mongo
```
