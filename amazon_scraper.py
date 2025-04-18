from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

async def get_two_images_from_amazon(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url, timeout=60000)
        await page.wait_for_selector("img", timeout=15000)
        html = await page.content()
        soup = BeautifulSoup(html, 'html.parser')
        img_tags = soup.find_all("img")
        img_urls = []
        for img in img_tags:
            src = img.get("src")
            if src and "media-amazon" in src and src.endswith(".jpg"):
                img_urls.append(src)
        await browser.close()
        return img_urls[:2]
