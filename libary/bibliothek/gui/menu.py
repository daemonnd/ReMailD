from tkinter import Tk, Menu

def öffne_datei(): pass
def speichern_unter(): pass
def konvertiere_bild(): pass
def konvertiere_audio(): pass
def zeige_info(): pass

root = Tk()
menubar = Menu(root)

# Datei-Menü
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Öffnen", command=öffne_datei)
filemenu.add_command(label="Speichern unter...", command=speichern_unter)
filemenu.add_separator()
filemenu.add_command(label="Beenden", command=root.quit)
menubar.add_cascade(label="Datei", menu=filemenu)

# Konvertieren-Menü
convertmenu = Menu(menubar, tearoff=0)
convertmenu.add_command(label="Bildformat ändern", command=konvertiere_bild)
convertmenu.add_command(label="Audioformat ändern", command=konvertiere_audio)
menubar.add_cascade(label="Konvertieren", menu=convertmenu)

# Hilfe-Menü
helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Über", command=zeige_info)
menubar.add_cascade(label="Hilfe", menu=helpmenu)

root.config(menu=menubar)
root.mainloop()