
# === ui.py ===
import tkinter as tk
from tkinter import ttk, messagebox
import json
from data_handler import load_data, save_data

root = None
frame = None
tree = None
data = []

def setup_menu():
    menu = tk.Menu(root)
    root.config(menu=menu)
    menu.add_command(label="Frontend", command=load_ui)
    menu.add_command(label="Backend", command=load_backend)

def setup_frame():
    global frame
    frame = ttk.Frame(root, padding=10)
    frame.grid(row=0, column=0, sticky="nsew")
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

def load_ui():
    global tree
    clear_frame()

    tree = ttk.Treeview(frame, columns=("Nume", "Telefon"), show='headings')
    tree.heading("Nume", text="Nume")
    tree.heading("Telefon", text="Telefon")
    tree.grid(row=0, column=0, columnspan=3, sticky="nsew")

    ttk.Button(frame, text="Adaugă", command=add_entry).grid(row=1, column=0, pady=10)
    ttk.Button(frame, text="Editează", command=edit_entry).grid(row=1, column=1, pady=10)
    ttk.Button(frame, text="Șterge", command=delete_entry).grid(row=1, column=2, pady=10)

    frame.rowconfigure(0, weight=1)
    frame.columnconfigure(0, weight=1)

    refresh_tree()

def load_backend():
    clear_frame()
    ttk.Label(frame, text="Date brute (JSON)", font=("Arial", 14)).pack()
    text = tk.Text(frame, wrap=tk.WORD)
    text.pack(expand=True, fill=tk.BOTH)
    try:
        text.insert(tk.END, json.dumps(data, indent=4))
    except Exception as e:
        text.insert(tk.END, f"Eroare la afișare: {e}")

def clear_frame():
    if frame is None:
        return
    for widget in frame.winfo_children():
        widget.destroy()

def refresh_tree():
    for row in tree.get_children():
        tree.delete(row)
    for entry in data:
        if "nume" in entry and "telefon" in entry:
            tree.insert('', 'end', values=(entry["nume"], entry["telefon"]))

def add_entry():
    open_form()

def edit_entry():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Atenție", "Selectați o înregistrare!")
        return
    index = tree.index(selected)
    if index >= len(data):
        messagebox.showerror("Eroare", "Index invalid.")
        return
    open_form(index)

def delete_entry():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Atenție", "Selectați o înregistrare!")
        return
    index = tree.index(selected)
    if index >= len(data):
        messagebox.showerror("Eroare", "Index invalid.")
        return
    if messagebox.askyesno("Confirmare", "Sigur doriți să ștergeți această înregistrare?"):
        del data[index]
        save_data(data)
        refresh_tree()

def open_form(index=None):
    form = tk.Toplevel(root)
    form.title("Formular Contact")
    form.geometry("300x150")

    tk.Label(form, text="Nume:").pack(pady=5)
    nume_entry = tk.Entry(form)
    nume_entry.pack()

    tk.Label(form, text="Telefon:").pack(pady=5)
    telefon_entry = tk.Entry(form)
    telefon_entry.pack()

    if index is not None and index < len(data):
        entry = data[index]
        nume_entry.insert(0, entry.get("nume", ""))
        telefon_entry.insert(0, entry.get("telefon", ""))

    def save():
        nume = nume_entry.get().strip()
        telefon = telefon_entry.get().strip()
        if not nume or not telefon:
            messagebox.showerror("Eroare", "Completați toate câmpurile!")
            return
        if index is None:
            data.append({"nume": nume, "telefon": telefon})
        else:
            data[index] = {"nume": nume, "telefon": telefon}
        save_data(data)
        refresh_tree()
        form.destroy()

    ttk.Button(form, text="Salvează", command=save).pack(pady=10)