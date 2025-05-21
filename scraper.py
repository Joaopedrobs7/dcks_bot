# scraper.py
import asyncio
import base64
from playwright.async_api import async_playwright

async def fetch_img():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        await page.goto('https://www.reddicks.meme/live-card/', wait_until='networkidle')

        # Get the base64 image source
        img_data_uri = await page.eval_on_selector("img", "el => el.src")
        print("Data URI received.")

        # Split header and base64 content
        header, encoded = img_data_uri.split(",", 1)
        file_ext = header.split(";")[0].split("/")[-1]  # e.g., 'png'

        # Decode and write to file
        img_bytes = base64.b64decode(encoded)
        filename = f"card.{file_ext}"

        with open(filename, "wb") as f:
            f.write(img_bytes)

        print(f"Saved image as: {filename}")
        await browser.close()
