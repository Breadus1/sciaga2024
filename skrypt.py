import tkinter as tk
import threading
import sqlite3
import os
import shutil

def main():
    if not os.path.exists('bazadanych.db'):
        conn = sqlite3.connect('bazadanych.db')
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tekst (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tresc TEXT
            )
        ''')

        with open('bazadanych.sql', 'r') as sql_file:
            sql_script = sql_file.read()
            cursor.executescript(sql_script)
        
        conn.commit()
        conn.close()

    conn = sqlite3.connect('bazadanych.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM tekst')
    results = cursor.fetchall()

    conn.close()

    if not os.path.exists('Test'):
        os.makedirs('Test')

    with open('Test/TekstTest.txt', 'w') as txt_file:
        for row in results:
            txt_file.write(f'{row[0]}: {row[1]}\n')

    print('Dane zapisane do pliku "Test/TekstTest.txt".')

def wykonaj_program():
    try:
        threading.Thread(target=main).start()
        label.config(text="Program wykonany poprawnie!")
    except Exception as e:
        label.config(text=f"Błąd: {e}")

def wycofaj_zmiany():
    usunieto_cos = False

    if os.path.exists('bazadanych.db'):
        os.remove('bazadanych.db')
        usunieto_cos = True

    if os.path.exists('Test'):
        shutil.rmtree('Test')
        usunieto_cos = True

    if usunieto_cos:
        label.config(text="Zmiany wycofane.")
    else:
        label.config(text="Nie znaleziono zmian.")

def zamknij_okno():
    root.destroy()

# okno
root = tk.Tk()
root.title("Moja Aplikacja")

# Przyciski
button_sciagaj = tk.Button(root, text="Ściągaj", command=wykonaj_program)
button_sciagaj.pack()

button_wycofaj = tk.Button(root, text="Wycofaj", command=wycofaj_zmiany)
button_wycofaj.pack()

button_quit = tk.Button(root, text="QUIT", command=zamknij_okno)
button_quit.pack()

# info
label = tk.Label(root, text="")
label.pack()

# Petla
root.mainloop()
