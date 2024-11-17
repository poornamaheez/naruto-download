from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def PageParse(url):
    # Path to your ChromeDriver
    driver_path = 'chromedriver-win64/chromedriver-win64/chromedriver.exe'  # Change this to the path of your chromedriver

    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode (no UI)
    chrome_options.page_load_strategy = 'eager'  # Only wait for DOMContentLoaded event, not full page load
    chrome_options.add_argument("--disable-extensions")  # Disable extensions for performance
    chrome_options.add_argument("--disable-gpu")  # Disable GPU for headless mode
    chrome_options.add_argument("--no-sandbox")  # Prevent issues with sandboxing in some environments

    # Disable image loading for performance boost
    chrome_prefs = {
        "profile.managed_default_content_settings.images": 2
    }
    chrome_options.experimental_options["prefs"] = chrome_prefs

    # Set up the ChromeDriver service
    service = Service(driver_path)

    # Initialize the WebDriver with options
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url)

    # Set a longer timeout value for slow page loads
    timeout = 30  # You can adjust this based on the website's load speed

    try:
        # Wait for the button to be visible and clickable
        download_button = WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((By.XPATH, "//button[@title='Download Episode']"))
        )
        download_button = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@title='Download Episode']"))
        )
        download_button.click()
    except Exception as e:
        print(f"Error finding or clicking the button: {e}")
        driver.quit()
        return 500  # Return an error code if something goes wrong

    try:
        # Wait for the new tab to open
        WebDriverWait(driver, timeout).until(lambda d: len(d.window_handles) > 1)

        # Switch to the new tab
        driver.switch_to.window(driver.window_handles[1])

        # Wait until at least 12 <a> tags are present on the new tab
        WebDriverWait(driver, timeout).until(
            lambda d: len(d.find_elements(By.TAG_NAME, 'a')) >= 12
        )
    except Exception as e:
        print(f"Error waiting for the new tab or loading: {e}")
        driver.quit()
        return 500  # Return an error code if something goes wrong

    # Get the HTML content of the new tab
    html_content = driver.page_source

    # Write the HTML content to a text file
    with open("html_content.txt", "w", encoding="utf-8") as file:
        file.write(html_content)

    # Close the browser
    driver.quit()

    return 200
