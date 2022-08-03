import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3 as sq

# Initialize tkinter GUI
root = tk.Tk()
root.title('VT Course Tracker')
root.geometry("400x250+500+300")

# Initialize database
conn = sq.connect('crns.db')
cur = conn.cursor()
cur.execute('create table if not exists tasks (title text)')

# Store CRNS
crns = []

# GUI functions
def add_task():
    word = e1.get()
    if len(word) == 0:
        messagebox.showinfo('Empty Entry', 'Please enter a CRN')
    else:
        crns.append(word)
        cur.execute('insert into tasks values (?)', (word,))
        list_update()
        e1.delete(0, 'end')

def list_update():
    clear_list()
    for i in crns:
        t.insert('end', i)

def del_one():
    try:
        val = t.get(t.curselection())
        if val in crns:
            crns.remove(val)
            list_update()
            cur.execute('delete from tasks where title = ?', (val,))
    except:
        messagebox.showinfo('Cannot Delete', 'No CRN selected')

def clear_list():
    t.delete(0, 'end')

def bye():
    print(crns)
    root.destroy()

def retrieve_db():
    while len(crns) != 0:
        crns.pop()
    for row in cur.execute('select title from tasks'):
        crns.append(row[0])

# Initialize geometry and initialize database
l1 = ttk.Label(root, text='VT Course Tracker')
l2 = ttk.Label(root, text='Enter Course CRN: ')
e1 = ttk.Entry(root, width=21)
t = tk.Listbox(root, height=11, selectmode='SINGLE')
b1 = ttk.Button(root, text='Add CRN', width=20, command=add_task)
b2 = ttk.Button(root, text='Delete CRN', width=20, command=del_one)
b3 = ttk.Button(root, text='Start Tracking', width=20, command=del_one)

retrieve_db()
list_update()

l1.place(x=50, y=10)
l2.place(x=50, y=50)
e1.place(x=50, y=70)
b1.place(x=50, y=100)
b2.place(x=50, y=130)
b3.place(x=50, y=205)
t.place(x=220, y=50)

# Run GUI
root.resizable(False, False)
root.mainloop()
conn.commit()
cur.close()