import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .filtering import pick_items


def make_driver(headless=True):
    """Create and configure a Chrome WebDriver."""
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)


def search_page(driver, character, character_type_value, 
                total_time=15, pause_between=5):
    """
    Search for a character and scroll to load results.
    """
    driver.get("http://shufazidian.com/s.php")

    # select the character type
    Select(driver.find_element(By.ID, "sort")).select_by_value(character_type_value)

    # enter the character and search
    box = driver.find_element(By.ID, "wd")
    box.clear()
    box.send_keys(character)
    box.send_keys(Keys.RETURN)

    # wait until results appear
    try:
        WebDriverWait(driver, max(5, min(20, total_time))).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.j"))
        )
    except Exception:
        print(f"⚠️ Timeout waiting for initial results for {character}")
        return []

    items = []
    start = time.time()
    end_time = start + max(0, total_time)
    pause_between = max(0.25, float(pause_between))
    last_height = 0

    # scrolling loop
    while time.time() < end_time:
        time.sleep(pause_between)
        items.extend(driver.find_elements(By.CSS_SELECTOR, "div.j"))

        # scroll to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.5)

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    return items


def searchImg(author, character, character_type_value,
              wait_time=15, headless=True, count=5, pause_between=5):
    """
    Wrapper for searching for images of a given character and author.
    """
    driver = make_driver(headless=headless)
    try:
        items = search_page(
            driver,
            character=character,
            character_type_value=character_type_value,
            total_time=wait_time,
            pause_between=pause_between,
        )
        if not items:
            print(f"❌ No results for {character}")
            return []

        return pick_items(items, author, count)
    finally:
        driver.quit()
