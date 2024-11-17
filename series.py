from bs4 import BeautifulSoup
from WebParser import  getPage
from anixx import PageParse
from FileDownload import download_file
from MissingEpisodes import missing_files_in_folder
import os

def DownloadSeries(id, Series, episode):
    print('------------------------------------------------------------')
    print(f"|       Process started for {Series}-EP{episode}           |")
    print('------------------------------------------------------------')
    url=f"https://anixx.to/watch/{id}/ep-{episode}"
    status = PageParse(url)
    download_link = ''
    if status == 200:
        print('Page saved in file successfully')

        with open('html_content.txt', 'r', encoding='utf-8') as file:
            content = file.read()
            soup = BeautifulSoup(content, 'html.parser')
            anchor_tags = soup.find_all('a')
            print(len(anchor_tags))
            while len(anchor_tags)<12:
                PageParse(url)
                content = file.read()
                soup = BeautifulSoup(content, 'html.parser')
                anchor_tags = soup.find_all('a')
            if len(anchor_tags)>1:
                # print(anchor_tags[4]['href'])
                download_link = anchor_tags[4]['href']
        if len(download_link)>1:
            size = download_file(download_link,f"{Series}-Ep-{episode}.mp4",r"D:\Videos\naruto")

            while size is None:
                size = DownloadSeries(Series, episode, episode)

        else:
            print('downlod link not found')
    # try:
    #     os.remove("html_content.txt")
    #     print('Deleted html_content!!')
    # except FileNotFoundError:
    #     print("File does not exist")


Series_Name = "Naruto Shippuden"
id = "naruto-shippuden"
# DownloadSeries(id, Series_Name ,424)

for i in range(433,451):
    DownloadSeries(id, Series_Name ,i)
# missing = missing_files_in_folder(r"D:\Videos\naruto")

# if len(missing)>0:
#     print(f"Missing files are {missing}")
#     UserInput = input('should we continue[y/n]: ')
#     if UserInput == 'y':
#         print("Ok! Here we go")
#         for i in missing:
#             DownloadSeries(id, Series_Name,i)
#     else:
#         print("No! Alright.... Bye!")
# else:
#     print('No Missing Files')

## https://anixx.to/watch/naruto-shippuden/ep-331