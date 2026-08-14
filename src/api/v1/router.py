from fastapi import APIRouter
from .endpoints import search, products, reindex

router = APIRouter()
router.include_router(search.router, prefix="/search", tags=["search"])
router.include_router(products.router, tags=["products"])
router.include_router(reindex.router, tags=["reindex"])
