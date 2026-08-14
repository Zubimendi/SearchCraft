# Architecture – SearchCraft

This document maps the non‑negotiable principles from the playbook to this specific codebase.

## Principles Applied

### Correctness under concurrency
- **Outbox insert is atomic with product write**: The trigger runs inside the same transaction as the product INSERT/UPDATE/DELETE. If the product transaction rolls back, the outbox entry is never created – no orphaned events.
- **Idempotent outbox processing**: The worker processes each outbox row exactly once (at‑least‑once). If the worker crashes after processing but before marking `processed=True`, the next run will see the row again and re‑process it. Meilisearch `add_documents` is idempotent (same document overwrites), so duplicate processing is safe.
- **Reindex with alias swap**: The new index is built while the old one serves traffic. The alias swap is atomic – no request sees a half‑built index.

### Resilience
- **Worker retries**: On failure, the worker logs the error and continues; the outbox row remains unprocessed, so it will be retried on the next poll (with exponential backoff not implemented in v1 but easily added).
- **Graceful shutdown**: The worker catches SIGTERM and finishes the current batch before exiting (not shown in code snippet but handled in `worker.py` by `asyncio.run()` and loop cleanup).

### State and workflow
- **Explicit state machine for sync**: Outbox rows have `processed` flag. The worker transitions them to processed after successful sync. If sync fails, they remain unprocessed – the worker effectively retries.

### Data and performance
- **Index configuration**: Meilisearch is configured with filterable attributes (`category`, `brand`, `price`) to enable fast faceting.
- **Pagination** – search results are paginated to avoid large response sizes.
- **Batch processing** – outbox rows are processed in batches to reduce round trips to Meilisearch.

### Distributed and cross‑service concerns
- **Eventual consistency** – the search index is eventually consistent with the DB, but within seconds. The outbox guarantees that every change is eventually reflected.
- **Reindex as a separate process** – it runs in the background and does not block normal search traffic.

## File‑by‑file reasoning

| File | Purpose | Principle |
|------|---------|-----------|
| `src/triggers.sql` | Database trigger that inserts into outbox on product change | Correctness under concurrency (atomic within transaction) |
| `src/outbox.py` | Worker logic to fetch and process outbox rows | Resilience (retries) and state (processed flag) |
| `src/search.py` | Meilisearch client and index setup | Performance (filterable attributes) |
| `src/reindex.py` | Zero‑downtime reindex | Distributed (alias swap) |
| `src/api/v1/endpoints/search.py` | Search endpoint with facets | Performance (pagination, filters) |
| `src/worker.py` | Background worker loop | Resilience (crash recovery) |

## Deliberate Simplifications for v1
- **No dead‑letter queue** – if a row fails repeatedly, it stays unprocessed. In production we’d add a DLQ or manual intervention.
- **No monitoring / alerting** – logs are the only observability. We’d add metrics (e.g., Prometheus) later.
- **Worker uses polling** (every 2s) – acceptable for MVP; could be replaced by `LISTEN/NOTIFY` for lower latency.
- **Reindex uses same filterable attributes** – in production we’d allow dynamic mapping.
