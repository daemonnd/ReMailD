import tkinter as tk

class CustomMenuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Custom Menü")
        self.root.geometry("500x300")

        # Menüleiste als horizontaler Frame
        self.menu_bar = tk.Frame(self.root, bg="#333", height=30)
        self.menu_bar.pack(side="top", fill="x")

        # Inhalt darunter
        self.content = tk.Frame(self.root, bg="white")
        self.content.pack(fill="both", expand=True)

        # Menüeinträge
        self.add_menu_button("Datei", self.on_file)
        self.add_menu_button("Bearbeiten", self.on_edit)
        self.add_menu_button("Hilfe", self.on_help)

    def add_menu_button(self, text, command):
        btn = tk.Button(self.menu_bar, text=text, command=command, bg="#444", fg="white", bd=0)
        btn.pack(side="left", padx=5, pady=2)

    def on_file(self):
        self.show_content("Datei-Menü ausgewählt")

    def on_edit(self):
        self.show_content("Bearbeiten-Menü ausgewählt")

    def on_help(self):
        self.show_content("Hilfe-Menü ausgewählt")

    def show_content(self, text):
        for widget in self.content.winfo_children():
            widget.destroy()
        label = tk.Label(self.content, text=text, font=("Arial", 16), bg="white")
        label.pack(pady=20)

# Starten
if __name__ == "__main__":
    root = tk.Tk()
    app = CustomMenuApp(root)
    root.mainloop()
