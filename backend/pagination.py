"""Helper functions for pagination logic."""

from .models import get_all_site


def get_paginated_articles(page: int, limit: int):
    """Return paginate artics and pagination info.."""
    articles = get_all_site()
    total_articles = len(articles)
    total_pages = (total_articles + limit - 1) // limit

    start = (page - 1) * limit
    end = start + limit
    paginated_articles = articles[start:end]

    return paginated_articles, total_pages
