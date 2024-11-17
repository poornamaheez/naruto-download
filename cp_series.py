from bs4 import BeautifulSoup
from WebParser import getPage
from anixx import PageParse
from FileDownload import download_file
from MissingEpisodes import missing_files_in_folder
import os
import time  # For retry delays

def DownloadSeries(id, series_name, episode):
    print('------------------------------------------------------------')
    print(f"|       Process started for {series_name} - EP{episode}       |")
    print('------------------------------------------------------------')

    url = f"https://anixx.to/watch/{id}/ep-{episode}"
    status = PageParse(url)

    if status != 200:
        print(f"Failed to fetch page for {series_name} - EP{episode}. Skipping...")
        return None

    print('Page saved in file successfully')
    download_link = ''

    # Retry logic for reading the file until anchor tags are found
    retries = 5
    while retries > 0:
        with open('html_content.txt', 'r', encoding='utf-8') as file:
            content = file.read()
            soup = BeautifulSoup(content, 'html.parser')
            anchor_tags = soup.find_all('a')

        if len(anchor_tags) >= 12:
            download_link = anchor_tags[4].get('href', '')
            if download_link:
                break  # Exit loop if link is found
        else:
            print("Anchor tags not found, retrying...")
            PageParse(url)  # Re-fetch the page
            retries -= 1
            time.sleep(2)  # Avoid rapid retries

    if not download_link:
        print(f"Download link not found for {series_name} - EP{episode}.")
        return None

    size = download_file(download_link, f"{series_name}-Ep-{episode}.mp4", r"D:\Videos\Boruto")
    if size is None:
        print("Download failed. Retrying...")
        DownloadSeries(id, series_name, episode)  # Retry the download

    # Clean up the temporary file
    # try:
    #     os.remove("html_content.txt")
    #     print("Deleted html_content.txt!")
    # except FileNotFoundError:
    #     print("html_content.txt not found for cleanup.")

# Parameters
series_name = "Boruto"
series_id = "boruto-naruto-next-generations"

# DownloadSeries(series_id, series_name, 1)
# for ep in range(12,20):
#     DownloadSeries(series_id, series_name, ep)

# Check for missing files
missing = missing_files_in_folder(r"D:\Videos\Boruto")

if missing:
    print(f"Missing files: {missing}")
    user_input = input('Should we continue downloading the missing files? [y/n]: ').strip().lower()
    if user_input == 'y':
        print("Continuing download for missing episodes...")
        for ep in missing:
            DownloadSeries(series_id, series_name, ep)
    else:
        print("Exiting... No further downloads.")
else:
    print("All episodes are downloaded.")