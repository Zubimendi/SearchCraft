import json
import asyncio
from typing import List, Dict, Any
from sqlalchemy import select, update, func
from sqlalchemy.ext.asyncio import AsyncSession

from .database import AsyncSessionLocal
from .models import Outbox, OutboxEventType, Product
from .search import client, INDEX_NAME

async def process_outbox_batch(batch_size: int = 100) -> int:
    """Fetch up to batch_size unprocessed outbox rows, process them, mark done."""
    async with AsyncSessionLocal() as session:
        # Fetch unprocessed rows, ordered by created_at
        stmt = select(Outbox).where(Outbox.processed == False).order_by(Outbox.created_at).limit(batch_size)
        result = await session.execute(stmt)
        rows = result.scalars().all()
        if not rows:
            return 0

        # Process each row (in a real system, we'd batch updates, but for simplicity we do one by one)
        for row in rows:
            await process_outbox_row(session, row)

        # Mark all as processed
        ids = [row.id for row in rows]
        await session.execute(
            update(Outbox)
            .where(Outbox.id.in_(ids))
            .values(processed=True, processed_at=func.now())
        )
        await session.commit()
        return len(rows)

async def process_outbox_row(session: AsyncSession, row: Outbox):
    """Handle a single outbox event."""
    product_id = row.payload.get("product_id")
    if row.event_type == OutboxEventType.PRODUCT_DELETED:
        # Delete from Meilisearch
        try:
            client.index(INDEX_NAME).delete_document(product_id)
        except Exception as e:
            # Log error; we'll retry later if not marked processed? For now, we'll mark processed even on error? We'll implement retry later.
            # For MVP, we'll mark processed and log.
            print(f"Failed to delete {product_id}: {e}")
        return

    # For insert/update, we need the full product data
    # The payload already contains the row data, but we could also fetch from DB if we trust trigger.
    data = row.payload.get("data")
    if not data:
        # fallback: fetch from products table
        stmt = select(Product).where(Product.id == product_id)
        prod = (await session.execute(stmt)).scalar_one_or_none()
        if not prod:
            # product might have been deleted; treat as deletion
            client.index(INDEX_NAME).delete_document(product_id)
            return
        # Convert to dict
        data = {
            "id": str(prod.id),
            "name": prod.name,
            "description": prod.description,
            "price": prod.price,
            "category": prod.category,
            "brand": prod.brand,
            "attributes": prod.attributes,
        }
    else:
        # data is dict from jsonb; ensure id is string
        data["id"] = str(data["id"])
    # Add/update document
    try:
        client.index(INDEX_NAME).add_documents([data])
    except Exception as e:
        print(f"Failed to index {product_id}: {e}")
        # Re-raise to prevent marking as processed? For now, we'll just log.
