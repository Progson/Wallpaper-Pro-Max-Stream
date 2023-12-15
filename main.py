import threading
import time
import requests
import sys
import json
import os

client_id = os.getenv("STREAMLAB_TAPETYPRO_CLIENT_ID")
client_secret = os.getenv("STREAMLAB_TAPETYPRO_CLIENT_SECRET")

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
    print("raz")
    response = requests.get(url, headers=headers)
    print("DWA")
    if response.status_code == 200:
        return response.json()  # Zwraca dane JSON z donacjami
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
    # Nagłówki żądania
    headers = {
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest'
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    response_dict = json.loads(response.text)
    global access_token
    access_token = response_dict.get('access_token', None)

def zapisz_elementy_json(donation_dict, katalog_donacji="donejty"):
    # Utwórz folder, jeśli nie istnieje
    # Ścieżka do katalogu, w którym znajduje się skrypt
    sciezka_katalogu = os.path.dirname(os.path.abspath(__file__)) + "/"+katalog_donacji
    
    if not os.path.exists(sciezka_katalogu):
        os.makedirs(sciezka_katalogu)

    # Sprawdź, czy 'data' istnieje w słowniku
    if 'data' in donation_dict:
        for i, element in enumerate(donation_dict['data']):
            # Tworzenie nazwy pliku dla każdego elementu
            donation_id = element.get('donation_id', None)

            nazwa_pliku = os.path.join(sciezka_katalogu, str(donation_id)+".json")

            # Zapisywanie elementu do pliku
            with open(nazwa_pliku, 'w', encoding='utf-8') as plik:
                json.dump(element, plik, ensure_ascii=False, indent=4)

            print(f"Zapisano: {nazwa_pliku}")
    else:
        print("Brak 'data' w słowniku JSON.")


# Funkcja, która uruchamia twoją funkcję co 5 sekund w tle
def execute_every_five_seconds():
    while True:
        time.sleep(5)  # Poczekaj 5 sekund przed kolejnym wykonaniem

# Uruchomienie funkcji w oddzielnym wątku
import shutil

def move_donation_to_otherFolder():
    source_folder = sciezka_katalogu = os.path.dirname(os.path.abspath(__file__)) + "/donejty"
    destination_folder = sciezka_katalogu = os.path.dirname(os.path.abspath(__file__)) + "/../TapetyPro/donejty"
    
    for filename in os.listdir(source_folder):
        source_path = os.path.join(source_folder, filename)

    # Upewnij się, że jest to plik, a nie katalog
        if os.path.isfile(source_path):
            destination_path = os.path.join(destination_folder, filename)
            # Przeniesienie pliku
            shutil.move(source_path, destination_path)
            print(f'Przeniesiono: {source_path} do {destination_path}')

def generate_wallpaper(prompt){
    
    
}    
    
if __name__ == "__main__":
    if len(sys.argv) > 1:
        code = sys.argv[1]
        process_code(code)
        donation_dict = get_donations(limit =  0)
        lastID = (donation_dict.get('data',None)[-1].get('donation_id',None))
        #lastID=182028640
        zapisz_elementy_json(donation_dict)
        move_donation_to_otherFolder()
        '''background_thread = threading.Thread(target=execute_every_five_seconds)
        background_thread.daemon = True  # Ustawienie wątku jako daemon (zakończy się wraz z głównym programem)
        background_thread.start()'''
        
        
        #donations = get_donations(access_token,after)
    else:
        print("Nie otrzymano kodu")

