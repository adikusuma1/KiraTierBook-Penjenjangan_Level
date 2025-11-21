from app.models import BookRequest, BookData
import asyncio
from app.services.google_books import search_book_metadata
from app.services.scraper import capture_book_preview

request = BookRequest(title="Harry Potter")
metadata = search_book_metadata(request.title)
if metadata and 'preview_link' in metadata:
    screenshots = asyncio.run(capture_book_preview(metadata['preview_link']))
    book_data = BookData(
        title=metadata['title'],
        authors=metadata['authors'],
        page_count=metadata.get('page_count'),
        categories=metadata['categories'],
        screenshots=screenshots
    )
    print("Full pipeline successful:")
    print("BookData:", book_data)
else:
    print("No metadata or preview link found")