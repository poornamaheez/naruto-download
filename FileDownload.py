import requests
from tqdm import tqdm
import os  # Import os to work with file paths

def download_file(url, file_name, save_path='.'):
    # Ensure the save path exists
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    # Full file path
    file_path = os.path.join(save_path, file_name)

    # Stream the file download to avoid loading large files into memory
    response = requests.get(url, stream=True)
    
    # Get the total file size in bytes
    total_size = int(response.headers.get('content-length', 0))

    # Convert bytes to megabytes
    total_size_mb = total_size / (1024 * 1024)
    print(f"Now downloading: {file_name}")

    print(f"Total file size: {total_size_mb:.2f} MB")

    # Open the local file and write the content to it in chunks
    with open(file_path, 'wb') as file:
        # Create a progress bar with tqdm
        for data in tqdm(response.iter_content(chunk_size=1024), total=total_size//1024, unit='KB', unit_scale=True):
            file.write(data)
    
    print(f"\nFile downloaded successfully: {file_path}")
    return total_size_mb

# Example usage
# url = r"https://hindianimeworld.com/?download_links=https%3A%2F%2Fggredi.info%2Fdownload.php%3Furl%3DaHR0cHM6LyURASDGHUSRFSJGYfdsffsderFStewthsfSFtrfteAawehyfcghysfdsDGDYdgdsfsdfwstdgdsgtertsdf9wd3l4aXltZWx1LmFuZjU5OC5jb20vdXNlcjEzNDIvMmFmYjcxMTZhZDM3MzRiNDY3ZTQ5YjIwNmViMzgwZWQvRVAuMzMwLnYxLjE3MTc3MDU3NDMuMTA4MHAubXA0P3Rva2VuPUcxd0ctOFFBVDAxZWFCVzVxc3FaZEEmZXhwaXJlcz0xNzI5ODU4MjcyJmlkPTEwNzU5NCZ0aXRsZT0oMTkyMHgxMDgwLWdvZ29hbmltZSluYXJ1dG8tc2hpcHB1dWRlbi1kdWItZXBpc29kZS0zMzAubXA0"
# file_name = 'downloaded_file.mp4'  # Specify the file name with extension
# save_path = './downloads'  # Path where the file should be saved (relative or absolute)
# download_file(url, file_name, save_path)
