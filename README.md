# Dad's Shufa Chinese Characters
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
- Example:
    ```
    苏轼
    饮马渡秋水
    水寒风似刀
    平沙日未没
    ```

2. **Run the program:** 
- The script will search each character/phrase on the website, filter by author, and download matching images to the `images/` folder.

## Setup

1. **Install Python (if not already installed):**
- **Windows:** Download and install Python 3.9 or newer from [python.org](https://www.python.org/downloads/).  
    Make sure to check "Add Python to PATH" during installation.
- **Mac:** Download from [python.org](https://www.python.org/downloads/) or use Homebrew:
    ```bash
    brew install python
    ```

2. **(Recommended) Create a virtual environment:**
- **Windows:**
    ```bat
    python -m venv venv
    venv\Scripts\activate
    ```
- **Mac:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Download and install [ChromeDriver](https://chromedriver.chromium.org/downloads) matching your Chrome version.**

5. **Update your `shufa.txt` in the project folder.**

6. **Run the script:**
   ```bash
   python main.py
   ```