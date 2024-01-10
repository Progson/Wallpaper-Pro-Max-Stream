import sys
import os

if len(sys.argv) < 2:
    print("No argument recived")
else:
    script_directory = os.path.dirname(os.path.abspath(__file__))  # Pobierz ścieżkę do folderu bieżącego skryptu
    argument_to_save = sys.argv[1]

    file_path = os.path.join(script_directory, "code.txt")  # Łącz ścieżkę do folderu z nazwą pliku

    with open(file_path, "w") as file:
        file.write(argument_to_save)

    print(f"argument saved in file code.txt")
