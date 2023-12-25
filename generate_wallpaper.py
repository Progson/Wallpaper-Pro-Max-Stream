import sys,os
import tkinter as tk
from tkinter import messagebox


root = tk.Tk()
root.withdraw() 

prompt = ''
if len(sys.argv) > 1:
        donationID = sys.argv[1]
        prompt = sys.argv[2]
        messagebox.showinfo("Komunikat", prompt)
root.destroy()
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

