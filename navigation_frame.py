import customtkinter

class NavigationFrame(customtkinter.CTkFrame):
    def __init__(self, parent, set_frame_callback):
        super().__init__(parent)

        # Set the callback for changing the frame
        # this method is create in main.py and called here
        self.set_frame_callback = set_frame_callback

        self.grid_rowconfigure(3, weight=1)

        # Create the widgets
        self.home_button = customtkinter.CTkButton(self, corner_radius=0, height=40, border_spacing=10, text="Home",
                                                   fg_color="transparent",
                                                   text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   anchor="w", command=self.home_button_event)
        self.home_button.grid(row=0, column=0, sticky="ew")

        self.frame_2_button = customtkinter.CTkButton(self, corner_radius=0, height=40, border_spacing=10, text="Adding",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="w",
                                                      command=self.frame_2_button_event)
        self.frame_2_button.grid(row=1, column=0, sticky="ew")

        self.frame_3_button = customtkinter.CTkButton(self, corner_radius=0, height=40, border_spacing=10, text="Vizualisation",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      anchor="w", command=self.frame_3_button_event)
        self.frame_3_button.grid(row=2, column=0, sticky="ew")

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self, values=["Dark", "Light"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=4, column=0, padx=20, pady=20, sticky="s")

    
    def home_button_event(self):
        self.set_frame_callback("home")

    def frame_2_button_event(self):
        self.set_frame_callback("frame_2")

    def frame_3_button_event(self):
        self.set_frame_callback("frame_3")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def set_button_color(self, name):
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
        self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")

    
    