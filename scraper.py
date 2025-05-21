import asyncio
import base64
import time
from playwright.async_api import async_playwright

async def fetch_img():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        await page.goto('https://www.reddicks.meme/live-card/', wait_until='networkidle')

        # Tenta por até 60 segundos encontrar uma imagem base64 válida
        timeout_seconds = 60
        interval = 2  # segundos entre as tentativas
        start_time = time.time()

        img_data_uri = None

        while time.time() - start_time < timeout_seconds:
            try:
                await page.wait_for_selector("img", timeout=3000)
                img_sources = await page.eval_on_selector_all("img", "els => els.map(el => el.src)")
                data_uri_imgs = [src for src in img_sources if src.startswith("data:")]
                if data_uri_imgs:
                    img_data_uri = data_uri_imgs[0]
                    break
            except Exception:
                pass
            await asyncio.sleep(interval)

        if not img_data_uri:
            raise ValueError("Nenhuma imagem base64 encontrada após esperar até 60 segundos.")

        print("Imagem base64 encontrada.")

        if "," not in img_data_uri:
            raise ValueError("Formato inválido de data URI.")

        header, encoded = img_data_uri.split(",", 1)
        file_ext = header.split(";")[0].split("/")[-1]

        img_bytes = base64.b64decode(encoded)
        filename = f"card.{file_ext}"

        with open(filename, "wb") as f:
            f.write(img_bytes)

        print(f"Imagem salva como: {filename}")
        await browser.close()