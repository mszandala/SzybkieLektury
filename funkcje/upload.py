import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

def run():
    # Tworzymy ukryte główne okno tkintera
    root = tk.Tk()
    root.withdraw()

    # 1. Wybór pliku .smil
    smil_file = filedialog.askopenfilename(
        title="Wybierz plik SMIL",
        filetypes=[("SMIL files", "*.smil")]
    )
    if not smil_file:
        messagebox.showinfo("Info", "Nie wybrano pliku .smil")
        return

    # 2. Wybór wielu plików .xhtml
    xhtml_files = filedialog.askopenfilenames(
        title="Wybierz pliki XHTML",
        filetypes=[("XHTML files", "*.xhtml")]
    )
    if not xhtml_files:
        messagebox.showinfo("Info", "Nie wybrano żadnych plików .xhtml")
        return

    # 3. Utworzenie folderu temp (jeśli nie istnieje)
    temp_dir = os.path.join(os.getcwd(), "temp")
    os.makedirs(temp_dir, exist_ok=True)

    # 4. Kopiowanie pliku smil
    shutil.copy(smil_file, temp_dir)

    # 5. Kopiowanie plików xhtml
    for file in xhtml_files:
        shutil.copy(file, temp_dir)

    messagebox.showinfo("Sukces", f"Pliki zostały skopiowane do folderu:\n{temp_dir}")

