import sys
import os
import requests
from PIL import Image
from io import BytesIO

# Check if the correct number of arguments is provided
if len(sys.argv) != 4:
    print("Usage: python name_of_script.py \"c:\\saving_folder\" \"example_name_of_image.jpg\" \"http://example.image_url.com\"")
    sys.exit(2)

def download_and_save(image_url, saving_folder_path, name_of_file):
    try:
        response = requests.get(image_url)

        # Check for successful response
        if response.status_code == 200:
            saving_path = os.path.join(saving_folder_path, name_of_file)
            image = Image.open(BytesIO(response.content))
            image.save(saving_path)
            print(saving_path)
            return 0
        else:
            print("Response error, response status: " + str(response.status_code))
            return 1
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return 1
    except IOError as e:
        print(f"IO error: {e}")
        return 1

# Get command-line arguments
saving_folder_path = sys.argv[1]
name_of_file = sys.argv[2]
image_url = sys.argv[3]

# Call the download function
status = download_and_save(image_url, saving_folder_path, name_of_file)

# Exit based on status
sys.exit(status)
