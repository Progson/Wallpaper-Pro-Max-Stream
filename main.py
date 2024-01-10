import sys
import socketio
import time

import tokens 
import execute_script as es
import Donations_manager as dm
import Button_activity_manager as bam

'''if len(sys.argv) == 1:
    print("Nie otrzymano kodu")
    sys.exit(2)'''

donations = dm.Donation_manager()
button_manager = bam.Button_activity_manager("",1)

sio = socketio.Client(logger=True, engineio_logger=True)
@sio.on('event')
def on_event(eventData):
    if eventData['type'] == 'donation':
        donation_data = eventData['message'][0]  
        button_manager.receive_donation(donation_data,donations)        
        
@sio.on('connect')
def connect():
    print("connected")

@sio.on('message')
def event(data):
    ...

    
if __name__ == "__main__":
    code = tokens.get_code_from_file("code.txt") #sys.argv[1]
    access_token , socket_token = tokens.get_tokens(code)
    button_manager.set_socket_token(socket_token)
    button_manager.set_seconds_between_wallpapers(2)
    
    button_manager.start_connection(sio)
    button_manager.start_downloading_and_setting_wallpaper(donations)
    time.sleep(120)
    sys.exit(0)
    button_man.disconnect_socketio(sio)

    

