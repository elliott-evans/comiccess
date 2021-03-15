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

#***     LOAD DATA FROM FILES     ***#


#***     DEFINE VARIABLES     ***#
search_entry = StringVar()
tab_startup_status = True

#***     DEFINE CLASSES     ***#


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
index_results_parent.grid(row=2, column=0, columnspan=2, sticky="s")
index_parent.grid_rowconfigure(2, weight=1)

#* Index Results Frames *#
index_results_canvas = Canvas(index_results_parent)
index_results_scrollbar = ttk.Scrollbar(index_results_parent, orient="vertical", command=index_results_canvas.yview)
index_results_frame = ttk.Frame(index_results_canvas)

index_results_frame.bind(
    "<Configure>",
    lambda e: index_results_canvas.configure(
        scrollregion=index_results_canvas.bbox("all")
    )
)

index_results_canvas.create_window((0, 0), window=index_results_frame, anchor="nw")
index_results_canvas.configure(yscrollcommand=index_results_scrollbar.set)

index_results_canvas.pack(side="left", fill="both", expand=True)
index_results_scrollbar.pack(side="right", fill="y")

for i in range(50):
    ttk.Label(index_results_frame, text="Sample scrolling label").pack()

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
root.mainloop()
