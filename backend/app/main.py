import sys
import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.models import BookRequest, BookResult
from app.services.google_books import search_book_metadata
from app.services.scraper import capture_book_preview
from app.services.ai_engine import analyze_book_with_ai

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

app = FastAPI(title="Book Classifier AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/analyze", response_model=BookResult)
async def analyze_book(request: BookRequest):
    print(f"\nSTART: Menganalisis '{request.title}'...")
    
    metadata = search_book_metadata(request.title)
    if not metadata:
        raise HTTPException(status_code=404, detail="Buku tidak ditemukan")
    print(f"Metadata: Ditemukan ({metadata.get('page_count')} hal).")

    print("Scraper: Mengambil screenshot...")
    screenshots = await capture_book_preview(metadata['preview_link'])
    
    evidence_img = screenshots[0] if screenshots else ""
    
    if not evidence_img:
        print("Warning: Screenshot gagal/blank. AI hanya akan pakai metadata.")

    print("AI Engine: Memulai klasifikasi...")
    ai_result = await analyze_book_with_ai(metadata, evidence_img)
    
    print(f"FINISH: Prediksi {ai_result.jenjang} ({ai_result.confidence_score}%)")

    return BookResult(
        title=metadata['title'],
        authors=metadata['authors'],
        page_count=metadata.get('page_count'),
        categories=metadata['categories'],
        thumbnail=metadata.get('thumbnail'), 
        screenshots=screenshots,
        analysis=ai_result
    )

if __name__ == "__main__":
    import uvicorn
    print("Server siap di [http://127.0.0.1:8000](http://127.0.0.1:8000)")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=False)