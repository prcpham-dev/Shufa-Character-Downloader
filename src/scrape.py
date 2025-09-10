import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ---------- Setup ----------
def make_driver(headless=True):
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=options)

# ---------- Core scraping ----------
def search_page(driver, character, character_type_value, wait_time=15):
    driver.get("http://shufazidian.com/s.php")

    dropdown = driver.find_element(By.ID, "sort")
    character_select = Select(dropdown)
    character_select.select_by_value(character_type_value)

    search_box = driver.find_element(By.ID, "wd")
    search_box.clear()
    search_box.send_keys(character)
    search_box.send_keys(Keys.RETURN)

    try:
        WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.j"))
        )
    except Exception:
        print(f"⚠️ Timeout waiting for results for {character}")
        return []
    return driver.find_elements(By.CSS_SELECTOR, "div.j")

# ---------- Helpers ----------
def is_valid_item(item):
    """
    Filter out app promo tiles and broken entries.
    """
    try:
        link = item.find_element(By.CSS_SELECTOR, "div.mbpho a")
        href = link.get_attribute("href")
        img = link.find_element(By.TAG_NAME, "img")
        src = img.get_attribute("src")
        return "app.png" not in src and "app_" not in href
    except Exception:
        return False

def get_item_author(item):
    try:
        return item.find_element(By.CSS_SELECTOR, "a.btnSFJ").text.strip()
    except Exception:
        return "Unknown"
    
def extract_img_url(item):
    try:
        return item.find_element(By.CSS_SELECTOR, "div.mbpho a").get_attribute("href")
    except Exception:
        return None
    
def pick_items(items, author, count, character):
    """
    Return up to {count} items: max author matches, then random valid fillers.
    """
    valid_items = [item for item in items if is_valid_item(item)]
    author_items = [item for item in valid_items if get_item_author(item) == author]
    other_items  = [item for item in valid_items if item not in author_items]
    chosen = author_items[:count]

    # Fill the rest with random others (avoid duplicates)
    remaining = max(0, count - len(chosen))
    if (remaining == count):
        print(f"⚠️ {character}: No matches for author '{author}'")

    if remaining > 0 and other_items:
        chosen.extend(random.sample(other_items, min(remaining, len(other_items))))

    # Package results: (img_url, used_author, is_author)
    results = []
    for item in chosen:
        author_name = get_item_author(item)
        results.append((extract_img_url(item), author_name, author_name == author))
    return results

# ---------- Public API ----------
def searchImg(author, character, character_type_value, wait_time=15, headless=True, count=5):
    driver = make_driver(headless=headless)
    try:
        items = search_page(driver, character, character_type_value, wait_time)
        if not items:
            print(f"❌ No results for {character}")
            return []
        return pick_items(items, author, count, character)
    finally:
        driver.quit()