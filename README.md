# Shufa Character Downloader
This project helps my dad to automatically download Chinese calligraphy images from [shufazidian.com](http://shufazidian.com/s.php) to help his with his drawing.

## Features
- Search for calligraphy images by author and character/phrase.
- Automatically match images with the chosen author.
- Save images to a local `images/` folder.

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

4. **Setup WebDriver:**

    1. **Check your Chrome version:**
    - Open Chrome and go to `chrome://settings/help`.

    2. **Download ChromeDriver:**
    - Go to [ChromeDriver Downloads](https://chromedriver.chromium.org/downloads).
    - Pick the version that matches your Chrome.

    3. **Install ChromeDriver:**
    - **Windows:** Place `chromedriver.exe` in the project folder or add it to PATH.
    - **Mac/Linux:** Move it to `/usr/local/bin/` and make it executable:
        ```bash
        sudo mv chromedriver /usr/local/bin/
        sudo chmod +x /usr/local/bin/chromedriver
        ```

    4. **Verify installation:**
    - Open a terminal/command prompt and run:
        ```bash
        chromedriver --version
        ```

    Tip: Make sure you download the correct ChromeDriver for your system.
    - If any step is unclear, you can ask ChatGPT for help. For example, copy and paste this prompt:

        **Prompt:**  
        "I’m setting up ChromeDriver for the Shufa Character Downloader on [Windows/Mac/Linux].  
        My Chrome version is [paste version here].  
        Can you tell me exactly which ChromeDriver to download and how to install it?"
    - **Windows:** Choose the version that matches your Chrome browser and your system type (64-bit or 32-bit).  
    - **macOS/Linux:** Download the build for your OS (Intel or Apple Silicon for mac).  

5. **Run the program:**
    - **Windows:**  
        Double-click `myApp.py`.
        If it opens in an editor instead of running, right-click → *Open with* → choose **Python** and check “Always use this app”.

    - **macOS:**  
        Double-click `myApp.py`.  
        If it opens in a text editor instead of running:  
        1. Right-click `myApp.py` → *Get Info*.  
        2. Under *Open with*, select **Python Launcher**.  
        3. Click **Change All…** so `.py` files always use Python.  

    - **Linux:**  
        Make the file executable (one-time setup):  
        ```bash
        chmod +x myApp.py

## How to Use

1. **Fill in your input:**
- **Wait time:** Number of seconds to wait between downloads (helps avoid being blocked and stuck on one task)
- **Batch Size:** Number of character being progress at a time.
- **Amount:** Total number of images to download per character.
- **Author:** Enter the calligraphy master’s name (e.g., 苏轼).
- **Character Type:** Choose calligraphy style (e.g., 行书, 草书, 楷书).
- **Chinese Text:** Paste or type in Chinese characters, phrases, or full poems you want to download. !!!Only keep Chinese character

2. **Start the download:**
- Click **Start** to begin fetching images.
- Progress and logs will be shown in **Logs** tab.
- Download images are saved into the local images/ folder, organized by character.

3. **Manage images:**
- Use **Delete Images** to clear previously download images.
- Use **Save Settings** to preserve your current configuration for next time.
