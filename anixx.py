from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

def PageParse(url):
    
    # Set up ChromeDriver options
    brave_path = 'C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe'


    options = webdriver.ChromeOptions()
    options.binary_location = brave_path

    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--incognito")
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_argument("--headless=new")

    # Provide the correct path to chromedriver
    service = Service('chromedriver-win64/chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Step 1: Open the target webpage and wait for it to fully load
        driver.get(url)
        print("Page loading...")
        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        print("Page loaded successfully.")

        # Step 2: Wait for the Dub section to appear
        wait = WebDriverWait(driver, 20)
        dub_section = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.ps_-block.ps_-block-dub")))
        print("Dub section found.")

        # Step 3: Locate and click the 'Download' button in the Dub section
        download_button = dub_section.find_element(By.XPATH, ".//div[@onclick='openDownloadModal(this)']")
        download_button.click()
        print("Download button clicked. Waiting for modal...")

        # Step 4: Wait for the modal to become visible
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "modal")))
        print("Modal is visible. Searching for 'Multi Server' button...")

        # Step 5: Find the 'Multi Server' button in the modal and extract its href
        multi_server_button = wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Multi Server")))
        href = multi_server_button.get_attribute("href")
        print(f"Found href: {href}")

        # Step 6: Navigate to the URL in the href and ensure full loading
        driver.get(href)
        print("Navigating to the Multi Server page...")

        # Additional wait for specific elements on the new page to ensure it fully loads
        wait.until(lambda d: d.execute_script('return document.readyState') == 'complete')
        print("Multi Server page loaded.")

        # Optional: Adjust delay to wait for dynamic elements (if needed)
        time.sleep(5)  # Adjust this if some elements take longer to load

        # Step 7: Save the new page's HTML content to the text file
        with open("html_content.txt", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print("HTML content replaced with content from Multi Server page.")

    except TimeoutException as e:
        print(f"Page or element loading timed out: {e}")

    except NoSuchElementException as e:
        print(f"Element not found: {e}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    finally:
        # Optional: Keep the browser open for a few seconds before quitting
        time.sleep(5)
        driver.quit()
        return 200

# Usage
# download_and_replace_content("https://anixx.to/watch/naruto-shippuden/ep-330")
