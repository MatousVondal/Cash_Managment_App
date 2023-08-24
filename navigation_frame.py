import customtkinter


def change_appearance_mode_event(new_appearance_mode: str):
    """
    Function to handle the event of changing the appearance mode.

    Args:
        new_appearance_mode (str): The new appearance mode ("Dark" or "Light").
    """
    customtkinter.set_appearance_mode(new_appearance_mode)


class NavigationFrame(customtkinter.CTkFrame):
    """
    A frame containing navigation buttons for switching between frames.

    This frame displays buttons for the "Home", "Adding", and "Visualization" frames,
    allowing the user to switch between different views of the application.
    """

    def __init__(self, parent, set_frame_callback):
        super().__init__(parent)

        # Set the callback for changing the frame
        self.set_frame_callback = set_frame_callback

        self.grid_rowconfigure(3, weight=1)

        # Create the widgets
        self.home_button = customtkinter.CTkButton(self, corner_radius=0, height=40, border_spacing=10, text="Home",
                                                   fg_color="transparent",
                                                   text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   anchor="w", command=self.home_button_event)
        self.home_button.grid(row=0, column=0, sticky="ew")

        self.frame_2_button = customtkinter.CTkButton(self, corner_radius=0, height=40, border_spacing=10,
                                                      text="Adding",
                                                      fg_color="transparent", text_color=("gray10", "gray90"),
                                                      hover_color=("gray70", "gray30"), anchor="w",
                                                      command=self.frame_2_button_event)
        self.frame_2_button.grid(row=1, column=0, sticky="ew")

        self.frame_3_button = customtkinter.CTkButton(self, corner_radius=0, height=40, border_spacing=10,
                                                      text="Visualization",
                                                      fg_color="transparent", text_color=("gray10", "gray90"),
                                                      hover_color=("gray70", "gray30"),
                                                      anchor="w", command=self.frame_3_button_event)
        self.frame_3_button.grid(row=2, column=0, sticky="ew")

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self, values=["Dark", "Light"],
                                                                command=change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=4, column=0, padx=20, pady=20, sticky="s")

    def home_button_event(self):
        """
        Event handler for the Home button click.
        """
        self.set_frame_callback("home")

    def frame_2_button_event(self):
        """
        Event handler for the Adding button click.
        """
        self.set_frame_callback("frame_2")

    def frame_3_button_event(self):
        """
        Event handler for the Visualization button click.
        """
        self.set_frame_callback("frame_3")

    def set_button_color(self, name):
        """
        Set the color of navigation buttons based on the active frame name.

        Args:
            name (str): The name of the active frame.
        """
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
        self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")
