import customtkinter
import os
import json
from datetime import datetime
from tkinter import messagebox


# Home frame class for the MoneySaver app
def base_file_name(file_name):
    """
    Extract the base name of a file without its extension (.json).

    This function is used to extract the base name of a file without the extension (.json). The extracted base name
    is intended for use in the option menu.

    Args:
        file_name (str): The name of the file including its extension.

    Returns:
        str: The base name of the file without the extension.
    """
    base_name = os.path.splitext(file_name)[0]
    return base_name


def take_alive_files():
    """
    Retrieve a list of existing files.

    This function retrieves a list of all files that have been created and returns them in a list. The list is intended
    to be used for the option menu.

    Returns:
        list: A list containing the names of existing files.
    """
    file_list = ["None"]  # Initialize the list with a default option
    for filename in os.listdir('/path_to_files'):
        if os.path.isfile(os.path.join('/path_to_files', filename)):
            file_list.append(base_file_name(filename))
    return file_list

class HomeFrame(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=0, fg_color="transparent")

        # Set the weight of the rows and columns
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # Set the current files
        # function upload all already created files and shown them in option menu
        self.current_files = take_alive_files()

        # create frame which holds all widgets in smaller rectangle
        self.frame = customtkinter.CTkFrame(self)
        self.frame.grid(row=0, column=0)

        # Set the weight of the rows and columns
        self.frame.rowconfigure((1,8), weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        # Create the widgets
        self.choose_file = customtkinter.CTkLabel(self.frame, text="Choose file:")
        self.choose_file.grid(row=1, column=0, padx=20, pady=(30, 0), sticky="s")
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
        self.create_button.grid(row=6, column=0, padx=40, pady=(10, 40))

    def click_on_create(self):
        """
        Create a new file when the 'Create' button is clicked.

        Reads author name and file name from entry widgets, creates a new file using the provided data template,
        and saves it with the given name. Refreshes values, clears the entry widgets, and displays a success message.

        Args:
            None

        Returns:
            None
        """
        # Get author and file name from entry widgets
        author = self.entry.get()
        file_name = self.entry2.get()

        # Get current date and time
        now = datetime.now()
        current_datetime_str = now.strftime("%d%m%Y%H%M%S")

        # Prepare data template for the new file
        data = {
            "name_of_author": author,
            "file_name": file_name,
            "datetime": current_datetime_str,
            "items": {
                "index": [],
                "date": [],
                "type": [],
                "price": [],
                "income_expenditure": [],
            }
        }

        # Create a new file and save data
        file_name = os.path.join("/path_to_files", file_name + '.json')
        with open(file_name, 'w') as f:
            json.dump(data, f, indent=4)

        # Refresh values, clear entry widgets, and show success message
        self.refresh_values()
        self.entry.delete(0, 10)
        self.entry2.delete(0, 10)

        log_message = "The file was created successfully"
        messagebox.showinfo("Info", log_message)

    def select_file(self, name=None):
        """
        Retrieve data from the selected file.

        This function is triggered when a file is selected from the option menu or when the 'Adding' button in
        the navigation frame is clicked. The selected file's data is stored in the self.data variable for use in
        other frames.

        Args:
            name (str): The name of the selected file (optional).

        Returns:
            tuple: A tuple containing the loaded data from the file and a boolean status indicating if data were upload.
        """
        # If name is not provided as an argument, use the name from the option menu
        name = self.choose_file_opener.get()

        # Load data from the selected file
        with open('/path_to_files/' + name + ".json", 'r') as f:
            data = json.load(f)
            status = True  # Indicates success

        return data, status

    def refresh_values(self):
        """
        Refresh the values in the option menu.

        This function updates the values displayed in the option menu with the updated list of existing files.

        Args:
            None

        Returns:
            None
        """
        updated_files = take_alive_files()

        # Update the values of the option menu
        self.choose_file_opener.configure(values=updated_files)

