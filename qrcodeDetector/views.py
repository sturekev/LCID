import tkinter as tk
from tkinter import ttk
from tkinter import *
from detector1 import qr_scanner
import pycurl
from io import StringIO
import io



root = tk.Tk(className="Device simulation")
nb = ttk.Notebook(root)















#Frame 1 features functions

def hallAccessStart():
    token = qr_scanner()
    location = Combo.get()
    url = f"http://18.215.231.250/HallAccess/{location}/{token}/" 
    print(url)
    e = io.BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.WRITEFUNCTION, e.write)
    c.setopt(c.HTTPHEADER, ['Content-Type: application/json','Accept-Charset: UTF-8'])
    c.setopt(c.POSTFIELDS, '@request.json')
    c.perform()
    c.close()
    response = e.getvalue().decode('UTF-8')
    reslabel = ttk.Label(frame1, text = f"{response}")
    reslabel.pack(padx = 5, pady = 5)
    sizegrip = ttk.Sizegrip(frame1)
    sizegrip.pack(expand = True, fill = tk.BOTH, anchor = tk.SE)

def DiningService():
    token = qr_scanner()
    location = Combo.get()
    url = f"http://18.215.231.250/diningservice/caf/{token}/{location}/" 
    print(url)
    e = io.BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.WRITEFUNCTION, e.write)
    c.setopt(c.HTTPHEADER, ['Content-Type: application/json','Accept-Charset: UTF-8'])
    c.setopt(c.POSTFIELDS, '@request.json')
    c.perform()
    c.close()
    response = e.getvalue().decode('UTF-8')
    reslabel = ttk.Label(frame1, text = f"{response}")
    reslabel.pack(padx = 5, pady = 5)
    sizegrip = ttk.Sizegrip(frame1)
    sizegrip.pack(expand = True, fill = tk.BOTH, anchor = tk.SE)

# Frame 1, 2, and 3
frame1 = ttk.Frame(nb)
frame2 = ttk.Frame(nb)
frame3 = ttk.Frame(nb)

#Frame 1 outline
top = Tk()
top.geometry("200x150")
building = ['Farwell', 'Olson', 'Diseth', 'Miller', 'Brandt', 'Ylvisaker', 'Baker Village', 'College Apartments', 'Larsen', 'Prairie Houses', 'Sustainability House', 'Off-Campus Living', 'Roth']
Combo = ttk.Combobox(frame1, values = building)
Combo.set("Pick an Option")
Combo.pack(padx = 5, pady = 5)


#get content from api 
button= ttk.Button(frame1, text= "Start", command= hallAccessStart)
button.pack(padx = 10, pady = 10, side = tk.LEFT)

#Frame 2 layout

button= ttk.Button(frame1, text= "Start", command=DiningService)
button.pack(padx = 10, pady = 10, side = tk.LEFT)



frame1.pack(fill= tk.BOTH, expand=True)
frame2.pack(fill= tk.BOTH, expand=True)
frame3.pack(fill= tk.BOTH, expand=True)

nb.add(frame1, text = "Building Access Device")
nb.add(frame2, text = "Dining service device")
nb.insert("end", frame3, text = "Library lent scan")
nb.pack(padx = 5, pady = 5, expand = True)

root.mainloop()
