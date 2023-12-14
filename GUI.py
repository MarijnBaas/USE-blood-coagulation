from tkinter import *

# Create root window
root = Tk()
root.attributes('-fullscreen',True)

# Create two frames at the top
top_frame1 = Frame(root, bg="lightblue")
top_frame2 = Frame(root, bg="lightgreen")
bottom_frame = Frame(root, bg="lightpink")

# Place frames on the grid
top_frame1.grid(row=0, column=0, sticky="N")
top_frame2.grid(row=0, column=1, sticky="S")
bottom_frame.grid(row=1, column=0, columnspan=2, sticky="EW")



root.mainloop()