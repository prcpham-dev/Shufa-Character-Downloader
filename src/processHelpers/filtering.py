from selenium.webdriver.common.by import By
import random

def is_valid_item(item):
    """
    Checks if a search result item is valid (real calligraphy, not PNG preview).

    """
    try:
        # must have a proper <a> and <img>
        link = item.find_element(By.CSS_SELECTOR, "div.mbpho a")
        href = link.get_attribute("href")
        img = link.find_element(By.TAG_NAME, "img")
        src = img.get_attribute("src")

        # skip app or PNG-only versions
        if not href or not src:
            return False
        if "app.png" in src or "app_" in href:
            return False
        if "/png/" in href or "/png/" in src:
            return False

        # possibly remove red
        if not "/gq/" in href or not "/gq/" in src:
            return False

        return True
    except Exception:
        return False

def get_item_author(item):
    """
    Extracts the author name from a search result item.
    """
    try:
        return item.find_element(By.CSS_SELECTOR, "a.btnSFJ").text.strip()
    except Exception:
        return "Unknown"
    
def extract_img_url(item):
    """
    Extracts the image URL from a search result item.
    """
    try:
        return item.find_element(By.CSS_SELECTOR, "div.mbpho a").get_attribute("href")
    except Exception:
        return None

def pick_items(items, author, count):
    """
    Return a list of `count` (image_url, author_name, is_author) items for
    later downloading phase.
    """
    seen = set()
    item_info = []
    
    for item in items:
        try:
            url = extract_img_url(item)
            if not url or url in seen or not is_valid_item(item):
                continue

            seen.add(url)
            author_name = get_item_author(item)
            item_info.append((url, author_name, author_name == author))
        except Exception:
            continue

    author_items = [i for i in item_info if i[2]]
    other_items = [i for i in item_info if not i[2]]

    chosen = author_items[:count]
    if len(chosen) < count:
        remaining = count - len(chosen)
        chosen.extend(random.sample(other_items, min(remaining, len(other_items))))

    return chosen
