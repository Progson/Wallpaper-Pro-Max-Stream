import sys,os
import tkinter as tk
from tkinter import messagebox

def connect_to_server():
    print('connect')
    pass

def disconnect_from_server():
    # Add your disconnection code here
    pass

def perform_auto_action():
    # Add code for automatic action here
    pass

app = tk.Tk()
app.title("Menu App")

connect_button = tk.Button(app, text="Connect to Server", command=connect_to_server)
connect_button.pack()

disconnect_button = tk.Button(app, text="Disconnect from Server", command=disconnect_from_server)
disconnect_button.pack()

auto_action_button = tk.Button(app, text="Automatically Do Something", command=perform_auto_action)
auto_action_button.pack()

quit_button = tk.Button(app, text="Quit", command=app.quit)
quit_button.pack()

app.mainloop()
exit()


import wallpaper as wp
import os
import sys

folder_for_saving_wp = os.path.dirname(os.path.abspath(__file__)) + "/generated_wallpapers"
print(folder_for_saving_wp)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        donationID = sys.argv[1]
        prompt = sys.argv[2]

        name_of_file = str(donationID)+ ".jpg"
        image_url = wp.wygenerujTapete(prompt)
        if image_url == False:
            sys.exit(1)
        saving_result = wp.pobierz_i_zapisz_obraz_z_url(image_url,folder_for_saving_wp,name_of_file)
        if saving_result == False:
            sys.exit(2)
        wp_setting_result = wp.ustaw_tapete(folder_for_saving_wp,name_of_file)
        if wp_setting_result == False:
            sys.exit(3)
    else:
        sys.exit(4)

