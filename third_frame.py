import customtkinter
import pandas as pd
from charts import Chart, HistogramBuilder, MoneyBalancePlotter


class ThirdFrame(customtkinter.CTkFrame):
# this class is used for vizualisation of data
# in this frame are shown charts and statistics
# data are loaded from self.data which are saved from home frame

    def __init__(self, parent):
        super().__init__(parent, corner_radius=0, fg_color="transparent")
        self.initialize_ui()

    def initialize_ui(self):
        # Configure row and column weights for layout
        self.rowconfigure(6, weight=1)
        self.columnconfigure(1, weight=1)
        
        # Create the tab view and other UI elements
        self.create_tabview()
        self.create_type_menu()
        self.create_statistics_labels()

        # Initialize instance variables
        self.data = None
        self.chart = Chart(self.tabview, self.data, None)
        

     # Create the tab view widget
    def create_tabview(self):
        self.tabview = customtkinter.CTkTabview(self, command=self.tabClick_event)
        self.tabview.grid(row=0, column=1, padx=(0, 20), pady=20, rowspan=7, sticky="nsew")
        tab_names = ["TimePlot", "HistogramPlot", "MoneyBalance"]
        for tab_name in tab_names:
            self.tabview.add(tab_name)
            self.tabview.tab(tab_name).grid_columnconfigure(0, weight=1)
    
    def tabClick_event(self):
        state = self.tabview.get()
        if state == "TimePlot":
            # when is active tab TimePlot then is enabled type menu
            # due ti this is possible to choose type of expenditure
            # in other tabs is type menu disabled because there is no need to choose type of expenditure
            self.type_menu.configure(state="normal")
            self.type_menu.set(self.tab_menu_state) # Set the type menu to the last selected value
            
        elif state == "HistogramPlot":
            # If is active tab HistogramPlot then is disabled type menu
            # In this state is build histogram plot by HistogramBuilder class

            self.type_menu.configure(state="disabled")
            if hasattr(self, 'hist'):
                # If is already created histogram plot then is destroyed
                # This block is used for update histogram plot
                # Old plot is destroyed and new plot is created
                self.hist.canvas.get_tk_widget().pack_forget()  # Destroy the existing chart

            self.hist = HistogramBuilder(self.tabview, self.data)
            self.type_menu.set("ALL")

        elif state == "MoneyBalance":
            # Everything is same as in HistogramPlot tab
            self.type_menu.configure(state="disabled")
            if hasattr(self, 'money_balance'):
                self.money_balance.canvas.get_tk_widget().pack_forget()  # Destroy the existing chart
            self.money_balance = MoneyBalancePlotter(self.tabview, self.data)
            self.type_menu.set("ALL")

    # Create the drop-down menu for selecting expenditure type
    def create_type_menu(self):
        values = ["ALL", "Food", "Clothes", "Party", "Fuel", "Rent", "Sport"]
        self.type_menu = customtkinter.CTkOptionMenu(self, values=values, command=self.create_chart)
        self.type_menu.grid(row=1, column=0, padx=20, pady=(36, 0), sticky="nsew")

    # Create the labels for displaying statistics
    def create_statistics_labels(self):

        self.frame = customtkinter.CTkFrame(self)
        self.frame.grid(row=5, column=0, padx=20, pady=20, rowspan=4, sticky="nsew")
        
        # Configure row and column weights for layout
        self.label1 = customtkinter.CTkLabel(self.frame, text="STATISTICS", font=("Helvetica", 13, "bold"),bg_color="transparent")
        self.label1.grid(row=0, column=0, padx=40, pady=(0,10), sticky="nsew")
        self.label01 = customtkinter.CTkLabel(self.frame, text="----------------------------------------------", font=("Helvetica", 10, "bold"), bg_color="transparent")
        self.label01.grid(row=1, column=0, padx=10, pady=(0,10), sticky="w")
        self.label0 = customtkinter.CTkLabel(self.frame, text="-Expendicures", font=("Helvetica", 10, "bold"),bg_color="transparent")
        self.label0.grid(row=2, column=0, padx=10, pady=(0,10), sticky="w")
        self.label2 = customtkinter.CTkLabel(self.frame, text="MAX by DAY:", font=("Helvetica", 10, "bold"), bg_color="transparent")
        self.label2.grid(row=3, column=0,padx=10, pady=(0,10), sticky="w")
        self.label3 = customtkinter.CTkLabel(self.frame, text="MAX by CATEGORY:", font=("Helvetica", 10, "bold"),bg_color="transparent")
        self.label3.grid(row=4, column=0, padx=10, pady=(0,10), sticky="w")
        self.label4 = customtkinter.CTkLabel(self.frame, text="MONTH Average:", font=("Helvetica", 10, "bold"), bg_color="transparent")
        self.label4.grid(row=5, column=0, padx=10, pady=(0,10), sticky="w")
        self.label5 = customtkinter.CTkLabel(self.frame, text="TOTAL:", font=("Helvetica", 10, "bold"), bg_color="transparent")
        self.label5.grid(row=6, column=0, padx=10, pady=(0,10), sticky="w")

        # Configure row and column weights for layout
        self.label02 = customtkinter.CTkLabel(self.frame, text="----------------------------------------------", font=("Helvetica", 10, "bold"), bg_color="transparent")
        self.label02.grid(row=7, column=0, padx=10, pady=(0,10), sticky="w")
        self.label6 = customtkinter.CTkLabel(self.frame, text="-Income", font=("Helvetica", 10, "bold"), bg_color="transparent")
        self.label6.grid(row=8, column=0, padx=10, pady=(0,10), sticky="w")
        self.label7 = customtkinter.CTkLabel(self.frame, text="MAX by MONTH:", font=("Helvetica", 10, "bold"), bg_color="transparent")
        self.label7.grid(row=9, column=0,padx=10, pady=(0,10), sticky="w")
        self.label8 = customtkinter.CTkLabel(self.frame, text="MONTH Average:", font=("Helvetica", 10, "bold"), bg_color="transparent")
        self.label8.grid(row=10, column=0, padx=10, pady=(0,10), sticky="w")
        self.label9 = customtkinter.CTkLabel(self.frame, text="TOTAL:", font=("Helvetica", 10, "bold"), bg_color="transparent")
        self.label9.grid(row=11, column=0, padx=10, pady=(0,10), sticky="w")
        
     # Create the chart
    def create_chart(self, expenditure):
    # this method is called when is clicked on vizualisation tab in navigation frame
        if hasattr(self, 'chart'):
            self.chart.canvas.get_tk_widget().pack_forget()  # Destroy the existing chart

        self.chart = Chart(self.tabview, self.data, expenditure)

        # Update the statistics labels
        data = pd.DataFrame(self.data["items"])
        df_exp = data[data['income_expenditure'] == "0"]
        df_in = data[data['income_expenditure'] == "1"]

        self.label2.configure(text=f"MAX by DAY: {self.max_expenditure_per_day(df_exp)}")
        self.label3.configure(text=f"MAX by Category: {self.max_expenditure_by_category(df_exp)}")
        self.label4.configure(text=f"MONTH Average: {self.avg_expenditure_per_month(df_exp)}")
        self.label5.configure(text=f"TOTAL: {self.total_spending(df_exp)}")

        self.label7.configure(text=f"MAX by MONTH: {self.month_max(df_in)}")
        self.label8.configure(text=f"MONTH Average: {self.month_avg(df_in)}")
        self.label9.configure(text=f"TOTAL: {self.total_income(df_in)}")

        self.tab_menu_state = self.type_menu.get() # Save the current state of the type menu for return to TimePlot tab (Tabclick_event METHOD)

    # Calculate statistics
    def max_expenditure_per_day(self, df):
        df = self.prepare_data(df)
        df['date'] = df['date'].dt.strftime('%d.%m')
        max_expenditure = df.groupby('date')['price'].sum()
        max_day = max_expenditure.idxmax()
        max_value = max_expenditure.max()
        return f"{self.format_number_with_spaces(max_value)} ({max_day})"

    def max_expenditure_by_category(self, df):
        df = self.prepare_data(df)
        max_expenditure = df.groupby('type')['price'].sum()
        max_category = max_expenditure.idxmax()
        max_value = max_expenditure.max()
        return f"{self.format_number_with_spaces(max_value)} ({max_category})"

    def avg_expenditure_per_month(self, df):
        df = self.prepare_data(df)
        df['date'] = df['date'].dt.strftime('%m')
        month_sum = df.groupby('date')['price'].sum()
        avg_expenditure = month_sum.mean()
        return f"{self.format_number_with_spaces(round(avg_expenditure))}"

    def total_spending(self, df):
        df = self.prepare_data(df)
        total = df["price"].sum()
        return f"{self.format_number_with_spaces(total)}"
    
    def total_income(self, df):
        df = self.prepare_data(df)
        total = df["price"].sum()
        return f"{self.format_number_with_spaces(total)}"
    
    def month_max(self, df):
        df = self.prepare_data(df)
        df['date'] = df['date'].dt.strftime('%m')
        month_sum = df.groupby('date')['price'].sum()
        max_month = month_sum.idxmax()
        max_value = month_sum.max()
        return f"{self.format_number_with_spaces(max_value)} ({max_month})"
    
    def month_avg(self, df):    
        df = self.prepare_data(df)
        df['date'] = df['date'].dt.strftime('%m')
        month_sum = df.groupby('date')['price'].sum()
        avg_month = month_sum.mean()
        return f"{self.format_number_with_spaces(round(avg_month))}"

    def prepare_data(self, df):
        new = df.copy()
        new['price'] = pd.to_numeric(new['price'], errors='coerce')
        new['date'] = pd.to_datetime(new['date'], format='%d.%m.%Y')
        return new
    
    def format_number_with_spaces(self, number):
        # Convert the number to a string and reverse it
        num_str = str(number)[::-1]
        
        # Create a list to hold the formatted parts
        formatted_parts = []

        # Iterate through the string in chunks of 3 characters
        for i in range(0, len(num_str), 3):
            chunk = num_str[i:i+3][::-1]  # Get the reversed chunk of 3 characters
            formatted_parts.append(chunk)

        # Reverse the formatted parts and join them with spaces
        formatted_number = " ".join(formatted_parts[::-1])
        
        # Add the currency symbol at the end
        formatted_number += " Kč"
        
        return formatted_number



