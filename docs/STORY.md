# SearchCraft: Achieving Zero-Downtime, Real-Time Product Search with the Outbox Pattern

**The Problem**

E-commerce product search is notoriously hard to keep fresh. If you've ever built a marketplace or online store, you know the struggle: a merchant updates a product's price or description, but the search results still show the old data. 

Most engineering teams resort to one of two naive solutions:
1. **The Nightly Reindex:** A heavy cron job runs at 3 AM to rebuild the index from scratch. Result: new products are invisible to shoppers for hours.
2. **The Brittle Sync API:** The application layer attempts to write to the database and the search index simultaneously. Result: dual-write problems. When the database transaction commits but the search API call fails, data drifts silently.

Alternatively, teams just throw money at expensive hosted services that still don't offer the control they need.

**Our Solution**

We set out to build SearchCraft, a product search backend that **never goes stale** and guarantees consistency without sacrificing performance. The secret ingredient? The **Transactional Outbox Pattern**.

Here is how we did it:
We rely on a PostgreSQL trigger that meticulously writes every product change (INSERT, UPDATE, DELETE) into an outbox table. This happens in the exact same database transaction as the product update. If the transaction rolls back, the event disappears. If it commits, the event is guaranteed to be recorded.

A lightweight background worker continuously polls this outbox and pushes the changes to Meilisearch idempotently. The result? Products appear in search within seconds of being added or updated, with guaranteed eventual consistency.

**The Technical Highlight: Zero-Downtime Reindexing**

Keeping the data fresh is only half the battle. What happens when your business requires a new analyzer, a new facet, or a complete schema change? Rebuilding a massive index typically involves downtime.

We engineered a zero-downtime reindex solution. When a full reindex is triggered, SearchCraft creates a brand new index in Meilisearch with a unique timestamp suffix. It then quietly streams all the data from PostgreSQL into this new index in the background while the old index continues serving live traffic. Once the new index is fully primed, we atomically swap the Meilisearch alias. For the end-user, the switch is instantaneous—no dropped requests, no half-baked search results.

**Why It Matters**

This pattern—using a transactional outbox for reliable event propagation—is the same robust architecture utilized by companies like Stripe and Shopify to ensure that critical events are never lost. By building it from scratch with FastAPI, PostgreSQL, and Meilisearch, we demonstrated how to handle distributed data consistency without relying on complex, third-party messaging buses.

**Conclusion**

SearchCraft isn't just an API; it's a testament to applying advanced distributed system principles to real-world problems. We eliminated the stale-data problem that plagues e-commerce sites, implemented a bulletproof zero-downtime reindexing mechanism, and built a resilient background worker that gracefully handles failures. It proves that with the right architecture, you can achieve enterprise-grade reliability and performance using standard open-source tools.

---

## For LinkedIn

**Post Option 1 (Technical Focus)**

🚀 Just finished building **SearchCraft**, a faceted product-search API from scratch! 

One of the biggest challenges in e-commerce is keeping search results fresh. Naive cron jobs lead to stale data, while dual-writes often lead to drift and inconsistency. 

I decided to fix this by implementing the **Transactional Outbox Pattern**. Using a PostgreSQL trigger, every product update is safely written to an outbox in the exact same transaction. A lightweight async worker then polls and pushes those events to Meilisearch idempotently. Result? Search results update within seconds, with zero data loss. 

I also engineered a zero-downtime reindexing strategy utilizing atomic alias swapping. 

Built with:
🐍 FastAPI & Async Python
🐘 PostgreSQL
🔍 Meilisearch
🐳 Docker Compose

Check out the full architecture and code on my GitHub! 👇
[Link to repo]

#SoftwareEngineering #Backend #Python #FastAPI #SystemDesign #PostgreSQL

---

**Post Option 2 (Short & Punchy)**

Tired of stale search results in e-commerce apps? I built **SearchCraft** to solve exactly that. 🛠️

Using the **Transactional Outbox Pattern**, SearchCraft guarantees that any product change in the PostgreSQL database is instantly synced to the Meilisearch index within seconds. No more heavy nightly cron jobs, no more dual-write drift. 

Plus, it supports 100% zero-downtime reindexing so you can change your schema without dropping a single search query. 

Check out the repo here: [Link]

#BackendDevelopment #FastAPI #SystemArchitecture #Meilisearch
