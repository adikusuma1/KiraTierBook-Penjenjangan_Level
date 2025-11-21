import requests
from typing import Optional, Dict, List


def search_book_metadata(query: str) -> Optional[Dict]:
    try:
        url = f"https://www.googleapis.com/books/v1/volumes?q={query}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if 'items' not in data or len(data['items']) == 0:
            return None
        book_item = data['items'][0]
        volume_info = book_item.get('volumeInfo', {})
        title = volume_info.get('title', 'Unknown Title')
        authors = volume_info.get('authors', [])
        page_count = volume_info.get('pageCount')
        categories = volume_info.get('categories', [])
        preview_link = volume_info.get('previewLink', '')
        thumbnail = volume_info.get('imageLinks', {}).get('thumbnail', '')
        return {
            'title': title,
            'authors': authors,
            'page_count': page_count,
            'categories': categories,
            'preview_link': preview_link,
            'thumbnail': thumbnail
        }
    except requests.exceptions.RequestException:
        return None
    except (KeyError, TypeError):
        return None