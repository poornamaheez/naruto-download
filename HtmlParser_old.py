import requests
from bs4 import BeautifulSoup

# Replace with the URL generated by your Live Server
url = 'http://127.0.0.1:5500/divs.html'  # Change this to your actual URL

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the first div (outermost div)
    outermost_div = soup.find('div')

    # Find all the divs inside the outermost div
    inner_divs = outermost_div.find_all('a')

    # Access the second div (index 1) in the outermost div
    if len(inner_divs) > 1:
        second_div = inner_divs[0]['href']
        print("Second div content:", second_div)  # Use prettify for better formatting
    else:
        print("There is no second div inside the outermost div.")
else:
    print(f"Failed to retrieve the URL. Status code: {response.status_code}")
