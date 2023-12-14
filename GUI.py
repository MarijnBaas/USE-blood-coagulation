from tkinter import *
root = Tk()
root.title("Digital Twin GUI")
root.attributes('-fullscreen', True)



exit_button = Button(root, text="Exit", command=root.destroy)
exit_button.pack(pady=20)
root.mainloop()