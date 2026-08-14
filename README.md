# SearchCraft – Faceted Search API with Live Index Sync

SearchCraft is a production-grade product search backend built with FastAPI and Meilisearch. It keeps the search index **always in sync** with your PostgreSQL database using a **database-triggered outbox** – no stale results, no scheduled periodic reindexes. It also supports **zero-downtime reindexing**, so you can change your index mapping or refresh data without interrupting search traffic.

## Quickstart

To get up and running quickly, make sure you have Docker and Docker Compose installed.

```bash
git clone <repo>
cd searchcraft
cp .env.example .env

# Start all services (PostgreSQL, Meilisearch, Web API, Background Worker)
make up

# Run database migrations to set up tables and triggers
make migrate

# Insert sample product data
make seed

# Search!
curl "http://localhost:8000/api/v1/search?q=phone&facets=category,brand"
```

## Why it's different

Most systems rely on periodic cron jobs to update their search indexes, leading to a frustrating lag between data changes and search results. SearchCraft changes the game:

- **Event-Driven Sync**: Sync is event-driven, not time-based. A PostgreSQL trigger detects changes and records them in an outbox. Changes appear in search within seconds.
- **Zero-Downtime Reindexing**: Need to change your mapping? Reindex rebuilds everything seamlessly in the background and uses an atomic alias swap to switch traffic.
- **Fully Self-Hosted**: Built completely on open-source, self-hosted infrastructure. No cloud dependencies, no vendor lock-in.

## Architecture Highlights

1. **Transactional Outbox**: We guarantee atomicity by creating an outbox event in the exact same transaction that modifies the product.
2. **Background Processing**: A resilient background worker pulls events from the outbox and idempotently syncs them to Meilisearch.
3. **Resilience & Scalability**: Built with async Python (FastAPI, asyncpg), keeping IO operations non-blocking and highly performant.

See `docs/ARCHITECTURE.md` for a deep dive into the outbox pattern, and `docs/PRD.md` for the product scope.
