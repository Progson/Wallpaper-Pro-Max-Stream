import subprocess
import sys
import os

def run_script(script_path,additional_arguments_values = []):
    script_values = additional_arguments_values
    script_values.insert(0, script_path)
    script_values.insert(0, sys.executable)
    result = subprocess.run(script_values, capture_output=True, text=True)
    return result

def run_script_in_this_folder(name_of_script, additional_arguments_values = []):
    path_to_generate_wallpaper_script = os.path.join(os.path.dirname(os.path.abspath(__file__)) ,name_of_script)
    return run_script(path_to_generate_wallpaper_script,additional_arguments_values)

def msgbox(text):
    run_script_in_this_folder("msg_box.py",additional_arguments_values=[text])
    
result = run_script_in_this_folder("generate_wallpaper_from_prompt.py", ["donation_message"])
path_to_folder_with_wallpapers = os.path.join(os.path.dirname(os.path.abspath(__name__)) ,"generated_wallpapers")
url = result.stdout
url = "https://img.freepik.com/premium-zdjecie/pies-animowany-obrazek-generatywna-sztuczna-inteligencja_786688-641.jpg"
saving_result = run_script_in_this_folder("save_image_from_url.py", [path_to_folder_with_wallpapers,"testy.jpg",url])
print(saving_result)
wallpaper_path = saving_result.stdout.rstrip('\n')
setting_result = run_script_in_this_folder("set_image_as_wallpaper.py", [wallpaper_path])
print(setting_result)
           
            