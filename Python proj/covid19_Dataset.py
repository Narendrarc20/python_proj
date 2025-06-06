import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates
from matplotlib.widgets import Cursor
import tkinter as tk
from tkinter import ttk

# Load the dataset
file_path = "WHO-COVID-19-global-data.csv"
df = pd.read_csv(file_path)

# Convert Date to datetime format
df['Date_reported'] = pd.to_datetime(df['Date_reported'])

# Fill missing values
df.fillna(0, inplace=True)

def show_full_dataset():
    """Displays the full dataset in a pop-up window in table format."""
    root = tk.Tk()
    root.title("Full Dataset Viewer")
    
    frame = tk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True)
    
    tree = ttk.Treeview(frame)
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    scrollbar.pack(side=tk.RIGHT, fill="y")
    tree.configure(yscrollcommand=scrollbar.set)
    
    tree['columns'] = list(df.columns)
    tree.column("#0", width=0, stretch=tk.NO)
    for col in df.columns:
        tree.column(col, anchor=tk.W, width=150)
        tree.heading(col, text=col, anchor=tk.W)
    
    for index, row in df.iterrows():
        tree.insert("", tk.END, values=list(row))
    
    root.mainloop()

def add_hover_tooltip(fig, ax, x_data=None, y_data=None):
    """Adds hover tooltip functionality to the plot"""
    annot = ax.annotate("", xy=(0,0), xytext=(20,20), textcoords="offset points",
                        bbox=dict(boxstyle="round", fc="w", alpha=0.8),
                        arrowprops=dict(arrowstyle="->"))
    annot.set_visible(False)

    def update_annot(event):
        if event.inaxes == ax:
            x, y = event.xdata, event.ydata
            annot.xy = (x, y)
            annot.set_text(f"({int(x)}, {int(y)})")
            annot.set_visible(True)
            fig.canvas.draw_idle()
        else:
            annot.set_visible(False)

    fig.canvas.mpl_connect("motion_notify_event", update_annot)

# Visualization Menu
while True:
    print("\nSelect a visualization:")
    print("1. Global COVID-19 Cases Trend")
    print("2. Top 10 Countries by COVID-19 Cases & Deaths")
    print("3. Daily New COVID-19 Cases Trend")
    print("4. Heatmap of COVID-19 Cases Across Countries")
    print("5. Pie Chart for Top 5 Countries with Highest COVID-19 Cases")
    print("6. Exit")
    print("7. View Full Dataset")
    
    choice = input("Enter your choice (1-7): ")
    
    if choice == "1":
        # Global COVID-19 Cases Trend
        # Convert numeric columns to the correct data type
        numeric_cols = ['New_cases', 'Cumulative_cases', 'New_deaths', 'Cumulative_deaths']
        df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')

        # Now perform groupby
        global_trend = df.groupby("Date_reported")[numeric_cols].sum()

        
        fig, ax = plt.subplots(figsize=(10,5))
        ax.plot(global_trend.index, global_trend["Cumulative_cases"], label="Cumulative Cases", color="blue")
        ax.plot(global_trend.index, global_trend["Cumulative_deaths"], label="Cumulative Deaths", color="red")
        
        ax.set_title("Global COVID-19 Cases Trend")
        ax.set_xlabel("Date")
        ax.set_ylabel("Count")
        ax.legend()
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
        plt.xticks(rotation=45)

        add_hover_tooltip(fig, ax)
        plt.show()

    elif choice == "2":
        # Top 10 Countries by COVID-19 Cases & Deaths
        # Ensure numeric columns are correctly formatted
        numeric_cols = ['New_cases', 'Cumulative_cases', 'New_deaths', 'Cumulative_deaths']
        df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')

        # Group by 'Country' and sum only numeric columns
        top_countries = df.groupby("Country")[numeric_cols].sum()

        # Get the top 10 countries by cumulative cases
        top_countries = top_countries.nlargest(10, "Cumulative_cases")

        # Print or visualize results
        print(top_countries)

        
        fig, ax = plt.subplots(figsize=(12,6))
        sns.barplot(x=top_countries.index, y=top_countries["Cumulative_cases"], color="blue", label="Cumulative Cases", ax=ax)
        sns.barplot(x=top_countries.index, y=top_countries["Cumulative_deaths"], color="red", label="Cumulative Deaths", ax=ax)

        ax.set_title("Top 10 Countries by COVID-19 Cases & Deaths")
        ax.set_xlabel("Country")
        ax.set_ylabel("Count")
        plt.xticks(rotation=60, ha='right', fontsize=10)
        ax.legend()

        add_hover_tooltip(fig, ax)
        plt.show()

    elif choice == "3":
        # Daily New COVID-19 Cases Trend
        # Convert relevant columns to numeric to avoid string concatenation issues
        numeric_cols = ['New_cases', 'Cumulative_cases', 'New_deaths', 'Cumulative_deaths']
        df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')

        # Group by date and sum numeric columns
        global_daily = df.groupby("Date_reported")[numeric_cols].sum()

        # Print or visualize results
        print(global_daily)

        
        fig, ax = plt.subplots(figsize=(10,5))
        ax.plot(global_daily.index, global_daily["New_cases"], label="New Cases", color="blue")
        
        ax.set_title("Daily New COVID-19 Cases Trend")
        ax.set_xlabel("Date")
        ax.set_ylabel("New Cases")
        ax.legend()
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
        plt.xticks(rotation=45)

        add_hover_tooltip(fig, ax)
        plt.show()

    elif choice == "4":
        # Heatmap of COVID-19 Cases Across Countries
        # Ensure only numeric columns are used for summation
        # Exclude non-numeric columns before summing
        numeric_cols = ['Cumulative_cases', 'New_cases', 'Cumulative_deaths', 'New_deaths']
        df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')

        # Perform groupby and sum only for numeric columns
        country_wise = df.groupby("Country")[numeric_cols].sum()

        # Sort by cumulative cases and get top 20
        country_wise = country_wise.sort_values("Cumulative_cases", ascending=False).head(20)

        # Display or use the data for visualization
        print(country_wise)


        country_wise = country_wise.reset_index()
        
        fig, ax = plt.subplots(figsize=(12,6))
        heatmap_data = country_wise.pivot_table(index="Country", values="Cumulative_cases")
        sns.heatmap(heatmap_data, cmap="Blues", annot=True, linewidths=0.5, ax=ax)

        ax.set_title("Heatmap of COVID-19 Cases Across Countries")
        ax.set_xlabel("Cumulative Cases")
        ax.set_ylabel("Country")

        plt.show()

    elif choice == "5":
        # Pie Chart for Top 5 Countries with Highest COVID-19 Cases
        # Convert only numeric columns to avoid datetime errors
        numeric_cols = ['Cumulative_cases', 'New_cases', 'Cumulative_deaths', 'New_deaths']
        df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')

        # Group by country and sum only numeric values
        top_5_countries = df.groupby("Country")[numeric_cols].sum()

        # Get top 5 countries with the highest cumulative cases
        top_5_countries = top_5_countries.nlargest(5, "Cumulative_cases")

        # Display results
        print(top_5_countries)

        
        fig, ax = plt.subplots(figsize=(8,8))
        wedges, texts, autotexts = ax.pie(top_5_countries["Cumulative_cases"], labels=top_5_countries.index, autopct='%1.1f%%', colors=sns.color_palette("pastel"), startangle=140)
        
        ax.set_title("Top 5 Countries with Highest COVID-19 Cases")
        plt.show()

    elif choice == "7":
        show_full_dataset()

    elif choice == "6":
        print("Exiting visualization tool.")
        break

    else:
        print("Invalid choice. Please select again.")
