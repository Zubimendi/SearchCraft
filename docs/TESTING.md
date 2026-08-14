# Testing – SearchCraft

## Running Tests
```bash
make test
```
This runs the pytest suite inside the `web` container.

## Unit Tests
- `test_outbox.py`: Verify that the outbox trigger fires correctly on insert/update/delete.
- `test_search.py`: Verify search filters and faceting work.

## End‑to‑End Tests
We provide a script to simulate realistic scenarios:

### Breaking Things on Purpose
1. **Kill the worker** while processing a batch:
   ```bash
   docker-compose stop worker
   # create a product
   curl -X POST /api/v1/products -d '...'
   # restart worker
   docker-compose start worker
   # verify the product appears in search eventually
   ```
   The outbox rows remain unprocessed during downtime; the worker picks them up on restart.

2. **Force a race condition** – send concurrent product updates and ensure the final search state is correct (the last update wins). The outbox ensures order of processing (by `created_at`), but duplicate processing is idempotent.

3. **Test reindex with concurrent writes**:
   - Start a reindex.
   - While reindex is running, create/update a product.
   - After reindex finishes, verify that the new product appears and that alias swap didn't lose it.
   (We will have an integration test for this.)

## Test Data
`make seed` inserts 1,000 sample products with varied categories, brands, and prices.

## Performance
Load test with k6 (not included in v1) to verify latency under load.
