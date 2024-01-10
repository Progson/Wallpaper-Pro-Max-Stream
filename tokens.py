import json
import os
import requests

client_id = os.getenv("STREAMLAB_TAPETYPRO_CLIENT_ID")
client_secret = os.getenv("STREAMLAB_TAPETYPRO_CLIENT_SECRET")

def get_code_from_file(file_name):
    try:
        with open(file_name, "r") as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print("Plik 'code.txt' nie istnieje.")  

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

def get_tokens(code):
    access_token = get_access_token(code)
    socket_token = get_socket_token(access_token)
    return access_token,socket_token
    
