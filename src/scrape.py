import random, time
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

# ---------- Helpers (unchanged) ----------
def is_valid_item(item):
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
    # Deduplicate items by their image URL
    unique = {}
    for item in items:
        url = extract_img_url(item)
        if url and url not in unique and is_valid_item(item):
            unique[url] = item
    valid_items = list(unique.values())

    author_items = [item for item in valid_items if get_item_author(item) == author]
    other_items  = [item for item in valid_items if item not in author_items]
    chosen = author_items[:count]

    remaining = max(0, count - len(chosen))
    if remaining == count:
        print(f"⚠️ {character}: No matches for author '{author}'")

    if remaining > 0 and other_items:
        chosen.extend(random.sample(other_items, min(remaining, len(other_items))))

    results = []
    for item in chosen:
        author_name = get_item_author(item)
        results.append((extract_img_url(item), author_name, author_name == author))
    return results

# ---------- Core scraping (updated) ----------
def search_page(driver, character, character_type_value, author=None, need_count=0, total_time=15, pause_between=5):
    """
    Scrolls in fixed chunks:
      [pause_between seconds scraping] -> scroll to bottom -> repeat
    for up to total_time seconds (or until enough author matches are seen).
    """
    driver.get("http://shufazidian.com/s.php")

    dropdown = driver.find_element(By.ID, "sort")
    character_select = Select(dropdown)
    character_select.select_by_value(character_type_value)

    search_box = driver.find_element(By.ID, "wd")
    search_box.clear()
    search_box.send_keys(character)
    search_box.send_keys(Keys.RETURN)

    try:
        WebDriverWait(driver, max(5, min(20, total_time))).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.j"))
        )
    except Exception:
        print(f"⚠️ Timeout waiting for initial results for {character}")
        return []

    # Accumulate all harvested elements for later filtering
    all_items = []

    start = time.time()
    end_by = start + max(0, total_time)
    pause_between = max(0.25, float(pause_between))  # avoid 0s

    def harvest():
        items_now = driver.find_elements(By.CSS_SELECTOR, "div.j")
        all_items.extend(items_now)

    # First scrape window before any scroll
    time.sleep(min(pause_between, max(0, end_by - time.time())))
    harvest()

    last_height = driver.execute_script("return document.body.scrollHeight")

    while time.time() < end_by:
        # Scroll to bottom to trigger more loads
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.5)

        # Scrape window
        time.sleep(min(pause_between, max(0, end_by - time.time())))
        harvest()

        # Check if page grew; if not, likely no more items
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Return all harvested items (may contain duplicates)
    return all_items

# ---------- Public API (updated to pass author/need_count) ----------
def searchImg(author, character, character_type_value, wait_time=15, headless=True, count=5, pause_between=5):
    driver = make_driver(headless=headless)
    try:
        items = search_page(
            driver,
            character=character,
            character_type_value=character_type_value,
            author=author,
            need_count=count,
            total_time=wait_time,
            pause_between=pause_between,
        )
        if not items:
            print(f"❌ No results for {character}")
            return []
        return pick_items(items, author, count, character)
    finally:
        driver.quit()
