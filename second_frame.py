import customtkinter
from tkinter import ttk
from datetime import datetime
from tkinter import messagebox
import os
import json

class SecondFrame(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=0, fg_color="transparent")
        
        # Configure row and column weights for layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(6, weight=1)

        # Place for data from home frame
        self.data = None
        self.status = None

        # Create the widgets
        self.in_or_ex_button = customtkinter.CTkOptionMenu(self, width=150,
                                                           values=["Income","Expenditure"], command=self.income_or_expenditure)
        self.in_or_ex_button.grid(row=0, column=0, padx=20, pady=(20,5))
        self.type_menu = customtkinter.CTkOptionMenu(self,  width=150,
                                                     values=["Food","Clothes","Party","Fuel","Rent","Sport"],
                                                     command=self.get_expendicure)
        self.type_menu.grid(row=1, column=0, padx=20, pady=5)

        self.entry = customtkinter.CTkEntry(self, width=150, placeholder_text="Amount of money (Kč)")
        self.entry.grid(row=2, column=0, padx=20, pady=5, sticky="nsew")

        self.date_entry = customtkinter.CTkEntry(self, placeholder_text=self.get_current_date())
        self.date_entry.grid(row=3, column=0, padx=20, pady=5, sticky="nsew")

        self.sidebar_button_1 = customtkinter.CTkButton(self, width=150, text="Add", command=self.create_record)
        self.sidebar_button_1.grid(row=4, column=0, padx=20, pady=5)
        
        self.button_3 = customtkinter.CTkButton(self, width=150, text="Save", command=self.save_file)
        self.button_3.grid(row=8, column=0, padx=20, pady=(5,20))

        # Create the treeview
        self.view = ttk.Treeview(self, columns=("index","date_time","expenditure_or_income","price","note"), show="headings")
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

    def get_current_date(self):
    # Function return current date in format dd.mm.yyyy    
        now = datetime.now()
        datetime_str = now.strftime("%d.%m.%Y")
        return datetime_str

    def income_or_expenditure(self, status):
    # Function is called when is clicked on income or expenditure button
    # If is clicked on income button then is type of expenditures is disabled    
        if status == "Income":
            self.type_menu.configure(state="disabled")
            self.type_menu.set("-------")
        else:
            self.type_menu.configure(state="normal")
            self.type_menu.set("None")

    def reload(self):
    # Function is called when is clicked on adding button in navigation frame
    # Function is used for reload data in treeview which are shown in second frame
        data = self.data

        if data["items"]["index"] == []:
            pass
        # if data are empty then is treeview empty
        else:
            if self.status == True:
                for item in self.view.get_children():
                    self.view.delete(item)
                # if data are not empty then are data in treeview
                # data are loaded from self.data which are saved from home frame
                # data are loaded in reverse order because of better orientation
                # Status is used for info if data are already uploaded    
                
                for i in data["items"]["index"]:
                    self.view.insert(parent="",index=0,values=(i,data["items"]["date"][i],data["items"]["type"][i],data["items"]["price"][i],data["items"]["income_expenditure"][i]))
                # Status is changed to False because data are already uploaded
                # In next click data are not uploaded again    
                self.status = False

            else:
                log_message = "Data are already upload."
                messagebox.showinfo("Info", log_message)

    def create_record(self):
        if self.date_entry.get() != "":
            now = datetime.now()
            datetime_str = now.strftime("%d.%m.%Y")
            # if date entry is empty then is used current date
        else:
            datetime_str = self.date_entry.get()
            # if date entry is not empty then is used date from date entry
        price = self.entry.get()
        highest_index = len(self.view.get_children())
        # highest index is used for index in treeview
     
        if self.in_or_ex_button.get() == "Income":
            in_or_ex = "1"
            type_of_ex_in = "Income"
        else:
            in_or_ex = "0"
            type_of_ex_in = self.name

        self.view.insert(parent="",index=0,values=(highest_index,datetime_str,type_of_ex_in,price,in_or_ex))
        # data are inserted in treeview

        self.entry.delete(0,10)

    def get_expendicure(self,name):
        # Function is called when is clicked on type of expenditure button
        # Variable name is used for take name of type of expenditure in create_record method
        self.name = name
    
    def save_file(self):
        data = self.data
        author = data["author"]
        file_name = data["file_name"]
        datetime_str = data["datetime"]
        
        # into box1, box2, box3, box4 are saved data from treeview
        box1 = []
        box2 = []
        box3 = []
        box4 = [] 
 
        for item in self.view.get_children():
        # data are upload from treeview into box1, box2, box3, box4
            values = self.view.item(item, "values")
            date_time = values[1]  
            expenditure = values[2]  
            price = values[3]
            in_or_ex = values[4]
        
            box1.append(date_time)
            box2.append(expenditure)
            box3.append(price)  
            box4.append(in_or_ex)
        
        index = list(range(0,len(box1)))
        
        # Data are saved in data variable
        # Data are saved in reverse order because of treeview upload data automatically reveresed
        # and if data are not saved in reverse order then data in file will be reveresed than before
        data = {"author": author,
                "file_name": file_name,
                "datetime": datetime_str,
                    "items":{
                        "index":index,
                        "date":box1[::-1],
                        "type":box2[::-1],
                        "price":box3[::-1],
                        "income_expenditure":box4[::-1]
                }
        }

        file_name = os.path.join("/Users/matous/Desktop/MoneySaver/files", file_name + '.json')
        with open(file_name, 'w') as f:
            json.dump(data, f, indent=4)

            log_message = "Data are successfully saved."
            messagebox.showinfo("Info", log_message)

