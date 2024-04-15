# open camera to detect qr code.
# Prerequisite: opencv-python

import cv2
import requests
import tkinter as tk
from tkinter import ttk
from tkinter import *
import pycurl
from io import StringIO
import io

BASE_URL = "http://18.215.231.250"  # Replace with the actual URL of your FastAPI server

def qr_scanner():
    # Create a new VideoCapture object
    cap = cv2.VideoCapture(0)

    # Check if the camera opened successfully
    if not cap.isOpened():
        print("Could not open camera")
        exit()

    # Initialize the QR code detector
    qr_detector = cv2.QRCodeDetector()

    while True:
        # Read a new frame from the camera
        ret, frame = cap.read()

        # Check if the frame was captured successfully
        if not ret:
            print("Failed to grab frame")
            break

        # Detect and decode the QR code in the frame
        data, bbox, _ = qr_detector.detectAndDecode(frame)

        # Check if a QR code was detected
        if (bbox is not None) and (data != ""):

            # Draw a bounding box around the QR code
            for i in range(3):
                #cv2.line(img, pt1, pt2, color[, thickness[, lineType[, shift]]])
                cv2.line(frame, tuple(map(int,bbox[0][i])), tuple(map(int,bbox[0][i+1])), (0, 255, 0),2 )    
            cv2.line(frame, tuple(map(int,bbox[0][-1])), tuple(map(int,bbox[0][0])), (0, 255, 0),2 )


        # Display the frame with the detected QR code (if any)
        cv2.imshow("QR Code Scanner", frame)
        if data:
                #print(f"Decoded Data: {data}")
                cv2.waitKey(200)
                cap.release()
                cv2.destroyAllWindows()
                # send_data()
                return data
        # Check if the 'q' key was pressed to exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            # Release the VideoCapture object and close all windows
            cap.release()
            cv2.destroyAllWindows()
            break




# print (response.getvalue())
# response.close()

root = tk.Tk()
frame= ttk.Frame(root)
def hallAccess():
   token = qr_scanner()
   location = Combo.get()
   print(token)
   print(location)
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
   if response["message"]:
       return response['message']
   elif response ['detail']['msg']:
       return response['detail']['msg']
   else: return response['detail']
   
   
def decrement():
   progressBar.step(-20)
   
def display():
   print(progressBar["value"])
   
top = root
top.geometry("200x150")
hallFrame  = Frame(top)
frame.pack()

building = ['Farwell', 'Olson', 'Diseth', 'Miller', 'Brandt', 'Ylvisaker', 'Baker Village', 'College Apartments', 'Larsen', 'Prairie Houses', 'Sustainability House', 'Off-Campus Living', 'Roth']

   
Combo = ttk.Combobox(frame, values = building)
Combo.set("Pick an Option")
Combo.pack(padx = 5, pady = 5)
progressBar= ttk.Progressbar(frame, mode='determinate')
progressBar.pack(padx = 10, pady = 10)

button= ttk.Button(frame, text= "Hall", command= hallAccess)
button.pack(padx = 10, pady = 10, side = tk.LEFT)

button= ttk.Button(frame, text= "Decrease", command= decrement)
button.pack(padx = 10, pady = 10, side = tk.LEFT)
button= ttk.Button(frame, text= "Display", command= display)
button.pack(padx = 10, pady = 10, side = tk.LEFT)

frame.pack(padx = 5, pady = 5)
root.mainloop()