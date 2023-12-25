from PIL import Image
import ctypes
import sys
import os

if len(sys.argv) != 2 and len(sys.argv) != 4:
    print("Example usage: python name_of_script.py path_to_image [px_width] [px_height]")
    sys.exit(2)
try:
    width_of_screen, height_of_screen = ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1)
except:
    print("couldn't recive screen width and height")
    sys.exit(1)
    
if len(sys.argv) == 4:
    width_of_screen = int(sys.argv[2])
    height_of_screen = int(sys.argv[3])
path_to_image = sys.argv[1]

if not os.path.exists(path_to_image):
    print("recived path doesn't exist")
    sys.exit(2)
    
try:
    image = Image.open(path_to_image)
except:
    print("couldn't open the image")
    sys.exit(1)
    
try:
    image = image.resize((width_of_screen, height_of_screen))
except:
    print("couldn't resize the image")
    sys.exit(1)

try:
    image.save(path_to_image) 
except:
    print("couldn't save the image")
    sys.exit(1)
    
sys.exit(0)

         