from fastapi import APIRouter, Query, Depends, HTTPException
from typing import Optional, List
from src.search import client, INDEX_NAME
from src.schemas import SearchResponse

router = APIRouter()

@router.get("")
async def search(
    q: Optional[str] = Query(None, description="Search query"),
    category: Optional[str] = Query(None, description="Filter by category"),
    brand: Optional[str] = Query(None, description="Filter by brand"),
    min_price: Optional[float] = Query(None, description="Minimum price"),
    max_price: Optional[float] = Query(None, description="Maximum price"),
    facets: Optional[str] = Query(None, description="Comma-separated list of facet fields to return (e.g., category,brand)"),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
):
    """Search products with faceted filters."""
    # Build filters for Meilisearch
    filter_conditions = []
    if category:
        filter_conditions.append(f"category = '{category}'")
    if brand:
        filter_conditions.append(f"brand = '{brand}'")
    if min_price is not None and max_price is not None:
        filter_conditions.append(f"price {min_price} TO {max_price}")
    elif min_price is not None:
        filter_conditions.append(f"price >= {min_price}")
    elif max_price is not None:
        filter_conditions.append(f"price <= {max_price}")
    filter_str = " AND ".join(filter_conditions) if filter_conditions else None

    # Facets
    facet_fields = facets.split(",") if facets else []
    # Ensure we only request facets that are filterable
    allowed_facets = ["category", "brand", "price"]  # we also support price range via filter, but facet for price as distribution? We'll handle separately.
    # Actually Meilisearch facets are for distribution counts; we'll request them if they are in allowed.
    facets_to_request = [f for f in facet_fields if f in allowed_facets]

    # Perform search
    index = client.index(INDEX_NAME)
    result = index.search(
        q or "",
        {
            "filter": filter_str,
            "facets": facets_to_request,
            "page": page,
            "hitsPerPage": per_page,
        }
    )

    # Format response
    hits = result.get("hits", [])
    total = result.get("nbHits", 0)
    facets_distribution = result.get("facetsDistribution", {})
    # Meilisearch returns facetsDistribution as dict of field->value->count

    return SearchResponse(
        hits=hits,
        total=total,
        page=page,
        per_page=per_page,
        facets=facets_distribution,
    )
