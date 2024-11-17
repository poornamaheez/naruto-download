import os
import re

def missing_files_in_folder(folder_path):
    try:
        # List all files in the directory
        files = os.listdir(folder_path)
        
        # Iterate over the files and delete those with 0KB size
        for f in files:
            file_path = os.path.join(folder_path, f)
            if os.path.isfile(file_path) and os.path.getsize(file_path) == 0:
                os.remove(file_path)  # Delete file with 0KB size
                print(f"Deleted: {file_path}")
        
        # Re-list the files after deletion
        files = os.listdir(folder_path)

        # Filter and return only the files (not directories), and extract numerical parts
        file_list = [int(''.join([char for char in os.path.splitext(f)[0] if char.isdigit()])) for f in files if os.path.isfile(os.path.join(folder_path, f))]
        
        # Sort the list to make sure it's in order
        number_list = sorted(file_list)
        
        # Find the minimum and maximum range
        full_range = set(range(number_list[0], number_list[-1] + 1))
        
        # Find the missing numbers by subtracting the given list from the full range
        missing_numbers = sorted(full_range - set(number_list))
        
        # Return missing numbers or 0 if none are missing
        return missing_numbers if missing_numbers else []
        
    except Exception as e:
        print(f"Error: {e}")
        return []

# Example usage
# folder_path = 'your/folder/path'
# missing_files = missing_files_in_folder(folder_path)
# print(missing_files)
