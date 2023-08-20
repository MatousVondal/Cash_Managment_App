import customtkinter
import os
import json
from datetime import datetime
from tkinter import messagebox

# Home frame class for the MoneySaver app 
class HomeFrame(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=0, fg_color="transparent")
        
        # Set the weight of the rows and columns
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # Set the current files
        # function upload all already created files and shown them in option menu
        self.current_files = self.take_alive_files()

        # create frame which holds all widgets in smaller rectangle
        self.frame = customtkinter.CTkFrame(self)
        self.frame.grid(row=0, column=0)

        # Set the weight of the rows and columns
        self.frame.rowconfigure((1,8),weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        # Create the widgets
        self.choose_file = customtkinter.CTkLabel(self.frame, text="Choose file:")
        self.choose_file.grid(row=1, column=0, padx=20, pady=(30,0), sticky="s")
        self.choose_file_opener = customtkinter.CTkOptionMenu(self.frame, width=180,
                                                              values=self.current_files, command=self.select_file)
        self.choose_file_opener.grid(row=2, column=0, padx=20, pady=5)
        self.label = customtkinter.CTkLabel(self.frame, text="or")
        self.label.grid(row=3, column=0, padx=40, pady=5)
        self.entry = customtkinter.CTkEntry(self.frame, width=180, placeholder_text="Author name")
        self.entry.grid(row=4, column=0, padx=40, pady=5)
        self.entry2 = customtkinter.CTkEntry(self.frame, width=180, placeholder_text="File name")
        self.entry2.grid(row=5, column=0, padx=40, pady=10)
        self.create_button = customtkinter.CTkButton(self.frame, width=180,
                                                     text="Create file", anchor="center", command=self.click_on_create)
        self.create_button.grid(row=6, column=0, padx=40, pady=(10,40))


    def click_on_create(self):
    # Function is called when is clicked on create button
    # Function create new file with name which is written in entry2 widget
    # And author name which is written in entry widget
    # Acording tamplete which is data variable is created new file
        author = self.entry.get()
        file_name = self.entry2.get()
 
        now = datetime.now()
        current_datetime_str = now.strftime("%d%m%Y%H%M%S")

        data = {"name_of_author": author,
                "file_name": file_name,
                "datetime": current_datetime_str,
                    "items":{
                        "index":[],
                        "date":[],
                        "type":[],
                        "price":[],
                        "income_expenditure":[],
                }
        }
        
        file_name = os.path.join("/path_to_files", file_name + '.json')
        with open(file_name, 'w') as f:
            json.dump(data, f, indent=4)

        self.refresh_values()
        self.entry.delete(0,10)
        self.entry2.delete(0,10)

        log_message = "The file was created successfully"
        messagebox.showinfo("Info", log_message)


    def select_file(self, name=None):
    # Function is called when is selected file from option menu
    # As well function is called when is clicked on adding button in navigation frame
    # By this function data are stored in self.data variable and can be used in other frames
        name = self.choose_file_opener.get()
        with open('/path_to_files'+ name + ".json", 'r') as f:
            data = json.load(f)
            status = True
        return data, status

    def base_file_name(self,file_name):
    # Function is used for take only base name of file without extension (.json)
    # This base name is used for option menu
        base_name = os.path.splitext(file_name)[0]
        return base_name
    
    def take_alive_files(self):
    # Function is used for take all files which are already created
    # And return them in list
    # This list is used for option menu    
        file_list = ["None"]
        for filename in os.listdir('/path_to_files'):
            if os.path.isfile(os.path.join('/path_to_files', filename)):
                file_list.append(self.base_file_name(filename))
        return file_list


    def refresh_values(self):
        updated_files = self.take_alive_files()

        # Update the values of the option menu
        self.choose_file_opener.configure(values=updated_files)
    
     


    

        
