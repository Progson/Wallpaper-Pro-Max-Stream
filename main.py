import requests
import sys
import json
import os
import subprocess
import socketio
import tkinter as tk
from tkinter import messagebox
import threading
import time

if len(sys.argv) == 1:
    print("Nie otrzymano kodu")
    sys.exit(2)
    
client_id = os.getenv("STREAMLAB_TAPETYPRO_CLIENT_ID")
client_secret = os.getenv("STREAMLAB_TAPETYPRO_CLIENT_SECRET")
sio = socketio.Client(logger=True, engineio_logger=True)

donations = []  #[1,name,amount,message]
donations_lock = threading.Lock()
urls_for_generated_wallpapers = []#[1,name,amount,message,url]
url_lock = threading.Lock()
donation_url_image = []
dui_lock = threading.Lock()


def access_donations(action="",args =[]):
    with donations_lock:
        if action == "get_length":
            return len(donations)
        if action == "delete":
            donations.pop(args[0])
        if action == "append":
            donations.append(args)
        if action == "read":
            return donations[args[0]]

def access_urls_for_generated_wallpapers(action="",args =[]):
    with url_lock:
        if action == "get_length":
            return len(urls_for_generated_wallpapers)
        if action == "delete":
            urls_for_generated_wallpapers.pop(args[0])
        if action == "append":
            urls_for_generated_wallpapers.append(args)
        if action == "read":
            return urls_for_generated_wallpapers[args[0]]
    
def access_donation_url_image(action="",args =[]):
    with url_lock:
        if action == "get_length":
            return len(donation_url_image)
        if action == "delete":
            donation_url_image.pop(args[0])
        if action == "append":
            donation_url_image.append(args)
        if action == "read":
            return donation_url_image[args[0]]

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

@sio.on('event')
def on_event(eventData):
    if eventData['type'] == 'donation':
        donation_data = eventData['message'][0]  
        donation_id = donation_data['id'] 
        donation_name = donation_data['name'] 
        donation_message = donation_data['message']
        donation_amount = donation_data['amount'] 
        access_donations("append",[donation_id,donation_name,donation_amount,donation_message])
        
@sio.on('connect')
def connect():
    print("connected")

@sio.on('message')
def event(data):
    print("hejka")
            

def run_script(script_path,additional_arguments_values = []):
    script_values = additional_arguments_values
    script_values.insert(0, script_path)
    script_values.insert(0, sys.executable)
    result = subprocess.run(script_values, capture_output=True, text=True)
    return result, result.returncode  

def run_script_in_this_folder(name_of_script, additional_arguments_values = []):
    path_to_generate_wallpaper_script = os.path.join(os.path.dirname(os.path.abspath(__file__)) ,name_of_script)
    return run_script(path_to_generate_wallpaper_script,additional_arguments_values)
   
   
def connect_and_wait(socket_token):
    sio.connect(f'https://sockets.streamlabs.com?token={socket_token}', transports=['websocket'])
    sio.wait()
    
def start_connection():
    code = sys.argv[1]
    access_token = get_access_token(code)
    socket_token = get_socket_token(access_token)
    connection_thread = threading.Thread(target=connect_and_wait, args=(socket_token ,))
    connection_thread.start()
    connect_button.pack_forget()
    
def disconnect_socketio():
    sio.disconnect()
    sys.exit(0)
    
def generation_on(stop_generation):
    while True:
        if(stop_generation.is_set()):
            stop_generation.clear()
            break
        row = access_donations("read",0)
        url = run_script_in_this_folder("generate_wallpaper.py", [str(row[3])])
        row.append(url)
        access_urls_for_generated_wallpapers("append",[row])
        access_donations("delete",[0])     
    
        
    
stop_generation = threading.Event()
def generate_wallpapers_switch_press():   
    switch_status_before_press =  generate_wallpapers_switch.cget("text")
    if switch_status_before_press == "ON":
        generate_wallpapers_switch.config(text="OFF")
        generate_wallpapers_switch.config(bg='red', fg='white')
        thread = threading.Thread(target=generation_on, args=(stop_generation,))
        thread.start()
    else:
        generate_wallpapers_switch.config(text="ON")
        generate_wallpapers_switch.config(bg='green', fg='white')
        stop_generation.set()

def downloading_switch_press():
    
    switch_status_before_press =  downloading_switch.cget("text")
    if switch_status_before_press == "ON":
        downloading_switch.config(text="OFF")
        downloading_switch.config(bg='red', fg='white')
    else:
        downloading_switch.config(text="ON")
        downloading_switch.config(bg='green', fg='white')
    
def setting_wallpapers_switch_press():
    switch_status_before_press =  setting_wallpapers_switch.cget("text")
    if switch_status_before_press == "ON":
        setting_wallpapers_switch.config(text="OFF")
        setting_wallpapers_switch.config(bg='red', fg='white')
    else:
        setting_wallpapers_switch.config(text="ON")
        setting_wallpapers_switch.config(bg='green', fg='white')

if __name__ == "__main__":
    app = tk.Tk()
    app.title("Menu")

    connect_button = tk.Button(app, text="start_connection", command=start_connection)
    connect_button.pack()
    
    generating_wallpaper_label = tk.Label(app, text="Generating wallpapers")
    generating_wallpaper_label.pack()
    generate_wallpapers_switch  = tk.Button(app,bg='green', fg='white',text = "ON", command=generate_wallpapers_switch_press)
    generate_wallpapers_switch.pack()
    
    downloading_label = tk.Label(app, text="downloading images")
    downloading_label.pack()
    downloading_switch  = tk.Button(app,bg='green', fg='white',text = "ON", command=downloading_switch_press)
    downloading_switch.pack()
    
    setting_wallpaper_label = tk.Label(app, text="setting wallpapers every: 10 sek")
    setting_wallpaper_label.pack()
    setting_wallpapers_switch  = tk.Button(app,bg='green', fg='white',text = "ON", command=setting_wallpapers_switch_press)
    setting_wallpapers_switch.pack()
    
    disconnect_button = tk.Button(app, text="disconnect", command=disconnect_socketio)
    disconnect_button.pack()
    
    app.mainloop()
    
    sio.disconnect()

    


'''
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

def move_donation_to_otherFolder():

    source_folder = os.path.dirname(os.path.abspath(__file__)) + "/donejty"
    destination_folder = os.path.dirname(os.path.abspath(__file__)) + "/../TapetyPro/donejty"
    
    for filename in os.listdir(source_folder):
        source_path = os.path.join(source_folder, filename)
        
        if os.path.isfile(source_path):
            destination_path = os.path.join(destination_folder, filename)
            shutil.move(source_path, destination_path)
            print(f'Przeniesiono: {source_path} do {destination_path}')

'''