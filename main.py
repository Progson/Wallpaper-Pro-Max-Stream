#import shutil
import requests
import sys
import json
import os
import subprocess

client_id = os.getenv("STREAMLAB_TAPETYPRO_CLIENT_ID")
client_secret = os.getenv("STREAMLAB_TAPETYPRO_CLIENT_SECRET")

print("dzialam")

lastID = 0
access_token = ""

def get_donations( limit = 0, after = 0):
    global access_token
    url = "https://streamlabs.com/api/v2.0/donations"
    if limit:
        url = f"https://streamlabs.com/api/v2.0/donations?limit={limit}"
    if after:
        url = f"https://streamlabs.com/api/v2.0/donations?after={after}"
        
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    
    
    if response.status_code == 200:
        return response.json()
    else:
        return response.text 
    
def process_code(code):
    data = {
    "grant_type": "authorization_code",
    "client_id": client_id,
    "client_secret": client_secret,
    "redirect_uri": "http://127.0.0.1:80",
    "code": code
    }
    url = 'https://streamlabs.com/api/v2.0/token'
    headers = {
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest'
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    response_dict = json.loads(response.text)
    global access_token
    access_token = response_dict.get('access_token', None)

def zapisz_elementy_json(donation_dict, katalog_donacji="donejty"):
    sciezka_katalogu = os.path.dirname(os.path.abspath(__file__)) + "/" + katalog_donacji
    
    if not os.path.exists(sciezka_katalogu):
        os.makedirs(sciezka_katalogu)
        
    if 'data' in donation_dict:
        for i, element in enumerate(donation_dict['data']):
            donation_id = element.get('donation_id', None)

            nazwa_pliku = os.path.join(sciezka_katalogu, str(donation_id)+".json")

            with open(nazwa_pliku, 'w', encoding='utf-8') as plik:
                json.dump(element, plik, ensure_ascii=False, indent=4)

            print(f"Zapisano: {nazwa_pliku}")
    else:
        print("Brak 'data' w słowniku JSON.")

'''def move_donation_to_otherFolder():
    source_folder = os.path.dirname(os.path.abspath(__file__)) + "/donejty"
    destination_folder = os.path.dirname(os.path.abspath(__file__)) + "/../TapetyPro/donejty"
    
    for filename in os.listdir(source_folder):
        source_path = os.path.join(source_folder, filename)
        
        if os.path.isfile(source_path):
            destination_path = os.path.join(destination_folder, filename)
            shutil.move(source_path, destination_path)
            print(f'Przeniesiono: {source_path} do {destination_path}')'''

def generate_wallpaper(donation_id,prompt):
    path_to_generate_wallpaper_script = os.path.join(os.path.dirname(os.path.abspath(__file__)) ,"generate_wallpaper.py")
    result = subprocess.run([sys.executable, path_to_generate_wallpaper_script,str(donation_id), str(prompt)], capture_output=True, text=True)
    return result.returncode        
    
if __name__ == "__main__":
    if len(sys.argv) > 1:
        code = sys.argv[1]
        process_code(code)
        
        #donation_dict = get_donations(limit =  0)
        #lastID = (donation_dict.get('data',None)[-1].get('donation_id',None))
        #zapisz_elementy_json(donation_dict)
        #move_donation_to_otherFolder()
        result = generate_wallpaper(1, "czerwony pies z wielkim krokodylim czolem")
        
    else:
        print("Nie otrzymano kodu")

