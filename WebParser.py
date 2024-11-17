from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

def getPage(url):
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run headless if you don't need a visible browser window

    # Specify the path to your ChromeDriver
    service = Service('chromedriver-win64/chromedriver-win64/chromedriver.exe')  # Replace with your path to ChromeDriver
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get(url)

    # Wait for the page to load (you can adjust the sleep time if needed)
    time.sleep(10)
    html_con = driver.page_source
    # Print the modal HTML
    # print(modal_html)
    with open('html_content.txt', 'w', encoding='utf-8') as file:
        file.write(html_con)
    # Clean up
    driver.quit()

    return 200

# Replace with the URL of the page containing the modal
url = 'https://s3taku.com/download?id=MTA3NDQ4&typesub=Gogoanime-DUB&title=Naruto+Shippuuden+%28Dub%29+Episode+192'  # Replace with the actual URL

