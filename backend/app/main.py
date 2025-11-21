import sys
import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.models import BookRequest, BookData
from app.services.google_books import search_book_metadata
from app.services.scraper import capture_book_preview

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

app = FastAPI(
    title="Book Classifier API", 
    description="API untuk klasifikasi buku berdasarkan penjenjangan", 
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/search", response_model=BookData)
async def search(request: BookRequest):
    print(f"Menerima Request: {request.title}")
    metadata = search_book_metadata(request.title)
    if not metadata:
        print("Metadata tidak ditemukan.")
        raise HTTPException(status_code=404, detail="Book not found")
    
    print(f"Metadata OK. Link Preview: {metadata['preview_link']}")
    screenshots = await capture_book_preview(metadata['preview_link'])
    
    return BookData(
        title=metadata['title'],
        authors=metadata['authors'],
        page_count=metadata.get('page_count'),
        categories=metadata['categories'],
        screenshots=screenshots
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)