import asyncio
import base64
from playwright.async_api import async_playwright

async def capture_book_preview(url: str) -> list:
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent=USER_AGENT,
            viewport={'width': 1280, 'height': 800}, 
            device_scale_factor=1
        )
        
        page = await context.new_page()
        
        try:
            print(f"Scraper: Membuka URL... {url[:50]}...")
            await page.goto(url, timeout=30000, wait_until="domcontentloaded")
            print("Scraper: Menunggu rendering canvas Google Books...")
            await asyncio.sleep(5) 
            await page.mouse.wheel(0, 600)
            await asyncio.sleep(3) 
            screenshot = await page.screenshot(full_page=False)
            base64_screenshot = base64.b64encode(screenshot).decode('utf-8')
            print(f"Scraper: Berhasil mengambil screenshot! (Size: {len(base64_screenshot)} chars)")
            await browser.close()
            return [base64_screenshot]

        except Exception as e:
            print(f"Scraper Error: {str(e)}")
            await browser.close()
            return []