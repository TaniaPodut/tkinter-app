# === Structura fișiere ===
# - main.py             (inițializează aplicația)
# - data_handler.py     (gestionează citirea/scrierea JSON)
# - ui.py               (gestionează interfața grafică doar cu funcții)
# === main.py ===
import tkinter as tk
import ui
from data_handler import load_data

if __name__ == "__main__":
    try:
        ui.root = tk.Tk()
        ui.root.title("Aplicație CRUD - Contacte")
        ui.root.geometry("600x400")
        ui.data = load_data()

        ui.setup_menu()
        ui.setup_frame()
        ui.load_ui()

        ui.root.mainloop()
    except Exception as e:
        print("Eroare la rularea aplicației:", e)
