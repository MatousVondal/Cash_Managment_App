import third_frame
import customtkinter
import home_frame
import navigation_frame
import second_frame

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Set the window properties
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
    # function controls which frame is shown acording 
    # click on buttons home or adding or vizualisation
    
        # set button color for selected button
        self.navigation.set_button_color(name)

        # Hide all frames
        self.home.grid_forget()
        self.second_frame.grid_forget()
        self.third_frame.grid_forget()

        # Show the selected frame
        if name == "home":
        # In this block is shown home frame
            self.home.grid(row=0, column=1, sticky="nsew")
        elif name == "frame_2":
        # When is frame changed to adding frame (second frame) this block is executed
        # As well has to be upload data from choosed file from home frame 
        # Data are saved in self.data 
        # Status is used for info if data are already uploaded
        # Method reload is used for reload data in treeview which are shown in second frame
            self.second_frame.grid(row=0, column=1, sticky="nsew")
            self.data, self.status = self.home.select_file()
            self.second_frame.data = self.data
            self.second_frame.status = self.status
            self.second_frame.reload()
        elif name == "frame_3":
        # When is frame changed to vizualisation frame (third frame) this block is executed
        # As well has to be upload data from choosed file from home frame
        # Data are saved in self.data
        # Method create_chart is used for create chart in third frame which visualise uploaded data from home frame data
            self.third_frame.grid(row=0, column=1, sticky="nsew")
            self.data, _ = self.home.select_file()   
            self.third_frame.data = self.data
            self.third_frame.create_chart("ALL")
            

if __name__ == "__main__":
    app = App()
    app.mainloop()
