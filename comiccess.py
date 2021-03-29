#***     IMPORT LIBRARIES     ***#
from tkinter import *
from tkinter import ttk
import random
import csv
import winsound
from functools import partial

#***     INITIALISE TKINTER WINDOW     ***#
root = Tk()
root.title("Comiccess")
root.iconbitmap('oci.ico')
root.resizable(False, False)

#***     DEFINE VARIABLES     ***#
search_entry = StringVar()
tab_startup_status = True
stock_items_class_list = []

#***     DEFINE CLASSES     ***#
class Comic:
    def __init__(self, series_name, vol_number, issue_name, in_stock, historical_sales, title_data, search_title):
        self.series_name = series_name
        self.vol_number = vol_number
        self.issue_name = issue_name
        self.full_title = str(series_name + ' Vol. ' + str(vol_number) + ': ' + issue_name)
        self.search_title = self.full_title.strip()
        self.in_stock = in_stock
        self.historical_sales = historical_sales
        self.title_data = title_data
        self.search_title = search_title

        self.index_frame = ttk.Frame(index_results_frame, relief=SUNKEN)
        self.index_title = ttk.Label(self.index_frame, text=self.full_title, anchor=CENTER, font='Bahnschrift 10 bold').grid(column=0, row=0, columnspan=2, sticky="ew")
        self.index_stock_label = ttk.Label(self.index_frame, text="In Stock", anchor=CENTER).grid(column=0, row=1, sticky="ew")
        self.index_hist_label = ttk.Label(self.index_frame, text="Historic Sales", anchor=CENTER).grid(column=1, row=1, sticky="ew")
        self.index_stock_item = ttk.Label(self.index_frame, text=self.in_stock, anchor=CENTER).grid(column=0, row=2, sticky="ew")
        self.index_hist_item = ttk.Label(self.index_frame, text=self.historical_sales, anchor=CENTER).grid(column=1, row=2, sticky="ew")
    
#***     LOAD DATA FROM FILES     ***#
def load_stock_data():
    with open('stock.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                title_data = str(row[0] + ' Vol. ' + str(row[1]) + ': ' + row[2] + "\n - " + row[3] + " in stock, and " + row[4] + " have been sold.")
                full_title_var = str(row[0] + str(row[1]) + row[2]).strip(",. ").lower().replace(",", "").replace(".", "").replace(" ","")
                globals()[full_title_var] = Comic(row[0], row[1], row[2], row[3], row[4], title_data, full_title_var)
                stock_items_class_list.append(list(globals().items())[-1])
                line_count += 1
        print(f'Processed {line_count-1} item/s.')
        topline = ttk.Label(index_results_frame, text="––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––").pack()
        for i in range(len(stock_items_class_list)):
            stock_items_class_list[i][1].index_frame.pack()
            ttk.Separator(index_results_frame, orient=HORIZONTAL).pack(fill="both", expand=True)

#***     DEFINE FUNCTIONS     ***#
def do_tab_switch_sales(event):
    global tab_startup_status
    if tab_startup_status == False:
        modify_manage_stock_tab.forget()
        modify_sales_tab.pack(side="left", fill="both", expand=True)
        print("tab_switched")
        tab_startup_status = True
    else:
        print('whoops')
    print(event)
    
def do_tab_switch_modify(event):
    global tab_startup_status
    if tab_startup_status == True:
        modify_sales_tab.forget()
        modify_manage_stock_tab.pack(side="left", fill="both", expand=True)
        print("tab_switched")
        tab_startup_status = False
    else:
        print('whoops')
    print(event)

#***     TKINTER WINDOW     ***#
s = ttk.Style()
s.configure('new.TFrame', background='#7AC5CD')

# Configure top level parent frames
index_parent = ttk.Frame(root)
index_parent.grid(column=0, row=0, sticky='n')
root.grid_columnconfigure(0, weight=1)

parent_separator = ttk.Separator(root, orient=VERTICAL)
parent_separator.grid(column=1, row=0, sticky='ns', padx=5, pady=5)

modify_parent = ttk.Frame(root)
modify_parent.grid(column=2, row=0, sticky=N)
root.grid_columnconfigure(2, weight=3)
root.grid_rowconfigure(0, weight=1)

#* Index Frames *#
index_label = ttk.Label(index_parent, text="INDEX", font=("Bahnschrift", 25))
index_label.grid(row=0, column=0, columnspan=2, sticky="n")

index_search_label = ttk.Label(index_parent, text="Index Search:  ")
index_search_label.grid(row=1, column=0, padx=2)
index_parent.grid_columnconfigure(0, weight=1)

index_search = ttk.Entry(index_parent, textvariable=search_entry)
index_search.grid(row=1, column=1, padx=2, pady=10, sticky="nsew")
index_parent.grid_columnconfigure(1, weight=80)

index_results_parent = ttk.Frame(index_parent)
index_results_parent.grid(row=2, column=0, columnspan=2, sticky="s", padx=10)
index_parent.grid_rowconfigure(2, weight=1)

#* Index Results Frames *#
index_results_canvas = Canvas(index_results_parent)
index_results_scrollbar = ttk.Scrollbar(index_results_parent, orient="vertical", command=index_results_canvas.yview)
index_results_frame = ttk.Frame(index_results_canvas)

index_results_frame.bind("<Configure>", lambda e: index_results_canvas.configure(scrollregion=index_results_canvas.bbox("all")))

index_results_canvas.create_window((0, 0), window=index_results_frame, anchor="nw")
index_results_canvas.configure(yscrollcommand=index_results_scrollbar.set)

index_results_canvas.pack(side="left", fill="both", expand=True)
index_results_scrollbar.pack(side="right", fill="y")



#* Modify Frames *#
#* Modify Tab Button Frames *#
modify_sales_button = ttk.Frame(modify_parent)
modify_sales_button.grid(row=0, column=0, padx=10, sticky=N)
modify_sales_text = ttk.Label(modify_sales_button, text="SALES", font=("Bahnschrift", 25), anchor="n")
modify_sales_text.pack()
modify_sales_button.bind("<Button-1>", do_tab_switch_sales)
modify_sales_text.bind("<Button-1>", do_tab_switch_sales)

modify_row_divide = ttk.Separator(modify_parent, orient=VERTICAL)
modify_row_divide.grid(row=0, column=1, sticky='ns', pady=5)

modify_manage_stock_button = ttk.Frame(modify_parent)
modify_manage_stock_button.grid(row=0, column=2, padx=10, sticky="s")
modify_manage_stock_text = ttk.Label(modify_manage_stock_button, text="MANAGE STOCK", font=("Bahnschrift", 25), anchor=N)
modify_manage_stock_text.pack()
modify_manage_stock_button.bind('<Button-1>', do_tab_switch_modify)
modify_manage_stock_text.bind('<Button-1>', do_tab_switch_modify)

modify_frames_parent = ttk.Frame(modify_parent)
modify_frames_parent.grid(row=1, column=0, columnspan=3)

modify_parent.grid_rowconfigure(1, weight=10)
modify_parent.columnconfigure(0, weight=1)
modify_parent.columnconfigure(2, weight=1)

#* Modify Tab Frames *#
modify_sales_tab = ttk.Frame(modify_frames_parent)
modify_sales_tab.pack(side="left", fill="both", expand=True)

modify_manage_stock_tab = ttk.Frame(modify_frames_parent)
modify_manage_stock_tab.pack(side="left", fill="both", expand=True)
modify_manage_stock_tab.forget()

#***     RUN UPDATES & TKINTER WINDOW     ***#
load_stock_data()
root.mainloop()
