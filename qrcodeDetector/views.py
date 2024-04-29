import tkinter as tk
from tkinter import ttk
from tkinter import *
from detector1 import qr_scanner
import pycurl
from io import StringIO
import io
import time


root = tk.Tk(className="Device simulation")
nb = ttk.Notebook(root)

#Frame 1 features functions
def change_color():
    colorboard1.config(bg="green")  # Change the background color of the frame

    # Schedule the color change back to red after a delay
    colorboard1.after(3000, lambda: colorboard1.config(bg="red")) # Change the background color back to red
    
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
    if response.split()[0] == '{"message":true}':
        print (True)
        colorboard1.config(bg="green")  # Change the background color of the frame

    # Schedule the color change back to red after a delay
        colorboard1.after(3000, lambda: colorboard1.config(bg="red"))

            

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
    if response.split()[0] == '{"message":true}':
        print (True)
        colorboard2.config(bg="green")  # Change the background color of the frame

    # Schedule the color change back to red after a delay
        colorboard2.after(3000, lambda: colorboard2.config(bg="red"))

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
Combo.pack(padx = 50, pady = 50)

colorboard1 = tk.Frame(frame1, width=200, height=200, bg="red")
colorboard1.pack()

#get content from api 
button= ttk.Button(frame1, text= "Start", command= hallAccessStart)
button.pack(padx = 50, pady = 50, side = tk.LEFT)

#Frame 2 layout

building = ["Caf"]
diningLocation = ttk.Combobox(frame2, values = building)
diningLocation.set("Pick an Option")
diningLocation.pack(padx = 50, pady = 50)

colorboard2 = tk.Frame(frame2, width=200, height=200, bg="red")
colorboard2.pack()

button= ttk.Button(frame2, text= "Start", command=DiningService)
button.pack(padx =50, pady = 50, side = tk.LEFT)

frame1.pack(fill= tk.BOTH, expand=True)
frame2.pack(fill= tk.BOTH, expand=True)

nb.add(frame1, text = "Building Access Device")
nb.add(frame2, text = "Dining service device")
nb.pack(padx = 100, pady = 100, expand = True)

root.mainloop()
