# Dad's Shufa Stuff
This project helps you automatically download Chinese calligraphy images from [shufazidian.com](http://shufazidian.com/s.php)

## Features
- Search for calligraphy images by author and character/phrase.
- Automatically match images with the chosen author.
- Save images to a local `images/` folder.

## How to Use

1. **Prepare your input file:**
   - Open the text file named `shufa.txt`.
   - The first line is the author's name (e.g., `苏轼`).
   - Each following line is a character or phrase you want to search.

   Example `shufa.txt`:
   ```
   苏轼
   饮马渡秋水
   水寒风似刀
   平沙日未没
   ```

2. **Run the program:**
   - The script will search each character/phrase on the website, filter by author, and download matching images to the `images/` folder.

## Setup

- **Python 3.9+**
- **Google Chrome** installed
- **ChromeDriver** (used by Selenium to control Chrome)
- **(Recommended) Create a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
- Python libraries:
  ```bash
  pip install -r requirements.txt
  ```

## Setup

1. Install dependencies:
   ```bash
   pip install aiohttp selenium
   ```
2. Download and install [ChromeDriver](https://chromedriver.chromium.org/downloads) matching your Chrome version.
3. Place your `shufa.txt` in the project folder.
4. Run the script:
   ```bash
   python main.py
   ```

## Notes
- Images will be saved in the `images/` directory.
