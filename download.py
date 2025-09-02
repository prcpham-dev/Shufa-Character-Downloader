import os
import asyncio
import aiohttp
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


async def fetchImg(session, url, out_file):
    """
    Download image asynchronously with aiohttp.
    """
    async with session.get(url) as resp:
        resp.raise_for_status()
        with open(out_file, "wb") as f:
            f.write(await resp.read())
    print(f"✅ Saved {out_file}")


def _make_driver(headless=True):
    """
    Create a Chrome WebDriver (headless by default).
    """
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=options)


def searchImg(author, word, wait_time=15, headless=True):
    """
    Use Selenium (blocking) to find the full-size image URL for given word+author.
    If the exact author is not found, pick a random result from the page.
    Returns: (img_url, used_author) or (None, None) if nothing found.
    """
    driver = _make_driver(headless=headless)
    try:
        driver.get("http://shufazidian.com/s.php")

        # enter word into search box
        search_box = driver.find_element(By.ID, "wd")
        search_box.clear()
        search_box.send_keys(word)
        search_box.send_keys(Keys.RETURN)

        # wait until results load
        try:
            WebDriverWait(driver, wait_time).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.j"))
            )
        except Exception:
            print(f"⚠️ Timeout waiting for results for {word}")
            return (None, None)

        items = driver.find_elements(By.CSS_SELECTOR, "div.j")
        if not items:
            print(f"❌ No results for {word}")
            return (None, None)

        # try to find exact author
        chosen = None
        for item in items:
            try:
                author_text = item.find_element(By.CSS_SELECTOR, "a.btnSFJ").text.strip()
            except Exception:
                continue
            if author_text == author:
                chosen = (item, author_text)
                break

        # fallback: random item
        if chosen is None:
            item = random.choice(items)
            try:
                author_text = item.find_element(By.CSS_SELECTOR, "a.btnSFJ").text.strip()
            except Exception:
                author_text = "Unknown"
            chosen = (item, author_text)
            print(f"ℹ️ Author '{author}' not found. Falling back to random author: {author_text}")

        item, used_author = chosen
        link = item.find_element(By.CSS_SELECTOR, "div.mbpho a")
        img_url = link.get_attribute("href")
        return (img_url, used_author)

    finally:
        driver.quit()


async def downloadImg(author, word, out_dir="images", headless=True):
    """
    Main async wrapper: search with Selenium, then download with aiohttp.
    If author isn't found, a random result is used (and reported).
    """
    img_url, used_author = await asyncio.to_thread(searchImg, author, word, 15, headless)
    if not img_url:
        print(f"❌ No image found for '{word}' (author requested: {author})")
        return None

    os.makedirs(out_dir, exist_ok=True)
    # include used author in filename to avoid collisions when random fallback kicks in
    safe_author = used_author.replace("/", "_").replace("\\", "_")
    out_file = os.path.join(out_dir, f"{word}_{safe_author}.jpg")

    async with aiohttp.ClientSession() as session:
        await fetchImg(session, img_url, out_file)

    return out_file


if __name__ == "__main__":
    asyncio.run(downloadImg("苏轼", "饮"))
