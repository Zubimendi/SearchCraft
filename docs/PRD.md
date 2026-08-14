# Product Requirements Document – SearchCraft

## Problem
E‑commerce and content platforms need product search that is:
- **Fresh** – results reflect the latest inventory and metadata.
- **Faceted** – users can filter by category, brand, price, etc.
- **Fast** – sub‑second latency.
- **Zero‑downtime** – reindexing should not take the site offline.

Most teams either:
- Periodically reindex (stale for minutes/hours),
- Use a paid hosted service,
- Or patch together brittle sync scripts.

## Users
- **Shoppers** – want relevant, current results with faceted navigation.
- **Merchants/Admins** – update products; expect changes to appear in search immediately.
- **Developers** – need a simple API to integrate search into their storefront.

## Scope (v1)
- Product data stored in PostgreSQL.
- Search index in Meilisearch.
- Synchronisation via outbox (trigger‑based) with a background worker.
- Search endpoint with text search, facet filters (category, brand, price range), pagination.
- Reindex endpoint that rebuilds the index without downtime.
- Basic product CRUD to demonstrate sync.

## Out of Scope (v1)
- Multi‑language or typo tolerance – Meilisearch handles this by default.
- Advanced analytics or personalisation.
- Complex product variants – we treat each product as a single document.
- Authentication/authorization – the API is open for MVP (but can be added later).

## Success Criteria
- A product created/updated via the API appears in search results within 5 seconds (p99).
- The reindex endpoint completes and switches traffic without returning errors during the process.
- Search latency < 200ms at 100 qps (tested via load test).
- Zero data loss during sync failures (retry and dead‑letter handled).
