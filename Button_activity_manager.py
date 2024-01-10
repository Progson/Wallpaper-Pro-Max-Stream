import threading
import sys
import os
import time
import execute_script as es

class Button_activity_manager:
    def __init__(self, socket_token, seconds_between_wallpapers):
        self.socket_token = socket_token
        self.seconds_between_wallpapers = seconds_between_wallpapers

    def set_seconds_between_wallpapers(self, seconds):
        self.seconds_between_wallpapers = seconds
        
    def set_socket_token(self, token):
        self.socket_token = token
        
    def start_connection(self,sio):
        connection_thread = threading.Thread(target=self.connect_and_wait_thread, args=(sio,))
        connection_thread.start()

    def receive_donation(self, donation_data,donations):
        download_set_thread = threading.Thread(target=self.recive_donation_thread, args=(donation_data,donations))
        download_set_thread.start()

    def start_downloading_and_setting_wallpaper(self, donations):
        download_set_thread = threading.Thread(target=self.download_first_donation_and_set_it_thread ,  args=(donations ,))
        download_set_thread.start()

    def disconnect_socketio(self, sio):
        sio.disconnect()
        sys.exit(0)

    def connect_and_wait_thread(self,sio):
        sio.connect(f'https://sockets.streamlabs.com?token={self.socket_token}', transports=['websocket'])
        sio.wait()
        
    def recive_donation_thread(self,donation_data,donations):
        donation_id = donation_data['id'] 
        donation_name = donation_data['name'] 
        donation_message = donation_data['message']
        donation_amount = donation_data['amount']
        result = es.run_script_in_this_folder("generate_wallpaper_from_prompt.py", [donation_message])
        if(result.returncode == 0):
            url = result.stdout.rstrip('\n')
            donations.access_donations("append",[donation_id,donation_name,donation_amount,donation_message,url])
            
    def download_first_donation_and_set_it_thread(self,donations):
        while True:
            if(donations.access_donations(action="get_length") > 0):
                donation = donations.access_donations(action="read",args=[0])            
                path_to_folder_with_wallpapers = os.path.join(os.path.dirname(os.path.abspath(__name__)) ,"generated_wallpapers")
                    
                saving_result = es.run_script_in_this_folder("save_image_from_url.py", [path_to_folder_with_wallpapers,str(donation[0])+".jpg",donation[4]])
                print(saving_result)
                if(saving_result.returncode != 0):
                    continue
                wallpaper_path = saving_result.stdout.rstrip('\n')
                setting_result = es.run_script_in_this_folder("set_image_as_wallpaper.py", [wallpaper_path])
                print(setting_result)
                if(setting_result.returncode != 0):
                    continue
                donations.access_donations(action="delete")
                print(donations.access_donations("copy"))
                time.sleep(self.seconds_between_wallpapers)
    