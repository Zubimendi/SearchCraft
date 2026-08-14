import asyncio
from sqlalchemy import select
from .database import AsyncSessionLocal
from .models import Product
from .search import client, INDEX_NAME

async def reindex(progress_callback=None):
    """Reindex all products into a new index, then swap alias."""
    # 1. Create a new index with a timestamp suffix
    import time
    suffix = int(time.time())
    new_index_name = f"products_v{suffix}"
    client.create_index(new_index_name, {"primaryKey": "id"})
    new_index = client.index(new_index_name)
    # Configure filterable attributes
    new_index.update_filterable_attributes(["category", "brand", "price"])
    new_index.update_sortable_attributes(["price", "name"])

    # 2. Fetch all products from DB in chunks
    async with AsyncSessionLocal() as session:
        stmt = select(Product)
        result = await session.execute(stmt)
        products = result.scalars().all()
        total = len(products)

        batch_size = 100
        for i in range(0, total, batch_size):
            batch = products[i:i+batch_size]
            docs = []
            for p in batch:
                docs.append({
                    "id": str(p.id),
                    "name": p.name,
                    "description": p.description,
                    "price": p.price,
                    "category": p.category,
                    "brand": p.brand,
                    "attributes": p.attributes,
                })
            new_index.add_documents(docs)
            if progress_callback:
                progress_callback(i+batch_size, total)

    # 3. Atomically swap the new index into the canonical "products" index.
    # swap_indexes swaps the contents of both indexes in place, so "products"
    # now holds the freshly-built data and the temp index holds the old data.
    client.swap_indexes([{"indexes": [INDEX_NAME, new_index_name]}])

    # 4. Delete the stale temp index that now contains the old data.
    client.delete_index(new_index_name)

    return new_index_name
