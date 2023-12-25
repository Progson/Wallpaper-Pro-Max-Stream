import sys
import os
import requests
from PIL import Image
from io import BytesIO

if(len(sys.argv) != 4):
    print("Usage: python name_of_script.py \"c:\\saving_folder\" \"example_name_of_image.jpg\" \"http://example.image_url.com\"")
    sys.exit(2)

def download_and_save(image_url, saving_folder_path, name_of_file):
    try:
        response = requests.get(image_url)
        if response.status_code == 200:
            saving_path = os.path.join(saving_folder_path,name_of_file)
            image = Image.open(BytesIO(response.content))
            image.save(saving_path)
            print(saving_path)
            return 0
        else:
            print("response error, response status: "+ response.status_code)
            return 1
    except:
        print("couldn't connect to url")
        return 1

saving_folder_path = sys.argv[1]
name_of_file = sys.argv[2]
image_url = sys.argv[3]
status = download_and_save(image_url,saving_folder_path,name_of_file)
if status == 0:
    sys.exit(0)
elif status == 1:
    sys.exit(1)
    



