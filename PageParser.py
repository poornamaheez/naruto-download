import requests
from bs4 import BeautifulSoup

def GetPage(url):
    response = requests.get(url)

    if response.status_code == 200:
        return response
    else:
        return     f"Failed to retrieve the URL. Status code: {response.status_code}"