import tkinter as tk

def change_color():
    frame.config(bg="green")  # Change the background color of the frame

    # Schedule the color change back to red after a delay
    frame.after(3000, lambda: frame.config(bg="red"))

root = tk.Tk()

frame = tk.Frame(root, width=200, height=200, bg="red")
frame.pack()

button = tk.Button(root, text="Change Color", command=change_color)
button.pack()

root.mainloop()