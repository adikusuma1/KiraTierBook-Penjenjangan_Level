import os
import requests
from typing import Optional, Dict
from dotenv import load_dotenv
from pathlib import Path

base_dir = Path(__file__).resolve().parent.parent.parent 
env_path = base_dir / '.env'
load_dotenv(dotenv_path=env_path)

def get_high_res_cover(image_links: dict) -> str:
    """Mencari gambar resolusi tertinggi dari list yang ada."""
    if not image_links:
        return ""
    
    for size in ['extraLarge', 'large', 'medium', 'thumbnail', 'smallThumbnail']:
        if size in image_links:
            url = image_links[size]
            return url.replace('&edge=curl', '').replace('&zoom=1', '&zoom=0')     
    return ""

def search_book_metadata(query: str) -> Optional[Dict]:
    try:
        api_key = os.getenv("GOOGLE_BOOKS_API_KEY")
        
        if not api_key:
            print("FATAL ERROR: GOOGLE_BOOKS_API_KEY tidak ditemukan/kosong di .env!")
            return None

        url = f"https://www.googleapis.com/books/v1/volumes?q={query}&key={api_key}"
        
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        if 'items' not in data or len(data['items']) == 0:
            return None
            
        book_item = data['items'][0]
        book_id = book_item.get('id')
        volume_info = book_item.get('volumeInfo', {})
        
        title = volume_info.get('title', 'Unknown Title')
        authors = volume_info.get('authors', [])
        page_count = volume_info.get('pageCount')
        categories = volume_info.get('categories', [])
        preview_link = volume_info.get('previewLink', '')
        
        image_links = volume_info.get('imageLinks', {})
        thumbnail = get_high_res_cover(image_links)
        
        if not thumbnail and book_id:
            print(f"⚠️ Cover API kosong. Mencoba fallback ID: {book_id}")
            thumbnail = f"https://books.google.com/books/content?id={book_id}&printsec=frontcover&img=1&zoom=0&edge=curl&source=gbs_api"
        
        if thumbnail:
            thumbnail = thumbnail.replace('&zoom=1', '&zoom=0')

        return {
            'title': title,
            'authors': authors,
            'page_count': page_count,
            'categories': categories,
            'preview_link': preview_link,
            'thumbnail': thumbnail 
        }
    except Exception as e:
        print(f"Error Google Books: {e}")
        return None