#***     IMPORT LIBRARIES     ***#
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import random
import csv
from functools import partial

#***     INITIALISE TKINTER WINDOW     ***#
root = Tk()
root.title("Comiccess")
root.iconbitmap('oci.ico')
root.resizable(False, False)

#***     DEFINE VARIABLES     ***#
search_entry = StringVar()
selectitem_existing_number_var = StringVar()
selectitem_create_volume_num_var = StringVar()
selectitem_create_volume_name_var = StringVar()
selectitem_create_init_stock_var = StringVar()
tab_startup_status = True
stock_items_class_list = []
series_list = {}
series_select_list = [""]
vol_select_list = []
do_restore = False
restore_var = ""

selectitem_series_existing_var = StringVar()
#***     DEFINE CLASSES     ***#
class Comic:
    def __init__(self, series_name, vol_number, issue_name, in_stock, historical_sales, title_data, search_title):
        self.series_name = series_name
        self.vol_number = vol_number
        self.issue_name = issue_name
        self.vol_issue = 'Vol. ' + self.vol_number + ': ' + self.issue_name
        self.full_title = str(series_name + ' Vol. ' + str(vol_number) + ': ' + issue_name)
        self.in_stock = int(in_stock)
        self.historical_sales = historical_sales
        self.title_data = title_data
        self.search_title = search_title
        if self.series_name not in series_list:
            series_list[self.series_name] = {self.vol_issue: self}
        elif self.series_name in series_list and self.vol_issue not in series_list[self.series_name]:
            series_list[self.series_name][self.vol_issue] = self
        else:
            result = messagebox.askquestion('Comic Duplicate Error','Instance of the {} comic already detected! Would you like to delete the duplicate item?'.format(self.full_title))
            if result=='yes':
                del self
            else:
                pass

    def create_item_widget(self, location):
        self.item_frame = ttk.Frame(location, relief=SUNKEN)
        self.mod_title = ttk.Label(self.item_frame, text=self.full_title, anchor=CENTER, font='Bahnschrift 10 bold').grid(column=0, row=0, columnspan=2, sticky="ew")
        self.mod_stock_label = ttk.Label(self.item_frame, text="In Stock", anchor=CENTER).grid(column=0, row=1, sticky="ew")
        self.mod_hist_label = ttk.Label(self.item_frame, text="Historic Sales", anchor=CENTER).grid(column=1, row=1, sticky="ew")
        self.mod_stock_item = ttk.Label(self.item_frame, text=self.in_stock, anchor=CENTER).grid(column=0, row=2, sticky="ew")
        self.mod_hist_item = ttk.Label(self.item_frame, text=self.historical_sales, anchor=CENTER).grid(column=1, row=2, sticky="ew")
        self.item_frame.pack()
        
        
    def clear_all():
        self.item_frame.forget_pack()
        del self
    
#***     LOAD DATA FROM FILES     ***#
def load_stock_data():
    global stock_items_class_list, series_list, series_select_list, vol_select_list, do_restore
    for item in stock_items_class_list:
        print("Wiped {}".format(item.full_title))
        item.clear_all()
    stock_items_class_list = []
    series_list = {}
    series_select_list = [""]
    vol_select_list = [""]
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
            stock_items_class_list[i][1].create_item_widget(index_results_frame)
            ttk.Separator(index_results_frame, orient=HORIZONTAL).pack(fill="both", expand=True)
        update_lists()
    if do_restore == True:
        if restore_var[0] == "modify":
            pass
        elif restore_var[0] == "sell":
            pass
        do_restore = False

#***     DEFINE FUNCTIONS     ***#
def update_lists():
    global series_list, series_select_list
    for item in series_list.keys():
        series_select_list.append(item)
    selectitem_existing_series.config(values=series_select_list)
    selectitem_create_series.config(values=series_select_list)
    sell_series_select_combobox.config(values=series_select_list)
    print("e{}".format(series_select_list))

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
    print(series_select_list)
    
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
    print(series_select_list)

#* Comics Selection Functions *#
def existing_series_selected(event):
    global vol_select_list
    if selectitem_existing_series.get() == "":
        vol_select_list = [""]
        selectitem_existing_vol.config(values=vol_select_list)
        selectitem_existing_vol.set("")
        selectitem_existing_number.delete(0, END)
        selectitem_existing_operator.set("")
        selectitem_existing_vol.config(state='disabled')
        selectitem_existing_operator.config(state='disabled')
        selectitem_existing_number.config(state='disabled')
        selectitem_apply_changes_button.config(state='disabled')
        selectitem_create_series.config(state='normal')
    else:
        vol_select_list = [""]
        selectitem_existing_vol.config(state='readonly')
        for key, val_list in series_list.items():
            if selectitem_existing_series.get() == key:
                for item in val_list.keys():
                    vol_select_list.append(item)
        selectitem_existing_vol.config(values=vol_select_list)
        selectitem_create_series.set("")
        selectitem_create_series.config(state='disabled')
        
    print(event)

def existing_vol_selected(event):
    if selectitem_existing_vol.get() == "":
        selectitem_existing_operator.config(state='disabled')
        selectitem_existing_operator.set("")
        selectitem_existing_number.delete(0, END)
        selectitem_existing_number.config(state='disabled')
        selectitem_apply_changes_button.config(state='disabled')
    else:
        selectitem_existing_operator.config(state='readonly')

def existing_operator_selected(event):
    if selectitem_existing_operator.get() == "":
        selectitem_existing_number.delete(0, END)
        selectitem_existing_number.config(state='disabled')
        selectitem_apply_changes_button.config(state='disabled')
    else:
        selectitem_existing_number.config(state='normal')
    
def existing_number_validate(char):
    if char.isdigit():
        return True
    else:
        return False

def selectitem_existing_num_command(event):
    if selectitem_existing_number.get() == "":
        selectitem_apply_changes_button.config(state='disabled')
    else:
        selectitem_apply_changes_button.config(state='normal')
        

def created_series_selected(event):
    if selectitem_create_series.get() == "":
        selectitem_create_series.config(state='normal')
        selectitem_create_vol_entry.delete(0, END)
        selectitem_create_vol_entry.config(state='disabled')
        selectitem_create_vol_name.delete(0, END)
        selectitem_create_vol_name.config(state='disabled')
        selectitem_create_init_stock.delete(0, END)
        selectitem_create_init_stock.config(state='disabled')
        selectitem_apply_changes_button.config(state='disabled')
        selectitem_existing_series.config(state='readonly')
        
    elif selectitem_create_series.get() in series_select_list:
        selectitem_create_series.config(state='readonly')
        selectitem_create_vol_entry.config(state='normal')
        selectitem_existing_series.set("")
        selectitem_existing_series.config(state='disabled')
    else:
        selectitem_create_series.config(state='normal')
        selectitem_create_vol_entry.config(state='normal')
        selectitem_existing_series.set("")
        selectitem_existing_series.config(state='disabled')

def created_vol_num_selected(event):
    if selectitem_create_vol_entry.get() == "":
        selectitem_create_vol_name.delete(0, END)
        selectitem_create_vol_name.config(state='disabled')
        selectitem_create_init_stock.delete(0, END)
        selectitem_create_init_stock.config(state='disabled')
        selectitem_apply_changes_button.config(state='disabled')
    else:
        selectitem_create_vol_name.config(state='normal')
        
def created_vol_name_selected(event):
    if selectitem_create_vol_name.get() == "":
        selectitem_create_init_stock.delete(0, END)
        selectitem_create_init_stock.config(state='disabled')
        selectitem_apply_changes_button.config(state='disabled')
    else:
        selectitem_create_init_stock.config(state='normal')
    
def created_comic_init_stock_selected(event):
    if selectitem_create_init_stock.get() == "":
        selectitem_apply_changes_button.config(state='disabled')
    else:
        selectitem_apply_changes_button.config(state='normal')

def selectitem_apply_changes():
    if selectitem_existing_series.get() != "":
        print(series_list[selectitem_existing_series.get()][selectitem_existing_vol.get()].in_stock)
        comic_class_instance = series_list[selectitem_existing_series.get()][selectitem_existing_vol.get()]
        stock_action = selectitem_existing_operator.get()
        stock_number = int(selectitem_existing_number.get())
        do_clear = False
        if stock_action == "SET":
            comic_class_instance.in_stock = stock_number
            do_clear = True
        elif stock_action == "+":
            comic_class_instance.in_stock += stock_number
            do_clear = True
        elif stock_action == "-":
            if stock_number <= comic_class_instance.in_stock:
                comic_class_instance.in_stock -= stock_number
                do_clear = True
            else:
                messagebox.showerror('Stock Error!', 'You tried to remove more comics than were in stock. Try again.')
                do_clear = False
                selectitem_existing_number.delete(0, END)
                selectitem_existing_num_command("")
        print(series_list[selectitem_existing_series.get()][selectitem_existing_vol.get()].in_stock)
        if do_clear == True:
            restore_var = ("modify",comic_class_instance.full_title)
            selectitem_existing_series.set("")
            existing_series_selected("")
            update_save_data()
    elif selectitem_create_series.get() != "":
        series_name = selectitem_create_series.get()
        vol_number = selectitem_create_vol_entry.get()
        issue_name = selectitem_create_vol_name.get()
        in_stock = selectitem_create_init_stock.get()
        title_data = str(series_name + ' Vol. ' + vol_number + ': ' + issue_name + "\n - " + in_stock + " in stock, and " + "0" + " have been sold.")
        full_title_var = str(series_name + vol_number + issue_name).strip(",. ").lower().replace(",", "").replace(".", "").replace(" ","")
        globals()[full_title_var] = Comic(series_name, vol_number, issue_name, in_stock, 0, title_data, full_title_var)
        update_save_data()
        selectitem_create_series.set("")
        created_series_selected("") 
    else: 
        pass

def sell_series_selected(event):
    sell_comic_select_combobox.config(values=series_select_list)
    selection = sell_series_select_combobox.get()
    if selection == "":
        sell_comic_select_combobox.config(values="", state='disabled')
        sell_comic_select_combobox.set("")
        sell_stock_data_parent.config(text="Comic")
        sell_comic_selected("")
    else:
        values_list = [""]
        comic_itemslist = series_list[sell_series_select_combobox.get()]
        for k, v in comic_itemslist.items():
            values_list.append(v.vol_issue)
        sell_comic_select_combobox.config(values=values_list, state='readonly')
        sell_comic_select_combobox.set("")
        sell_comic_selected("")

def sell_comic_selected(event):
    if sell_comic_select_combobox.get() == "":
        sell_stock_data_parent.config(text="Comic: ")
        sell_stock_details_value.config(text=" - ")
        sell_stock_historical_value.config(text=" - ")
        sell_stock_button.config(state='disabled', text='Sell :::  \n')
    else:
        print(series_list[sell_series_select_combobox.get()][sell_comic_select_combobox.get()])
        selected_item = series_list[sell_series_select_combobox.get()][sell_comic_select_combobox.get()]
        sell_stock_data_parent.config(text=" {} ".format(selected_item.full_title))
        sell_stock_details_value.config(text=" {} ".format(selected_item.in_stock))
        sell_stock_historical_value.config(text=" {} ".format(selected_item.historical_sales))
        sell_stock_button.config(state='normal', text='Sell ::: \n{}'.format(selected_item.full_title))

def sell_stock_button():
    pass
    selected_item = series_list[sell_series_select_combobox.get()][sell_comic_select_combobox.get()]
    print("Item in stock: {}".format(selected_item.in_stock))
    clearitem = False
    if selected_item.in_stock > 1:
        selected_item.in_stock -= 1
        clearitem = True
    else:
        messagebox.showerror('Out of stock!', 'It looks like that item is out of stock, sorry!')
    print("Item in stock: {}".format(selected_item.in_stock))
    if clearitem == True:
        restore_var = ("sell",selected_item.full_title)
        update_save_data()
    
def update_save_data():
    do_restore = True
    print("Data (not) saved!")
    #load_stock_data()

#***     TKINTER WINDOW     ***#
s = ttk.Style()
s.configure('new.TFrame', background='#7AC5CD')

# Configure top level parent frames
index_parent = ttk.Frame(root)
index_parent.grid(column=0, row=0, sticky='n')
root.grid_columnconfigure(0, weight=1)

parent_separator = ttk.Separator(root, orient=VERTICAL)
parent_separator.grid(column=1, row=0, sticky='ns', padx=5, pady=5)
root.grid_columnconfigure(1, weight=0)

modify_parent = ttk.Frame(root)
modify_parent.grid(column=2, row=0, sticky=N)
root.grid_columnconfigure(2, weight=7)
root.grid_rowconfigure(0, weight=1)

#* Index Frames *#
index_label = ttk.Label(index_parent, text="INDEX", font=("Bahnschrift", 25))
index_label.grid(row=0, column=0, columnspan=2, sticky="n")

#index_search_label = ttk.Label(index_parent, text="Index Search:  ")
#index_search_label.grid(row=1, column=0, padx=2)
#index_parent.grid_columnconfigure(0, weight=1)

#index_search = ttk.Entry(index_parent, textvariable=search_entry)
#index_search.grid(row=1, column=1, padx=2, pady=10, sticky="nsew")
#index_parent.grid_columnconfigure(1, weight=80)

index_results_parent = ttk.Frame(index_parent)
index_results_parent.grid(row=1, column=0, columnspan=2, sticky="s", padx=10)
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
#* Manage Stock Parent Frames *#
manage_stock_selectitem_parent = ttk.LabelFrame(modify_manage_stock_tab, text="Select Comic")
manage_stock_selectitem_parent.grid(row=0, column=0)

# Manage Stock SelectItem Parent Frames #
selectitem_existing_parent = ttk.LabelFrame(manage_stock_selectitem_parent, text="Existing Comic")
selectitem_existing_parent.grid(row=0, column=0)

selectitem_or_divider = ttk.Label(manage_stock_selectitem_parent, text=" or ")
selectitem_or_divider.grid(row=0, column=1)

selectitem_new_parent = ttk.LabelFrame(manage_stock_selectitem_parent, text="Create Comic")
selectitem_new_parent.grid(row=0, column=2)

# SelectItem Existing #
selectitem_existing_series_label = ttk.Label(selectitem_existing_parent, text="Series:  ")
selectitem_existing_series_label.grid(row=0, column=0)

selectitem_existing_series = ttk.Combobox(selectitem_existing_parent, state='readonly', values=series_select_list)
selectitem_existing_series.grid(row=0, column=1, pady=5)
selectitem_existing_series.bind("<<ComboboxSelected>>",existing_series_selected)

selectitem_existing_vol_label = ttk.Label(selectitem_existing_parent, text="Volume:  ")
selectitem_existing_vol_label.grid(row=1, column=0)

selectitem_existing_vol = ttk.Combobox(selectitem_existing_parent, state='disabled')
selectitem_existing_vol.grid(row=1, column=1, pady=5)
selectitem_existing_vol.bind("<<ComboboxSelected>>",existing_vol_selected)

selectitem_existing_operator = ttk.Combobox(selectitem_existing_parent, state='disabled', values=("SET","+","-"), width=4)
selectitem_existing_operator.grid(row=2, column=0, pady=5)
selectitem_existing_operator.bind("<<ComboboxSelected>>",existing_operator_selected)

selectitem_existing_number_validation = selectitem_existing_parent.register(existing_number_validate)
selectitem_existing_number = ttk.Entry(selectitem_existing_parent, textvariable=selectitem_existing_number_var, state='disabled', width=23, validate='all', validatecommand=(selectitem_existing_number_validation, '%S'))
selectitem_existing_number.grid(row=2, column=1, pady=5)
selectitem_existing_number.bind("<KeyRelease>",selectitem_existing_num_command)
                
# SelectItem CreateNew #
selectitem_create_series_label = ttk.Label(selectitem_new_parent, text="Series:  ")
selectitem_create_series_label.grid(row=0, column=0)

selectitem_create_series = ttk.Combobox(selectitem_new_parent, values=series_select_list)
selectitem_create_series.grid(row=0, column=1, pady=5)
selectitem_create_series.bind("<<ComboboxSelected>>",created_series_selected)
selectitem_create_series.bind("<KeyRelease>",created_series_selected)

selectitem_create_vol_frame = ttk.Frame(selectitem_new_parent)
selectitem_create_vol_frame.grid(row=1, column=0, columnspan=2)

selectitem_create_vol_label = ttk.Label(selectitem_create_vol_frame, text="  Vol.")
selectitem_create_vol_label.grid(row=0, column=0)

selectitem_create_vol_entry_validation = selectitem_create_vol_frame.register(existing_number_validate)
selectitem_create_vol_entry = ttk.Entry(selectitem_create_vol_frame, textvariable=selectitem_create_volume_num_var, state='disabled', width=3, validate='all', validatecommand=(selectitem_create_vol_entry_validation, '%S'))
selectitem_create_vol_entry.grid(row=0, column=1)
selectitem_create_vol_entry.bind("<KeyRelease>",created_vol_num_selected)

selectitem_create_vol_name_label = ttk.Label(selectitem_create_vol_frame, text=" : ")
selectitem_create_vol_name_label.grid(row=0, column=2)

selectitem_create_vol_name = ttk.Entry(selectitem_create_vol_frame, textvariable=selectitem_create_volume_name_var, state='disabled', width=23)
selectitem_create_vol_name.grid(row=0, column=3)
selectitem_create_vol_name.bind("<KeyRelease>",created_vol_name_selected)

selectitem_create_init_stock_label = ttk.Label(selectitem_new_parent, text="Initial Stock:")
selectitem_create_init_stock_label.grid(row=2, column=0)

selectitem_create_init_stock_validation = selectitem_new_parent.register(existing_number_validate)
selectitem_create_init_stock = ttk.Entry(selectitem_new_parent, width=23, textvariable=selectitem_create_init_stock_var, state='disabled', validate='all', validatecommand=(selectitem_create_init_stock_validation, '%S'))
selectitem_create_init_stock.grid(row=2, column=1, pady=5)
selectitem_create_init_stock.bind("<KeyRelease>",created_comic_init_stock_selected)

# SelectItem Apply Changes #
selectitem_apply_changes_button = ttk.Button(manage_stock_selectitem_parent, text="Apply Changes", command=selectitem_apply_changes, state='disabled', width=70)
selectitem_apply_changes_button.grid(row=2, column=0, columnspan=3, pady=5)

#* Sell Stock Parent Frames *#
sell_stock_selectitem_parent = ttk.LabelFrame(modify_sales_tab, text="Select Comic To Sell")
sell_stock_selectitem_parent.grid(row=0, column=0)

sell_stock_data_parent = ttk.LabelFrame(modify_sales_tab, text="Comic: ", width=50)
sell_stock_data_parent.grid(row=1, column=0, pady=7)

# Sell Stock SelectItem #
sell_series_select_label = ttk.Label(sell_stock_selectitem_parent, text="Select Series: |")
sell_series_select_label.grid(row=0, column=0)

sell_series_select_combobox = ttk.Combobox(sell_stock_selectitem_parent, values=series_select_list, state='readonly', width=54)
sell_series_select_combobox.grid(row=0, column=1, columnspan=3, pady=5, padx=5)
sell_series_select_combobox.bind("<<ComboboxSelected>>",sell_series_selected)

sell_comic_select_label = ttk.Label(sell_stock_selectitem_parent, text="Select Comic: |")
sell_comic_select_label.grid(row=1, column=0)

sell_comic_select_combobox = ttk.Combobox(sell_stock_selectitem_parent, values="", state='disabled', width=54)
sell_comic_select_combobox.grid(row=1, column=1, columnspan=3, pady=5, padx=5)
sell_comic_select_combobox.bind("<<ComboboxSelected>>",sell_comic_selected)

# Sell Stock Item Data #
sell_stock_details_label = ttk.Label(sell_stock_data_parent, text="                         Current Stock: ")
sell_stock_details_label.grid(row=0, column=0)

sell_stock_details_value = ttk.Label(sell_stock_data_parent, text=" - ")
sell_stock_details_value.grid(row=0, column=1)

sell_stock_historical_label = ttk.Label(sell_stock_data_parent, text="                  Historical Sales: ")
sell_stock_historical_label.grid(row=0, column=2)

sell_stock_historical_value = ttk.Label(sell_stock_data_parent, text=" - ")
sell_stock_historical_value.grid(row=0, column=3)

sell_stock_spacer = ttk.Label(sell_stock_data_parent, text="                              ")
sell_stock_spacer.grid(row=0, column=4)

# Sell Stock Sell Button #
sell_stock_button = Button(modify_sales_tab, text="Sell :::  \n", command=sell_stock_button, state='disabled', width=60, anchor=CENTER)
sell_stock_button.grid(row=2, column=0, padx=5)

#***     RUN UPDATES & TKINTER WINDOW     ***#
do_tab_switch_modify("")
do_tab_switch_sales("")
load_stock_data()
print("\n E")
print(series_select_list)
root.mainloop()
