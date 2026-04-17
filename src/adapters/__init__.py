from typing import Any
from math import ceil

def get_pagination(
        items: list[dict[str, Any]] | list[None], 
        items_count: int | None, 
        page: int = 1, 
        rows_per_page: int = 10
    ) -> dict[str, Any]:
    next_page = None
    prev_page = None
    pages_count = None

    if items_count is not None:
        
        pages_count = ceil(items_count/rows_per_page)

        if page < pages_count:
            next_page = page + 1

        if page > 1:
            prev_page = page - 1
   
    pagination = {
        'pages_count': pages_count,
        'items_count': items_count,
        'items_per_page': rows_per_page,
        'prev': prev_page,
        'prox': next_page,
        'current': page
    }
    return {
        "items": items,
        'pagination': pagination
    }
