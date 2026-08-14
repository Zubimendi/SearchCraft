# Cursor / Agent Context – SearchCraft

## What’s Done
- Full codebase (FastAPI, SQLAlchemy async, Meilisearch, worker).
- Docker Compose setup with web, worker, postgres, meilisearch.
- Outbox triggers on `products` table.
- Worker processes outbox rows and updates Meilisearch.
- Search endpoint with filters and facets.
- Reindex endpoint with background task and alias swap.
- All five required documents.

## What’s NOT Done (and why)
- **Dead‑letter queue**: not needed for MVP; in production we’d add one.
- **Monitoring / metrics**: not implemented to keep code focused; can be added later.
- **Authentication**: omitted because MVP is open; a real deployment would add JWT or OAuth2.
- **Advanced error handling**: worker logs errors but does not implement exponential backoff – easily added.
- **Full test suite**: only basic unit tests; integration tests for reindex are stubbed.

## Design Decisions Already Made
- Polling interval = 2s – good for MVP; could use `LISTEN/NOTIFY` for lower latency.
- Meilisearch as search engine – chosen for ease of setup and robust faceting.
- Async SQLAlchemy – to keep web endpoints non‑blocking.
- Outbox rows are processed in batches of 100 to balance throughput.

## Next Steps (Prioritized)
1. Add exponential backoff to worker retries.
2. Implement a dead‑letter queue for permanently failing rows.
3. Add Prometheus metrics (e.g., outbox lag, reindex duration).
4. Write comprehensive integration tests for reindex with concurrent writes.
5. Add caching layer (Redis) for frequent search queries to reduce load on Meilisearch.

## How to Resume
To continue development, run `make up` and use the existing code. If you need to modify the outbox schema, ensure migrations are applied. The worker runs in a separate container – you can restart it with `docker-compose restart worker`.
