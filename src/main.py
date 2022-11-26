# Imports
import vtt
import time
from datetime import date
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.messagebox import showerror
from tkinter.messagebox import showinfo
import sqlite3 as sq

# Initialize tkinter GUI
window = tk.Tk()
window.title('VT Course Tracker')
window.geometry("400x250+500+300")

# Initialize database
conn = sq.connect('crns.db')
cur = conn.cursor()
cur.execute('create table if not exists crns (title text)')

# Store CRNS
crns = []

# Timetable Information
month = date.today().month
year = date.today().year

if 1 < month < 10:
    semester = vtt.Semester.FALL
elif 10 <= month <= 12:
    semester = vtt.Semester.SPRING
    year += 1
else:
    semester = vtt.Semester.SPRING

# GUI functions
def add_task():
    CRN = e1.get()
    if len(CRN) == 0:
        messagebox.showinfo('Empty Entry', 'Please enter a CRN')
    elif len(CRN) != 5:
        messagebox.showinfo('Invalid Entry', 'Please enter a valid CRN')
    elif CRN in crns:
        messagebox.showinfo('Duplicate Entry', 'Please enter a new CRN')
    elif vtt.get_crn(str(year), semester, CRN):
        crns.append(CRN)
        cur.execute('insert into crns values (?)', (CRN,))
        list_update()
        e1.delete(0, 'end')
    else:
        messagebox.showinfo('Invalid Entry', 'Please enter a valid CRN')

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
            cur.execute('delete from crns where title = ?', (val,))
    except:
        messagebox.showinfo('Cannot Delete', 'No CRN selected')

def clear_list():
    t.delete(0, 'end')

def start_tracking():
    window.destroy()

def retrieve_db():
    while len(crns) != 0:
        crns.pop()
    for row in cur.execute('select title from crns'):
        crns.append(row[0])

# Initialize geometry and retrieve database
l1 = ttk.Label(window, text='VT Course Tracker')
l2 = ttk.Label(window, text='Enter Course CRN: ')
e1 = ttk.Entry(window, width=21)
t = tk.Listbox(window, height=11, selectmode='SINGLE')
b1 = ttk.Button(window, text='Add CRN', width=20, command=add_task)
b2 = ttk.Button(window, text='Delete CRN', width=20, command=del_one)
b3 = ttk.Button(window, text='Start Tracking', width=20, command=start_tracking)

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
window.resizable(False, False)
window.mainloop()
conn.commit()
cur.close()

# Start tracking
class Course:
    def __init__(self, CRN):
        self.CRN = CRN
        self.course = vtt.get_crn(str(year), semester, CRN)
        self.open = self.course.has_open_spots()

CRNs = []
for i in crns:
    CRNs.append(Course(i))

print("[Course Tracking Started]")
while True:
    for crn in CRNs:
        if crn.course.has_open_spots() != crn.open:
            crn.open = crn.course.has_open_spots()
            root = tk.Tk()
            root.eval('tk::PlaceWindow %s center' % root.winfo_toplevel())
            if crn.open:
                showinfo(title="Course Open", message=str(crn.course.get_subject()) + ' ' + str(crn.course.get_code()) + ' CRN: ' + str(crn.CRN) + ' is now available.')
            else:
                showerror(title="Course Closed", message=str(crn.course.get_subject()) + ' ' + (crn.course.get_code()) + ' CRN: ' + str(crn.CRN) + ' is now closed.')
            root.destroy()

        time.sleep(1)