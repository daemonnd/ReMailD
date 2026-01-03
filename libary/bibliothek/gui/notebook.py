import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.geometry("600x400")

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

# Tabs als Frames anlegen
convert_tab = ttk.Frame(notebook)
upload_tab = ttk.Frame(notebook)

notebook.add(convert_tab, text="Convert")
notebook.add(upload_tab, text="Upload")

# Beispiel-Widgets
tk.Label(convert_tab, text="Hier konvertierst du Dateien").pack(padx=20, pady=20)
tk.Label(upload_tab, text="Hier lädst du Dateien hoch").pack(padx=20, pady=20)

notebook.selection = convert_tab  # Standardmäßig den Konvertieren-Tab auswählen

root.mainloop()
