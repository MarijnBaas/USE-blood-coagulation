import tkinter as tk
import tkinter.messagebox
import customtkinter
from PIL import Image, ImageTk

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Blood Coagulation Digital Twin GUI")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure((2), weight=1)
        self.grid_rowconfigure((0, 1), weight=0)

        # create tabview
        self.tabview = customtkinter.CTkTabview(self, anchor="nw", width = 1000, height = 450)
        self.tabview.grid(row=0, column=1, padx=(20, 0), sticky="nsew")

        self.tabview.add("Graph 1")
        self.tabview.add("Graph 2")
        self.tabview.add("Graph 3")
        self.tabview.tab("Graph 1").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview.tab("Graph 2").grid_columnconfigure(0, weight=1)

        image = customtkinter.CTkImage(light_image=Image.open("chart1.jpg"),
                             dark_image=Image.open("chart1.jpg"), size=(100, 100))

        # create a label with the image object and place it inside the tab
        label = customtkinter.CTkLabel(self.tabview.tab("Graph 1"), image=image)
        label.grid(row=0, column=0)

        self.input_frame = customtkinter.CTkFrame(self)
        self.input_frame.grid(row=0, column=2, padx=(20, 20), pady=(20, 0), sticky="nsew")

        # set default values


    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")


if __name__ == "__main__":
    app = App()
    app.mainloop()
