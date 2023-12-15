
import os
import re
import ctypes
import win32con
from openai import OpenAI
import requests
from PIL import Image
from io import BytesIO

def wygenerujTapete(givenPrompt):
    try:
        client = OpenAI()
        response = client.images.generate(
            model="dall-e-3",
            prompt = givenPrompt,
            size="1792x1024",
            quality="standard",
            n=1,
        )
        return response.data[0].url
    except:
        return False
        
    
    
def pobierz_i_zapisz_obraz_z_url(url, folder,name_of_file):
    try:
        odpowiedz = requests.get(url)
        if odpowiedz.status_code == 200:
            obraz = Image.open(BytesIO(odpowiedz.content))
            obraz.save(folder+"/"+name_of_file)
            return True
        else:
            return False
    except:
        return False
        
def ustaw_tapete(folder, name_of_file,resize = False):
    try:
        if not os.path.exists(folder+"/"+name_of_file):
            return False
        
        obraz = Image.open(folder+"/"+name_of_file)
        if resize:
            width_of_screen, height_of_screen = ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1)
            obraz = obraz.resize((width_of_screen, height_of_screen))
            obraz.save(folder+"/resized_"+name_of_file) 
            ctypes.windll.user32.SystemParametersInfoW(win32con.SPI_SETDESKWALLPAPER, 0, folder + "/resized_"+name_of_file, win32con.SPIF_UPDATEINIFILE | win32con.SPIF_SENDCHANGE)
        else:
            ctypes.windll.user32.SystemParametersInfoW(win32con.SPI_SETDESKWALLPAPER, 0, folder +"/"+ name_of_file, win32con.SPIF_UPDATEINIFILE | win32con.SPIF_SENDCHANGE)
        return True
    except:
        return False
        
def znajdz_najwieksza_liczbe_w_nazwach_plikow(folder):
    najwieksza_liczba = 0
    if os.path.isdir(folder):
        for plik in os.listdir(folder):
            if os.path.isfile(os.path.join(folder, plik)):
                liczby_w_nazwie = re.findall(r'\d+', plik)
                for liczba_str in liczby_w_nazwie:
                    liczba = int(liczba_str)
                    if liczba > najwieksza_liczba:
                        najwieksza_liczba = liczba
    return najwieksza_liczba

        
        
