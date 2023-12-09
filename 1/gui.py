import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from tkcalendar import DateEntry
import datetime
import os
import json
import subprocess



class FileSelectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Scraping Data")
        self.root.geometry("500x600")

        self.style = ttk.Style()
        self.style.configure('TButton', font=('Arial', 10), background='#4CAF50')

        self.file_path = tk.StringVar()

        # Set default values for initial and secondary dates and times
        self.set_default_values()

        self.create_widgets()

    def set_default_values(self):
        
        # Set default values for initial date and time
        #initial_date_default = datetime.datetime.today() - datetime.timedelta(days=3)
        #initial_date_default = datetime.datetime(2023, 10, 1)
        #self.initial_date1 = tk.StringVar(value=initial_date_default.strftime('%Y-%m-%d'))
        
        self.initial_date = tk.StringVar(value=(datetime.datetime.now()- datetime.timedelta(days=3)).strftime('%Y-%m-%d'))
        self.initial_hour = tk.StringVar(value="00")
        self.initial_minute = tk.StringVar(value="01")

        # Set default values for secondary date and time
        self.secondary_date = tk.StringVar(value=datetime.datetime.now().strftime('%Y-%m-%d'))
        self.secondary_hour = tk.StringVar(value=datetime.datetime.now().strftime('%H'))
        self.secondary_minute = tk.StringVar(value=datetime.datetime.now().strftime('%M'))

    def create_widgets(self):
        # File path entry
        label_file = ttk.Label(self.root, text="Select a file:")
        label_file.grid(row=0, column=0, padx=10, pady=10)
        entry_file = ttk.Entry(self.root, textvariable=self.file_path, width=30)
        entry_file.grid(row=0, column=1, padx=10, pady=10)
        browse_button = ttk.Button(self.root, text="Browse", command=self.browse_file)
        browse_button.grid(row=0, column=2, padx=10, pady=10)

        # Initial date entry
        label_initial_date = ttk.Label(self.root, text="Initial Date:")
        label_initial_date.grid(row=1, column=0, padx=10, pady=10)
        initial_date_entry = DateEntry(self.root, textvariable=self.initial_date, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        initial_date_entry.grid(row=1, column=1, padx=10, pady=10)

        # Initial time entry
        label_initial_time = ttk.Label(self.root, text="Initial Time:")
        label_initial_time.grid(row=2, column=0, padx=10, pady=10)
        initial_hour_spinbox = ttk.Spinbox(self.root, textvariable=self.initial_hour, from_=0, to=23, width=5, format="%02.0f")
        initial_hour_spinbox.grid(row=2, column=1, padx=10, pady=10)
        ttk.Label(self.root, text=" : ").grid(row=2, column=2)
        initial_minute_spinbox = ttk.Spinbox(self.root, textvariable=self.initial_minute, from_=0, to=59, width=5, format="%02.0f")
        initial_minute_spinbox.grid(row=2, column=3, padx=10, pady=10)

        # Secondary date entry
        label_secondary_date = ttk.Label(self.root, text="Secondary Date:")
        label_secondary_date.grid(row=3, column=0, padx=10, pady=10)
        secondary_date_entry = DateEntry(self.root, textvariable=self.secondary_date, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        secondary_date_entry.grid(row=3, column=1, padx=10, pady=10)

        # Secondary time entry
        label_secondary_time = ttk.Label(self.root, text="Secondary Time:")
        label_secondary_time.grid(row=4, column=0, padx=10, pady=10)
        secondary_hour_spinbox = ttk.Spinbox(self.root, textvariable=self.secondary_hour, from_=0, to=23, width=5, format="%02.0f")
        secondary_hour_spinbox.grid(row=4, column=1, padx=10, pady=10)
        ttk.Label(self.root, text=" : ").grid(row=4, column=2)
        secondary_minute_spinbox = ttk.Spinbox(self.root, textvariable=self.secondary_minute, from_=0, to=59, width=5, format="%02.0f")
        secondary_minute_spinbox.grid(row=4, column=3, padx=10, pady=10)

        # OK Button
        ok_button = ttk.Button(self.root, text="OK", command=self.ok_button_click)
        ok_button.grid(row=5, column=1, padx=10, pady=10)

        self.root.configure(bg='#f0f0f0')

    def browse_file(self):
        file_types = [("Excel files", "*.xlsx;*.xls;*.csv"), ("All files", "*.*")]
        file_path = filedialog.askopenfilename(title="Select a file", filetypes=file_types)

        if file_path:
            _, file_extension = os.path.splitext(file_path)
            valid_extensions = ['.xlsx', '.xls', '.csv']
            if file_extension.lower() in valid_extensions:
                self.file_path.set(file_path)
            else:
                messagebox.showwarning("Invalid File", "Please select a valid Excel or CSV file.")
        else:
            messagebox.showinfo("Info", "No file selected.")

    def ok_button_click(self):
        file_path = self.file_path.get()
        initial_date = self.initial_date.get()
        initial_hour = self.initial_hour.get()
        initial_minute = self.initial_minute.get()
        secondary_date = self.secondary_date.get()
        secondary_hour = self.secondary_hour.get()
        secondary_minute = self.secondary_minute.get()
        data={
        "file_path": file_path,    
        "initial_date"   :  initial_date,
        "initial_hour"   : initial_hour,
        "initial_minute" : initial_minute,
        "secondary_date" : secondary_date,
        "secondary_hour" : secondary_hour,
        "secondary_minute":secondary_minute}
        
        #first_date = datetime.datetime.combine(datetime.datetime.strptime(initial_date, "%Y-%m-%d"), datetime.time(int(initial_hour),int(initial_minute)))
        #end_date = datetime.datetime.combine(datetime.datetime.strptime(secondary_date, "%Y-%m-%d"), datetime.time(int(secondary_hour),int(secondary_minute)))
        #print("Input Values", f"File Path: {file_path}\nInitial Date: {first_date}\nSecondary Date: {end_date}")
        #print(initial_date,initial_hour,initial_minute,secondary_date,secondary_hour,secondary_minute)
    
        serial=json.dumps(data)
        subprocess.run(["python","az_madar.py",serial])
if __name__ == "__main__":
    root = tk.Tk()
    app = FileSelectorApp(root)
    root.mainloop()
