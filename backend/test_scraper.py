import asyncio
from app.services.google_books import search_book_metadata
from app.services.scraper import capture_book_preview

metadata = search_book_metadata('Harry Potter')
print(f"Metadata: {metadata}")
if metadata and 'preview_link' in metadata:
    print(f"Preview link: {metadata['preview_link']}")
    screenshots = asyncio.run(capture_book_preview(metadata['preview_link']))
    print('Screenshots captured:', len(screenshots))
else:
    print('No preview link found')