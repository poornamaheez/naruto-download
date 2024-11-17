from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time

def PageParse(url):
    driver_path = 'chromedriver-win64/chromedriver.exe'
    brave_path = 'C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe'

    brave_options = Options()
    brave_options.binary_location = brave_path

    # Browser configurations
    brave_options.add_argument("--disable-gpu")
    brave_options.add_argument("--no-sandbox")
    brave_options.add_argument("--disable-software-rasterizer")
    brave_options.add_argument("--ignore-certificate-errors")
    brave_options.add_argument("--disable-web-security")
    # brave_options.add_argument("--headless=new")  # Enable if needed

    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=brave_options)
    driver.get(url)
    timeout = 30

    try:
        # Remove any fixed or high z-index overlays dynamically
        def remove_overlays():
            try:
                overlays = driver.find_elements(By.XPATH, "//div[contains(@style,'z-index: 2147483647')]")
                for overlay in overlays:
                    driver.execute_script("arguments[0].remove();", overlay)
                    print("Overlay removed.")
            except Exception as e:
                print(f"Overlay removal error: {e}")

        # Wait for the 'zoro' buttons and click the second one
        zoro_buttons = WebDriverWait(driver, timeout).until(
            EC.presence_of_all_elements_located((By.XPATH, "//button[normalize-space(.)='zoro']"))
        )
        print(f"Found {len(zoro_buttons)} 'zoro' buttons.")

        if len(zoro_buttons) >= 2:
            second_button = zoro_buttons[1]
            driver.execute_script("arguments[0].scrollIntoView();", second_button)
            time.sleep(1)  # Small delay to ensure the view is adjusted
            second_button.click()
            print("Clicked the second 'zoro' button.")
        else:
            print("Less than 2 'zoro' buttons found!")
            driver.quit()
            return 500

        # Wait and retry logic for the download button
        retry_count = 3
        for attempt in range(retry_count):
            try:
                remove_overlays()  # Clear overlays before each attempt

                download_button = WebDriverWait(driver, timeout).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@title='Download Episode']"))
                )
                driver.execute_script("arguments[0].scrollIntoView();", download_button)
                time.sleep(1)  # Give time for the button to become stable

                # Try JavaScript click
                driver.execute_script("arguments[0].click();", download_button)
                print("Clicked the download button.")
                break  # If successful, exit the loop

            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                time.sleep(2)  # Delay before retry

        else:
            print("Failed to click the download button after retries.")
            driver.quit()
            return 500

    except Exception as e:
        print(f"Error during execution: {e}")
        driver.quit()
        return 500

    try:
        # Handle new tab if opened
        WebDriverWait(driver, timeout).until(lambda d: len(d.window_handles) > 1)
        driver.switch_to.window(driver.window_handles[1])
        WebDriverWait(driver, timeout).until(lambda d: len(d.find_elements(By.TAG_NAME, 'a')) >= 12)
    except Exception as e:
        print(f"Error handling new tab: {e}")
        driver.quit()
        return 500

    # Save HTML content
    html_content = driver.page_source
    with open("html_content.txt", "w", encoding="utf-8") as file:
        file.write(html_content)

    driver.quit()
    return 200

# Example usage
# url = "https://example.com"  # Replace with your target URL
# PageParse(url)
