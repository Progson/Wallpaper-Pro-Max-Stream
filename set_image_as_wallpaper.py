import sys
import os
import ctypes
import win32con
from PIL import Image

if(len(sys.argv) !=2):
    print("Example usage: python name_of_script.py \"c:\\example\\folder\\to\\image\\example_image.jpg\"")
    sys.exit(2)
    

def set_wallpaper(path_to_image):
    try:
        if not os.path.exists(path_to_image):
            print(f"given path to image: {path_to_image} doesn't exist")
            return 2
        image = Image.open(path_to_image)
        ctypes.windll.user32.SystemParametersInfoW(win32con.SPI_SETDESKWALLPAPER, 0, path_to_image, win32con.SPIF_UPDATEINIFILE | win32con.SPIF_SENDCHANGE)
        print("wallpaper set succesfully")
        return 0
    except:
        print("there was a problem with setting up wallpaper")
        return 1

status = set_wallpaper(sys.argv[1])
sys.exit(status)