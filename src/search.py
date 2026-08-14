import meilisearch
from .config import settings

client = meilisearch.Client(settings.MEILISEARCH_URL, settings.MEILISEARCH_API_KEY)
INDEX_NAME = "products"  # alias

def ensure_index():
    """Create index if it doesn't exist, set up filterable attributes for facets."""
    try:
        index = client.index(INDEX_NAME)
        # index stats to check existence
        client.get_index(INDEX_NAME)
    except meilisearch.errors.MeilisearchApiError:
        # create index
        client.create_index(INDEX_NAME, {"primaryKey": "id"})
    # Configure filterable attributes for faceting
    index = client.index(INDEX_NAME)
    index.update_filterable_attributes(["category", "brand", "price"])  # price for range
    # Also set sortable attributes if needed
    index.update_sortable_attributes(["price", "name"])
