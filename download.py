import os
import asyncio
import aiohttp
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


def searchImg(author, word, wait_time=15):
    """
    Use Selenium (blocking) to find the full-size image URL for given word+author.
    """
    driver = webdriver.Chrome()
    driver.get("http://shufazidian.com/s.php")

    # enter word into search box
    search_box = driver.find_element(By.ID, "wd")
    search_box.clear()
    search_box.send_keys(word)
    search_box.send_keys(Keys.RETURN)

    # wait until results load (instead of fixed sleep)
    try:
        WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.j"))
        )
    except:
        print(f"⚠️ Timeout waiting for results for {word}")
        driver.quit()
        return None

    img_url = None
    items = driver.find_elements(By.CSS_SELECTOR, "div.j")
    for item in items:
        try:
            author_text = item.find_element(By.CSS_SELECTOR, "a.btnSFJ").text.strip()
        except:
            continue
        if author_text == author:
            link = item.find_element(By.CSS_SELECTOR, "div.mbpho a")
            img_url = link.get_attribute("href")
            break

    driver.quit()
    return img_url



async def downloadImg(author, word, out_dir="images"):
    """
    Main async wrapper: search with Selenium, then download with aiohttp.
    """
    img_url = await asyncio.to_thread(searchImg, author, word)
    if not img_url:
        print(f"❌ No image found for {word} by {author}")
        return None

    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, f"{word}.jpg")

    async with aiohttp.ClientSession() as session:
        await fetchImg(session, img_url, out_file)

    return out_file

if __name__ == "__main__":
    asyncio.run(downloadImg("苏轼", "饮"))