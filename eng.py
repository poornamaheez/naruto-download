from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def PageParse(url):
    # Path to your ChromeDriver
    driver_path = 'chromedriver-win64/chromedriver.exe'  # Change this to the path of your chromedriver

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
        # Find all buttons containing the text 'Zoro'
        zoro_buttons = WebDriverWait(driver, timeout).until(
            EC.presence_of_all_elements_located((By.XPATH, "//button[contains(., 'Zoro')]"))
        )

        if len(zoro_buttons) >= 2:
            for _ in range(0,10):
                zoro_buttons[1].click()  # Click the second 'Zoro' button
            print("Clicked the second 'Zoro' button.")
        else:
            print("Less than 2 'Zoro' buttons found!")
            driver.quit()
            return 500  # Return an error code if the second button is not found

        # Wait for the "Download Episode" button to be visible and clickable
        download_button = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@title='Download Episode']"))
        )
        download_button.click()  # Click the download button
        print("Clicked the download button.")
    except Exception as e:
        print(f"Error finding or clicking buttons: {e}")
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
