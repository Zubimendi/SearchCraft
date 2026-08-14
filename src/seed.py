import asyncio
import random
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import AsyncSessionLocal
from src.models import Product

CATEGORIES = ["Electronics", "Clothing", "Home", "Sports", "Books"]
BRANDS = ["BrandA", "BrandB", "BrandC", "TechCorp", "StyleCo"]
ADJECTIVES = ["Awesome", "Sleek", "Durable", "Portable", "Ergonomic"]
NOUNS = ["Widget", "Device", "Gadget", "Thingamajig", "Tool"]

async def seed_data():
    async with AsyncSessionLocal() as session:
        for _ in range(1000):
            product = Product(
                name=f"{random.choice(ADJECTIVES)} {random.choice(NOUNS)}",
                description="This is a generated product description.",
                price=round(random.uniform(10.0, 500.0), 2),
                category=random.choice(CATEGORIES),
                brand=random.choice(BRANDS),
                attributes={"color": "black", "weight": "1kg"}
            )
            session.add(product)
        await session.commit()
    print("Seeded 1000 products.")

def seed():
    asyncio.run(seed_data())

if __name__ == "__main__":
    seed()
