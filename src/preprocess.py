import json 

SETTING_PATH = "setting.json"

def load_settings():
    """
    Load settings from setting.json.
    """
    with open(SETTING_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_settings(settings):
    """
    Save settings to setting.json.
    """
    with open(SETTING_PATH, "w", encoding="utf-8") as f:
        json.dump(settings, f, ensure_ascii=False, indent=2)
    
def prepare_data():
    settings = load_settings()
    wait_time = settings.get("wait_time", 15)
    batch_size = settings.get("batch_size", 4)
    count = settings.get("count", 5)

    author = settings.get("author", "").strip()
    character_type_value = settings.get("character_type_value", "").strip()

    characters = settings.get("characters", "")
    characters = list(dict.fromkeys(characters.replace("\n", "")))
    return author, characters, character_type_value, wait_time, batch_size, count
