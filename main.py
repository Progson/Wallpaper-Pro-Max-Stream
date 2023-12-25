import requests
import sys
import json
import os
import subprocess
import socketio


client_id = os.getenv("STREAMLAB_TAPETYPRO_CLIENT_ID")
client_secret = os.getenv("STREAMLAB_TAPETYPRO_CLIENT_SECRET")
    
def get_access_token(code):    
    data = {
    "grant_type": "authorization_code",
    "client_id": client_id,
    "client_secret": client_secret,
    "redirect_uri": "http://127.0.0.1:80",
    "code": code
    }
    url = "https://streamlabs.com/api/v2.0/token"
    headers = {
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest'
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    response_dict = json.loads(response.text)
    return response_dict.get('access_token', None)   

def get_socket_token(access_token):  
    url = "https://streamlabs.com/api/v2.0/socket/token"
    headers = {"accept": "application/json",'Authorization': f'Bearer {access_token}'}

    response = requests.get(url, headers=headers)
    try:
        response_dict = json.loads(response.text)
        return response_dict.get('socket_token', None)
    except json.JSONDecodeError as e:
        print("nie dziala")
        print(response.text)
        return None


sio = socketio.Client(logger=True, engineio_logger=True)

@sio.on('event')
def on_event(eventData):
    if eventData['type'] == 'donation':
        donation_data = eventData['message'][0]  
        donation_id = donation_data['id']  
        donation_message = donation_data['message']
        donation_amount = donation_data['amount'] 
        donation_currency = donation_data['currency']
        #generate_wallpaper(donation_id,donation_message)
        run_script_in_this_folder("msg_box.py", [donation_message])
        
@sio.on('connect')
def connect():
    print("connected")

@sio.on('message')
def event(data):
    print("hejka")
    
def get_donations( access_token,limit = 0, after = 0):
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
        print("Brak 'data' w dictionary JSON.")

'''def move_donation_to_otherFolder():

    source_folder = os.path.dirname(os.path.abspath(__file__)) + "/donejty"
    destination_folder = os.path.dirname(os.path.abspath(__file__)) + "/../TapetyPro/donejty"
    
    for filename in os.listdir(source_folder):
        source_path = os.path.join(source_folder, filename)
        
        if os.path.isfile(source_path):
            destination_path = os.path.join(destination_folder, filename)
            shutil.move(source_path, destination_path)
            print(f'Przeniesiono: {source_path} do {destination_path}')

'''
def generate_wallpaper(donation_id,prompt):
    path_to_generate_wallpaper_script = os.path.join(os.path.dirname(os.path.abspath(__file__)) ,"generate_wallpaper.py")
    result = subprocess.run([sys.executable, path_to_generate_wallpaper_script,str(donation_id), str(prompt)], capture_output=True, text=True)
    return result.returncode        

def run_script(script_path,additional_arguments_values = []):
    script_values = additional_arguments_values
    script_values.insert(0, script_path)
    script_values.insert(0, sys.executable)
    result = subprocess.run(script_values, capture_output=True, text=True)
    return result, result.returncode  

def run_script_in_this_folder(name_of_script, additional_arguments_values = []):
    path_to_generate_wallpaper_script = os.path.join(os.path.dirname(os.path.abspath(__file__)) ,name_of_script)
    run_script(path_to_generate_wallpaper_script,additional_arguments_values)
    
if __name__ == "__main__":
    if len(sys.argv) > 1:
        code = sys.argv[1]
        access_token = get_access_token(code)
        socket_token = get_socket_token(access_token)
        #print(socket_token)
        
        sio.connect(f'https://sockets.streamlabs.com?token={socket_token}', transports=['websocket'])

        try:
            sio.wait()
        except KeyboardInterrupt:
            pass
            
    else:
        print("Nie otrzymano kodu")

