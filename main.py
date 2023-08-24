import third_frame
import customtkinter
import home_frame
import navigation_frame
import second_frame


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Set the window properties
        self.status = None
        self.data = None
        self.title("MoneySaver")
        self.geometry(f"{1200}x{680}")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Create the frames
        self.home = home_frame.HomeFrame(self)
        self.home.grid(row=0, column=0)

        self.second_frame = second_frame.SecondFrame(self)
        self.second_frame.grid(row=0, column=0, sticky="nsew")

        self.third_frame = third_frame.ThirdFrame(self)
        self.third_frame.grid(row=0, column=0, sticky="nsew")

        self.navigation = navigation_frame.NavigationFrame(self, self.select_frame_by_name)
        self.navigation.grid(row=0, column=0, sticky="nsew")

        # Set the default frame
        self.select_frame_by_name("home")

    def select_frame_by_name(self, name):
        """
        Control the displayed frame based on button clicks for home, adding, or visualization.

        Args:
            name (str): The name of the frame to be displayed.

        Returns:
            None
        """
        # Set button color for the selected button
        self.navigation.set_button_color(name)

        # Hide all frames
        self.home.grid_forget()
        self.second_frame.grid_forget()
        self.third_frame.grid_forget()

        # Display the selected frame
        if name == "home":
            # Display the home frame
            self.home.grid(row=0, column=1, sticky="nsew")
        elif name == "frame_2":
            # Display the adding frame (second frame)
            # Also, data is uploaded from the chosen file in the home frame
            # The uploaded data is saved in self.data
            # The status variable indicates if data has already been uploaded
            # The reload method is used to refresh the data in the treeview shown in the second frame
            self.second_frame.grid(row=0, column=1, sticky="nsew")
            self.data, self.status = self.home.select_file()
            self.second_frame.data = self.data
            self.second_frame.status = self.status
            self.second_frame.reload()
        elif name == "frame_3":
            # Display the visualization frame (third frame)
            # Data is also uploaded from the chosen file in the home frame
            # The uploaded data is saved in self.data
            # The create_chart method is used to generate a chart in the third frame,
            # visualizing the data uploaded from the home frame
            self.third_frame.grid(row=0, column=1, sticky="nsew")
            self.data, _ = self.home.select_file()
            self.third_frame.data = self.data
            self.third_frame.create_chart("ALL")


if __name__ == "__main__":
    app = App()
    app.mainloop()
