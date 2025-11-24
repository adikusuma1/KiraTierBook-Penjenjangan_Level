import sys
import asyncio
import uvicorn

if __name__ == "__main__":
    if sys.platform.startswith("win"):
        print("Mengaktifkan WindowsProactorEventLoopPolicy...")
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

    print("Menjalankan Server Stable (Reload Non-Aktif)...")
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=False)