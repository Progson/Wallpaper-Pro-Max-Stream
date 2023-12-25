import tkinter as tk
from tkinter import messagebox
import sys

root = tk.Tk()
root.withdraw()  # Ukryj główne okno
komunikat = "żyje"
if(len(sys.argv) > 1):
    komunikat = sys.argv[1]
messagebox.showinfo("Komunikat", komunikat)

# Zamknij główne okno (opcjonalnie)
root.destroy()