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

'''if len(sys.argv) == 1:
    print("Nie otrzymano kodu")
    sys.exit(2)'''

client_id = os.getenv("STREAMLAB_TAPETYPRO_CLIENT_ID")
client_secret = os.getenv("STREAMLAB_TAPETYPRO_CLIENT_SECRET")
sio = socketio.Client(logger=True, engineio_logger=True)
seocnds_between_wallpapers = 2



'''Działanie
1. przychodzi donejt generuje sie dos niego url zapisuje się do kolejki
2. co 30 sekund pobiera się url i ustawia odrazu tapeta i kasuje z kolejki


'''

donations = [] #id,name,amount,prompt,url
donations_lock = threading.Lock()

def access_donations(action="",args =[]):
    with donations_lock:
        if action == "get_length":
            return len(donations)
        if action == "delete":
            if(len(args)==1):
                donations.pop(args[0])
            else:
                donations.pop()
        if action == "append":
            donations.append(args)
        if action == "read":
            return donations[args[0]]
        if action == "copy":
            copy = donations
            return copy
    
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
        print("socket token error ")
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
        result = run_script_in_this_folder("generate_wallpaper_from_prompt.py", [donation_message])
        if(result.returncode == 0):
            url = result.stdout.rstrip('\n')
            access_donations("append",[donation_id,donation_name,donation_amount,donation_message,url])
            print(access_donations("copy"))
        else:
            ...
            '''jak jest blad np safty policy'''
        
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
    return result

def run_script_in_this_folder(name_of_script, additional_arguments_values = []):
    path_to_script = os.path.join(os.path.dirname(os.path.abspath(__name__)) ,name_of_script)
    return run_script(path_to_script,additional_arguments_values)

def msgbox(text):
    run_script_in_this_folder("msg_box.py",additional_arguments_values=[text])
   
def disconnect_socketio():
    sio.disconnect()
    sys.exit(0)

def connect_and_wait(socket_token):
    sio.connect(f'https://sockets.streamlabs.com?token={socket_token}', transports=['websocket'])
    sio.wait()
    
def get_code_from_file(file_name):
    try:
        with open(file_name, "r") as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print("Plik 'code.txt' nie istnieje.")  
          
def get_tokens(code):
    access_token = get_access_token(code)
    socket_token = get_socket_token(access_token)
    return access_token,socket_token
    
def download_first_donation_and_set_it():
    while True:
        if(access_donations(action="get_length") > 0):
            donation = access_donations(action="read",args=[0])            
            path_to_folder_with_wallpapers = os.path.join(os.path.dirname(os.path.abspath(__name__)) ,"generated_wallpapers")
                
            saving_result = run_script_in_this_folder("save_image_from_url.py", [path_to_folder_with_wallpapers,str(donation[0])+".jpg",donation[4]])
            print(saving_result)
            if(saving_result.returncode != 0):
                continue
            wallpaper_path = saving_result.stdout.rstrip('\n')
            setting_result = run_script_in_this_folder("set_image_as_wallpaper.py", [wallpaper_path])
            print(setting_result)
            if(setting_result.returncode != 0):
                continue
            access_donations(action="delete")
            print(access_donations("copy"))
            time.sleep(seocnds_between_wallpapers)

def start_connection(socket_token):
    connection_thread = threading.Thread(target=connect_and_wait, args=(socket_token ,))
    connection_thread.start()
    
def start_downloading_and_setting_wallpaper():
    download_set_thread = threading.Thread(target=download_first_donation_and_set_it)
    download_set_thread.start()
    
    
if __name__ == "__main__":
    code = get_code_from_file("code.txt") #sys.argv[1]
    access_token , socket_token = get_tokens(code)
    start_connection(socket_token)
    start_downloading_and_setting_wallpaper()
    time.sleep(30)
    sio.disconnect()

    

