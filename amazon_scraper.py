from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

def get_two_images_from_amazon(url):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url, timeout=60000)
        page.wait_for_selector("img", timeout=15000)
        html = page.content()
        soup = BeautifulSoup(html, 'html.parser')
        img_tags = soup.find_all("img")
        img_urls = []
        for img in img_tags:
            src = img.get("src")
            if src and "media-amazon" in src and src.endswith(".jpg"):
                img_urls.append(src)
        browser.close()
        return img_urls[:2]
