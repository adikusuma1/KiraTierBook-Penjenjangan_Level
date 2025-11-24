import sys
import os
import asyncio
import uvicorn

if __name__ == "__main__":
    if sys.platform.startswith("win"):
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

    port = int(os.environ.get("PORT", 8000))
    
    print(f"Menjalankan Server di Port {port}...")
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=False)