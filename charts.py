import matplotlib.pyplot as plt
import pandas as pd
import json
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

vscode_blue = (0.175, 0.392, 0.785, 1.0)
custom_mid_gray_rgba = ((0.175 + 0.1625) / 2, (0.175 + 0.1625) / 2, (0.175 + 0.1625) / 2, 1.0)

class Chart():
    def __init__(self, tabview, file, expenditure):
        
        # Conrol the data that will be plotted
        if expenditure == "ALL":
            df = pd.DataFrame(file["items"])
            df_exp = df[df['income_expenditure'] == "0"]
            df_pre = self.pre_processing(df_exp)
        elif expenditure == None:
            with open('/Users/matous/Desktop/MoneySaver/files/blank.json', 'r') as f:
                file = json.load(f)
                df_pre = pd.DataFrame(file["items"])
        else:
            df = pd.DataFrame(file["items"])
            df_exp = df[df['income_expenditure'] == "0"]
            df_exp = self.take_specific_expenditure(df_exp, expenditure)
            df_pre = self.pre_processing(df_exp)

        # Create a Matplotlib figure and axis
        fig, ax = self.setup_plot()

        ax.stem(df_pre['date'], df_pre['price'], linefmt='--', markerfmt='D', basefmt='white', bottom=1.1, use_line_collection=True)

        self.configure_plot(ax, fig)

        # Embed the Matplotlib plot into the Tkinter GUI
        self.embed_plot(tabview, fig)

    # Create a Matplotlib figure and axis
    def setup_plot(self):
        fig, ax = plt.subplots(figsize=(2, 1))
        return fig, ax

    # Configure the Matplotlib plot
    def configure_plot(self, ax, fig):
        # Configure fonts
        title_font = {'family': 'Helvetica', 'size': 5, 'weight': 'bold'}
        label_font = {'family': 'Helvetica', 'size': 4}
        tick_font = {'family': 'Helvetica', 'size': 4}

        # Configure plot title, axes labels, and grid
        ax.set_title("Expenditure Over Time", fontdict=title_font, color='white')
        ax.set_xlabel("Days", fontdict=label_font, color='white', labelpad=10)
        ax.set_ylabel("Sum of money by day in [Kč]", fontdict=label_font, color='white', labelpad=10, va='center', rotation=-90)
        ax.grid(True, color='white', linestyle='--', linewidth=0.5)

        ax.yaxis.set_label_position("right")  # Move y-axis label to the right

        ax.tick_params(axis='both', labelsize=tick_font['size'], colors='white')

        # Rotate and adjust x-axis tick labels
        plt.xticks(rotation=45)
        plt.subplots_adjust(bottom=0.2)

        # Set background color
        ax.set_facecolor('lightgray')

        # Set plot area color
        fig.patch.set_facecolor(custom_mid_gray_rgba)

    # Embed the Matplotlib plot into the Tkinter GUI
    def embed_plot(self, tabview, fig):
        self.canvas = FigureCanvasTkAgg(fig, master=tabview.tab("TimePlot"))
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill='both', expand=True)

    # Pre-process the data to be plotted by the Matplotlib figure 
    def pre_processing(self, df):
        new_df = df.copy()
        new_df = new_df.assign(price=pd.to_numeric(new_df['price'], errors='coerce'))  # Transform price column to integers
        new_df['date'] = pd.to_datetime(new_df['date'], format='%d.%m.%Y')  # Convert the 'date' column to datetime format
        new_df = new_df.sort_values(by='date')  # Order by date
        new_df = new_df.groupby('date')['price'].sum().reset_index()  # Group by date and sum the 'price' column
        new_df['date'] = new_df['date'].dt.strftime('%d.%m')  # Extract month and day
        return new_df
    
    def take_specific_expenditure(self, df, expenditure_type):
        filtered_df = df[df['type'] == expenditure_type][['date', 'price']]
        return filtered_df


# Create the chart for histogram plot 
class HistogramBuilder:
    def __init__(self, tabview, file):
        df = pd.DataFrame(file["items"])
        df_exp = df[df['income_expenditure'] == "0"]
        df_pre = self.pre_processing(df_exp)

        fig, ax = self.setup_plot()

        vscode_blue = (0.175, 0.392, 0.785, 1.0)

        ax.bar(df_pre['type'], df_pre['price'], color='grey', edgecolor=vscode_blue)

        self.configure_plot(ax, fig)

        self.embed_plot(tabview, fig)

    # Create a Matplotlib figure and axis
    def setup_plot(self):
        fig, ax = plt.subplots(figsize=(2, 1))
        return fig, ax

    # Configure the Matplotlib plot
    def configure_plot(self, ax, fig):
        # Configure fonts and colors for the plot
        title_font = {'family': 'Helvetica', 'size': 5, 'weight': 'bold'}
        label_font = {'family': 'Helvetica', 'size': 4}
        tick_font = {'family': 'Helvetica', 'size': 4}

        # Configure plot title, axes labels, and grid
        ax.set_title("Total Expenditure by Category", fontdict=title_font, color='white')
        ax.set_ylabel("Money in [Kč]", fontdict=label_font, color='white')
        ax.grid(False)

        ax.tick_params(axis='both', labelsize=tick_font['size'], colors='white', rotation=45)

        # Set background color
        ax.set_facecolor('white')

        # Set plot area color
        fig.patch.set_facecolor(custom_mid_gray_rgba)

    # Embed the Matplotlib plot into the Tkinter GUI
    def embed_plot(self, tabview, fig):
        self.canvas = FigureCanvasTkAgg(fig, master=tabview.tab("HistogramPlot"))
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill='both', expand=True)
    #  Pre-process the data to be plotted by the Matplotlib figure
    def pre_processing(self, df):
        new_df = df.copy()
        new_df = new_df.assign(price=pd.to_numeric(new_df['price'], errors='coerce'))  # Transform price column to integers
        new_df = new_df.groupby('type')['price'].sum().reset_index()  # Group by expenditure type and sum the 'price' column
        return new_df
    
class MoneyBalancePlotter:
    def __init__(self, tabview, file):
        df = pd.DataFrame(file["items"])

        df_balance = self.calculate_monthly_money_balance(df)

        fig, ax = self.setup_plot()

        ax.plot(df_balance['date'], df_balance['balance'], marker='x', color='grey',mec=vscode_blue, mfc=vscode_blue)

        self.configure_plot(ax, fig)

        self.embed_plot(tabview, fig)


    #  Create a Matplotlib figure and axis
    def setup_plot(self):
        fig, ax = plt.subplots(figsize=(5, 2))
        return fig, ax

    #  Configure the Matplotlib plot
    def configure_plot(self, ax, fig):
        title_font = {'family': 'Helvetica', 'size': 5, 'weight': 'bold'}
        label_font = {'family': 'Helvetica', 'size': 4}
        tick_font = {'family': 'Helvetica', 'size': 4}

        ax.set_title("Money Balance Through Time", fontdict=title_font, color='white')
        ax.set_xlabel("Month", fontdict=label_font, color='white')
        ax.set_ylabel("Money Balance [Kč]", fontdict=label_font, color='white', labelpad=5)
        ax.grid(True)

        ax.tick_params(axis='x', labelsize=tick_font['size'], colors='white')
        ax.tick_params(axis='y', labelsize=tick_font['size'], colors='white', rotation=45)

        # Set background color
        ax.set_facecolor('white')

        # Set plot area color
        fig.patch.set_facecolor(custom_mid_gray_rgba)

    #  Embed the Matplotlib plot into the Tkinter GUI
    def embed_plot(self, tabview, fig):
        self.canvas = FigureCanvasTkAgg(fig, master=tabview.tab("MoneyBalance"))
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill='both', expand=True, ipadx=10, ipady=10)

    #  Pre-process the data to be plotted by the Matplotlib figure
    def calculate_monthly_money_balance(self, df):
        new_df = df.copy()
        new_df = new_df.assign(price=pd.to_numeric(new_df['price'], errors='coerce'))
        new_df['date'] = pd.to_datetime(new_df['date'], format='%d.%m.%Y')
        new_df['income'] = new_df[new_df['income_expenditure'] == "1"]['price']
        new_df['expenditure'] = new_df[new_df['income_expenditure'] == "0"]['price']
        new_df['date'] = new_df['date'].dt.strftime('%m')
        ex = new_df.groupby('date')['expenditure'].sum()
        in_ = new_df.groupby('date')['income'].sum()
        balance = in_ - ex
        return balance.reset_index().rename(columns={'index': 'date', 0: 'balance'})