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
print(result.stdout)