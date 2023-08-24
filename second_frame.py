import customtkinter
from tkinter import ttk
from datetime import datetime
from tkinter import messagebox
import os
import json


def get_current_date():
    """
    Get the current date in the format dd.mm.yyyy.

    Returns:
        str: Current date in the format dd.mm.yyyy.
    """
    now = datetime.now()
    datetime_str = now.strftime("%d.%m.%Y")
    return datetime_str


class SecondFrame(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=0, fg_color="transparent")

        # Configure row and column weights for layout
        self.get_expendicure = None
        self.name = None
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(6, weight=1)

        # Place for data from home frame
        self.data = None
        self.status = None

        # Create the widgets
        self.in_or_ex_button = customtkinter.CTkOptionMenu(self,
                                                           width=150,
                                                           values=["Income", "Expenditure"],
                                                           command=self.income_or_expenditure)
        self.in_or_ex_button.grid(row=0, column=0, padx=20, pady=(20, 5))
        self.type_menu = customtkinter.CTkOptionMenu(self, width=150,
                                                     values=["Food", "Clothes", "Party", "Fuel", "Rent", "Sport"],
                                                     command=self.get_expendicure)
        self.type_menu.grid(row=1, column=0, padx=20, pady=5)

        self.entry = customtkinter.CTkEntry(self, width=150, placeholder_text="Amount of money (Kč)")
        self.entry.grid(row=2, column=0, padx=20, pady=5, sticky="nsew")

        self.date_entry = customtkinter.CTkEntry(self, placeholder_text=get_current_date())
        self.date_entry.grid(row=3, column=0, padx=20, pady=5, sticky="nsew")

        self.sidebar_button_1 = customtkinter.CTkButton(self, width=150, text="Add", command=self.create_record)
        self.sidebar_button_1.grid(row=4, column=0, padx=20, pady=5)

        self.button_3 = customtkinter.CTkButton(self, width=150, text="Save", command=self.save_file)
        self.button_3.grid(row=8, column=0, padx=20, pady=(5, 20))

        # Create the treeview
        self.view = ttk.Treeview(self,
                                 columns=("index", "date_time", "expenditure_or_income", "price", "note"),
                                 show="headings")
        self.view.grid(row=0, column=1, rowspan=10, padx=20, pady=20, sticky="nsew")

        # Configure the treeview
        self.view.heading("date_time", text="Date of create")
        self.view.heading("expenditure_or_income", text="Type")
        self.view.heading("price", text="Price (Kč)")
        self.view.heading("index", text="N.")
        self.view.heading("note", text="Expenditure or Income")

        # Set the weight of the rows and columns
        self.type_menu.configure(state="disabled")
        self.type_menu.set("-------")

    def income_or_expenditure(self, status):
        """
        Handle the action when the income or expenditure button is clicked.

        Args:
            status (str): The status of the button ("Income" or "Expenditure").

        Notes:
            - If the "Income" button is clicked, the type of expenditures is disabled.
            - If the "Expenditure" button is clicked, the type of expenditures is enabled with a default selection of "None".
        """
        if status == "Income":
            self.type_menu.configure(state="disabled")
            self.type_menu.set("-------")
        else:
            self.type_menu.configure(state="normal")
            self.type_menu.set("None")

    def reload(self):
        """
        Reload data in the treeview displayed in the second frame.

        Notes:
            - If there is no data, the treeview remains empty.
            - If data are present and have not been loaded before, they are loaded into the treeview.
              - The data is inserted in reverse order for better orientation.
            - The `status` attribute is used to indicate whether data have been previously uploaded.
            - After data loading, the `status` is set to False to avoid redundant loading in subsequent clicks.
        """
        data = self.data

        if not data["items"]["index"]:
            pass
        else:
            if self.status:
                for item in self.view.get_children():
                    self.view.delete(item)

                for i in data["items"]["index"]:
                    self.view.insert(parent="", index=0, values=(
                        i, data["items"]["date"][i], data["items"]["type"][i], data["items"]["price"][i],
                        data["items"]["income_expenditure"][i]))

                self.status = False
            else:
                log_message = "Data are already uploaded."
                messagebox.showinfo("Info", log_message)

    def create_record(self):
        """
        Create a new record based on the provided inputs and insert it into the treeview.

        If the date entry is empty, the current date is used. Otherwise, the date from the entry is used.
        The highest index is used for the index in the treeview.
        The income or expenditure type and corresponding name are determined based on the button selection.
        The new record is inserted into the treeview.

        Notes:
            - The `view` attribute refers to the treeview widget.
            - The `in_or_ex_button` attribute represents the income/expenditure button's state.
            - The `name` attribute holds the selected type of expenditure.
            - The `entry` attribute refers to the entry widget for price input.
            - The `date_entry` attribute refers to the entry widget for date input.
        """
        if self.date_entry.get() != "":
            now = datetime.now()
            datetime_str = now.strftime("%d.%m.%Y")
        else:
            datetime_str = self.date_entry.get()

        price = self.entry.get()
        highest_index = len(self.view.get_children())

        if self.in_or_ex_button.get() == "Income":
            in_or_ex = "1"
            type_of_ex_in = "Income"
        else:
            in_or_ex = "0"
            type_of_ex_in = self.name

        self.view.insert(parent="", index=0, values=(highest_index, datetime_str, type_of_ex_in, price, in_or_ex))
        self.entry.delete(0, 10)

    def get_expenditure(self, name):
        """
        Set the selected type of expenditure based on the provided name.

        This function is called when a type of expenditure button is clicked. The variable `name` is used to store
        the name of the selected type of expenditure, which is then used in the `create_record` method.

        Args:
            name (str): The name of the selected type of expenditure.
        """
        self.name = name

    def save_file(self):
        """
        Save the current data to a JSON file.

        This function saves the data currently displayed in the treeview to a JSON file. It extracts data from the treeview's
        values and saves them in reverse order to match the automatic reversal performed by the treeview.

        Raises:
            OSError: If there is an issue with the file writing process.
        """
        data = self.data
        author = data["author"]
        file_name = data["file_name"]
        datetime_str = data["datetime"]

        # Initialize lists to hold data from the treeview
        box1 = []
        box2 = []
        box3 = []
        box4 = []

        for item in self.view.get_children():
            # Extract values from the treeview item
            values = self.view.item(item, "values")
            date_time = values[1]
            expenditure = values[2]
            price = values[3]
            in_or_ex = values[4]

            # Append values to corresponding boxes
            box1.append(date_time)
            box2.append(expenditure)
            box3.append(price)
            box4.append(in_or_ex)

        index = list(range(0, len(box1)))

        # Create a data dictionary to save in JSON format
        data = {
            "author": author,
            "file_name": file_name,
            "datetime": datetime_str,
            "items": {
                "index": index,
                "date": box1[::-1],
                "type": box2[::-1],
                "price": box3[::-1],
                "income_expenditure": box4[::-1]
            }
        }

        file_name = os.path.join("/Users/matous/PycharmProjects/Cash_Managment_App/files", file_name + '.json')
        try:
            with open(file_name, 'w') as f:
                json.dump(data, f, indent=4)
                log_message = "Data are successfully saved."
                messagebox.showinfo("Info", log_message)
        except OSError as e:
            messagebox.showerror("Error", f"An error occurred while saving the data: {e}")

