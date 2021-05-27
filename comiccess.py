#***     IMPORT LIBRARIES     ***#
import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import csv
from tempfile import NamedTemporaryFile
import shutil
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
create_status = True
selectitem_series_existing_var = StringVar()

#***     DEFINE CLASSES     ***#
class Comic:
    def __init__(self, series_name, vol_number, issue_name, in_stock, historical_sales):
        self.series_name = series_name
        self.vol_number = vol_number
        self.issue_name = issue_name
        self.vol_issue = 'Vol. ' + self.vol_number + ': ' + self.issue_name
        self.full_title = str(series_name + ' Vol. ' + str(vol_number) + ': ' + issue_name)
        self.in_stock = int(in_stock)
        self.historical_sales = int(historical_sales)
        # adds the comic to the appropriate place in the series_list dictionary
        result = 'no'
        if self.series_name not in series_list:
            series_list[self.series_name] = {self.vol_issue: self} # creates a new key-value in the top dictionary, with the value pointing to a second dictionary that holds the volumes for the key's series.
        elif self.series_name in series_list and self.vol_issue not in series_list[self.series_name]: #adds the comic to the volumes dictionary for its series
            for k, v in series_list[self.series_name].items():
                if vol_number == v.vol_number:
                    messagebox.showerror('Volume Duplicate Error','There is already a Volume {} comic for {}!'.format(self.vol_number, self.series_name)) # if a user tried to create a duplicate comic number, it will throw here
                    result = 'yes'
                else:
                    series_list[self.series_name][self.vol_issue] = self
                    break
        else:
            result = messagebox.askquestion('Comic Duplicate Error','Instance of the {} comic already detected! Would you like to delete the duplicate item?'.format(self.full_title)) # if an error results in a duplicate instance of a volume, it will throw here
        if result=='yes':
            create_status = False
            del self
        else:
            create_status = True

    def create_item_widget(self, location): # creates the item listing in the index results canvas
        self.item_frame = ttk.Frame(location, relief=SUNKEN)
        self.mod_title = ttk.Label(self.item_frame, text=self.full_title, anchor=CENTER, font='Bahnschrift 10 bold').grid(column=0, row=0, columnspan=2, sticky="ew")
        self.mod_stock_label = ttk.Label(self.item_frame, text="In Stock", anchor=CENTER).grid(column=0, row=1, sticky="ew")
        self.mod_hist_label = ttk.Label(self.item_frame, text="Historic Sales", anchor=CENTER).grid(column=1, row=1, sticky="ew")
        self.mod_stock_item = ttk.Label(self.item_frame, text=self.in_stock, anchor=CENTER).grid(column=0, row=2, sticky="ew")
        self.mod_hist_item = ttk.Label(self.item_frame, text=self.historical_sales, anchor=CENTER).grid(column=1, row=2, sticky="ew")
        self.item_frame.pack()
        self.line_frame = ttk.Frame(location)
        self.line_frame.pack()
        self.obj_line = ttk.Separator(self.line_frame, orient=HORIZONTAL)
        self.obj_line.pack(fill="both", expand=True)
        
    def clear_all(self): # erases the comic from the active program. Only called on error, or when it is about to be re-loaded from the file.
        try:
            self.line_frame.forget()
            self.item_frame.forget()
            del self
        except:
            del self
    
#***     LOAD DATA FROM FILES     ***#
def load_stock_data(): # used to set the data in the window to the latest available from file. triggered on startup and by update_save_data()
    global stock_items_class_list, series_list, series_select_list, vol_select_list, do_restore, restore_var
    for item in stock_items_class_list: # wipes all comic objects from the system and clears the display window
        item.clear_all()
    # resets all global lists to original values
    series_list = {}
    series_select_list = [""]
    vol_select_list = [""]
    line_count = 0
    stock_items_class_list = []
    with open('stock.csv', 'r', newline='') as csv_file: # imports all stored data from file
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                #print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                stock_items_class_list.append(Comic(row[0], row[1], row[2], row[3], row[4])) # generates an instance of Comic with the given values
                line_count += 1
        print(f'Processed {line_count-1} item/s.')
        for i in range(len(stock_items_class_list)):
            stock_items_class_list[i].create_item_widget(index_results_frame) # generates the index results object for each comic
        update_lists() # initialises dropdown menu options
    if do_restore == True: #restores to previous state if necessary
        if restore_var[0] == "modify":
            selectitem_existing_series.set(restore_var[1])
            existing_series_selected("")
            selectitem_existing_vol.set(restore_var[2])
            existing_vol_selected("")
            
        elif restore_var[0] == "sell":
            sell_series_select_combobox.set(restore_var[1])
            sell_series_selected("")
            sell_comic_select_combobox.set(restore_var[2])
            sell_comic_selected("")
        do_restore = False
    csv_file.close()  

#***     DEFINE FUNCTIONS     ***#
def update_lists(): # initialises the dropdown menues where existing series are the only options
    global series_list, series_select_list
    for item in series_list.keys():
        series_select_list.append(item)
    selectitem_existing_series.config(values=series_select_list)
    selectitem_create_series.config(values=series_select_list)
    sell_series_select_combobox.config(values=series_select_list)

def do_tab_switch_sales(event): # switches right-region tab to focus on Sales
    global tab_startup_status
    if tab_startup_status == False:
        modify_manage_stock_tab.forget()
        modify_sales_tab.pack(side="left", fill="both", expand=True)
        tab_startup_status = True
    
def do_tab_switch_modify(event): # switches right-region tab to focus on Modify Stock
    global tab_startup_status
    if tab_startup_status == True:
        modify_sales_tab.forget()
        modify_manage_stock_tab.pack(side="left", fill="both", expand=True)
        tab_startup_status = False
    

#* Comics Selection Functions *#
def existing_series_selected(event): # handles various events associated with the modify existing frame
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
        for key, val_list in series_list.items(): # initialises the volume selection options for a chosen series
            if selectitem_existing_series.get() == key:
                for item in val_list.keys():
                    vol_select_list.append(item)
        selectitem_existing_vol.config(values=vol_select_list)
        selectitem_create_series.set("")
        selectitem_create_series.config(state='disabled')
        
def existing_vol_selected(event): # enables or disables the operator selection frame
    if selectitem_existing_vol.get() == "":
        selectitem_existing_operator.config(state='disabled')
        selectitem_existing_operator.set("")
        selectitem_existing_number.delete(0, END)
        selectitem_existing_number.config(state='disabled')
        selectitem_apply_changes_button.config(state='disabled')
    else:
        selectitem_existing_operator.config(state='readonly')

def existing_operator_selected(event): # enables or disables number entry
    if selectitem_existing_operator.get() == "":
        selectitem_existing_number.delete(0, END)
        selectitem_existing_number.config(state='disabled')
        selectitem_apply_changes_button.config(state='disabled')
    else:
        selectitem_existing_number.config(state='normal')
    
def existing_number_validate(char): #used to ensure that only numbers can be entered in entry frames to which it is applied
    if char.isdigit():
        return True
    else:
        return False

def selectitem_existing_num_command(event): #enables apply changes button
    if selectitem_existing_number.get() == "":
        selectitem_apply_changes_button.config(state='disabled')
    else:
        selectitem_apply_changes_button.config(state='normal')
        

def created_series_selected(event): # focuses user on created series frames, and enables or disables following interaction points
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

def created_vol_num_selected(event): # enables or disables volume name selection
    if selectitem_create_vol_entry.get() == "":
        selectitem_create_vol_name.delete(0, END)
        selectitem_create_vol_name.config(state='disabled')
        selectitem_create_init_stock.delete(0, END)
        selectitem_create_init_stock.config(state='disabled')
        selectitem_apply_changes_button.config(state='disabled')
    else:
        selectitem_create_vol_name.config(state='normal')
        
def created_vol_name_selected(event): # enables initial stock value
    if selectitem_create_vol_name.get() == "":
        selectitem_create_init_stock.delete(0, END)
        selectitem_create_init_stock.config(state='disabled')
        selectitem_apply_changes_button.config(state='disabled')
    else:
        selectitem_create_init_stock.config(state='normal')
    
def created_comic_init_stock_selected(event): #enables or disables create commic application button
    if selectitem_create_init_stock.get() == "":
        selectitem_apply_changes_button.config(state='disabled')
    else:
        selectitem_apply_changes_button.config(state='normal')

def selectitem_apply_changes(): # updates the data if the user is in the Modify Stock tab
    global create_status # used to ensure that there are no issues if a comic is being created.
    if selectitem_existing_series.get() != "":
        comic_class_instance = series_list[selectitem_existing_series.get()][selectitem_existing_vol.get()]
        stock_action = selectitem_existing_operator.get()
        stock_number = int(selectitem_existing_number.get())
        do_clear = False
        if stock_action == "SET": # set stock to entered number
            comic_class_instance.in_stock = stock_number
            do_clear = True
        elif stock_action == "+": # adds a specified number of items to the stock count
            comic_class_instance.in_stock += stock_number
            do_clear = True
        elif stock_action == "-": # allows for decreasing stock by more than one
            if stock_number <= comic_class_instance.in_stock:
                comic_class_instance.in_stock -= stock_number
                do_clear = True
            else:
                messagebox.showerror('Stock Error!', 'You tried to remove more comics than were in stock. Try again.') # triggered if the user tries to decrease the stock below its limit 0
                do_clear = False
                selectitem_existing_number.delete(0, END)
                selectitem_existing_num_command("")
        if do_clear == True:
            restore_var = ("modify",comic_class_instance.series_name, comic_class_instance.vol_issue)
            selectitem_existing_series.set("")
            existing_series_selected("")
            update_save_data() # triggers data save update
    elif selectitem_create_series.get() != "": # triggers if the chosen function is to add a comic.
        series_name = selectitem_create_series.get()
        vol_number = selectitem_create_vol_entry.get()
        issue_name = selectitem_create_vol_name.get()
        in_stock = selectitem_create_init_stock.get()
        title_data = str(series_name + ' Vol. ' + vol_number + ': ' + issue_name + "\n - " + in_stock + " in stock, and " + "0" + " have been sold.")
        full_title_var = str(series_name + vol_number + issue_name).strip(",. ").lower().replace(",", "").replace(".", "").replace(" ","")
        stock_items_class_list.append(Comic(series_name, vol_number, issue_name, in_stock, 0)) # adds a new comic instance to the list
        if create_status == True:
            selectitem_create_series.set("")
            created_series_selected("")
            create_status = False
        else:
            selectitem_create_vol_entry.delete(0, END)
            created_vol_name_selected("")
        update_save_data() # triggers data save update
    else: 
        pass

def sell_series_selected(event): # clears or configures the comic selection combobox and other options below it.
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

def sell_comic_selected(event): # clears or configures the item information frame
    if sell_comic_select_combobox.get() == "":
        sell_stock_data_parent.config(text="Comic: ")
        sell_stock_details_value.config(text=" - ")
        sell_stock_historical_value.config(text=" - ")
        sell_stock_button.config(state='disabled', text='Sell :::  \n')
    else:
        selected_item = series_list[sell_series_select_combobox.get()][sell_comic_select_combobox.get()]
        sell_stock_data_parent.config(text=" {} ".format(selected_item.full_title))
        sell_stock_details_value.config(text=" {} ".format(selected_item.in_stock))
        sell_stock_historical_value.config(text=" {} ".format(selected_item.historical_sales))
        sell_stock_button.config(state='normal', text='Sell ::: \n{}'.format(selected_item.full_title))

def sell_stock_button():
    pass
    selected_item = series_list[sell_series_select_combobox.get()][sell_comic_select_combobox.get()] # selects the comic object located as the value of a dictionary stored within another dictionary.
    clearitem = False
    if selected_item.in_stock > 0: # ensures that there are items in stock
        selected_item.in_stock -= 1
        selected_item.historical_sales += 1
        clearitem = True
        messagebox.showinfo('Success!', 'You have sold an item of stock!') # 
    else:
        messagebox.showerror('Out of stock!', 'It looks like that item is out of stock, sorry!') # shows an error window
    if clearitem == True:
        restore_var = ("sell",selected_item.series_name,selected_item.vol_issue) # stores the data that will be used to return the program to its state after the data is updated.
        update_save_data()
    sell_comic_selected("")
    
def update_save_data():
    do_restore = True # activates the restore function to allow the program to return to its prior state when updating data
    tempfile = NamedTemporaryFile(mode='w', delete=False, newline='') # creates a tempfile per Python standards.
    with open('stock.csv', newline='') as csv_file, tempfile:
        csv_reader = csv.reader(csv_file, delimiter=',')
        csv_writer = csv.writer(tempfile, delimiter=',')
        rowcount = 0
        for row in csv_reader:
            if rowcount == 0:
                csv_writer.writerow(row) # returns the header row to the tempfile
                rowcount += 1
        for k, v in series_list.items(): #iterates over each comic series
            for k, v in series_list[k].items(): # iterates over each volume within the list
                rowcount += 1
                csv_writer.writerow((v.series_name, v.vol_number, v.issue_name, v.in_stock, v.historical_sales)) # adds the item to the tempfile
    shutil.move(tempfile.name, 'stock.csv') # transfers tempfile data into loading file
    load_stock_data() # resets and restarts program from scratch state, loading from stock.csv.

#***     TKINTER WINDOW     ***#
 # Tkinter style with Dark Sky Blue background, used to colour item headers appropriately
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

 # THESE WERE REMOVED due to a lack of time to build the associated function, and serve no purpose here.
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

index_results_frame.bind("<Configure>", lambda e: index_results_canvas.configure(scrollregion=index_results_canvas.bbox("all"))) # Bind the scrollbar to the results canvas

index_results_canvas.create_window((0, 0), window=index_results_frame, anchor="nw")
index_results_canvas.configure(yscrollcommand=index_results_scrollbar.set)

index_results_canvas.pack(side="left", fill="both", expand=True)
index_results_scrollbar.pack(side="right", fill="y")

topline = ttk.Label(index_results_frame, text="––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––").pack() #separate INDEX from results region
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

# SelectItem Existing # (Allows modification of the stock of a given )
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

selectitem_existing_number_validation = selectitem_existing_parent.register(existing_number_validate) # guarantees that only a number can be entered into stock modifier value
selectitem_existing_number = ttk.Entry(selectitem_existing_parent, textvariable=selectitem_existing_number_var, state='disabled', width=23, validate='all', validatecommand=(selectitem_existing_number_validation, '%S'))
selectitem_existing_number.grid(row=2, column=1, pady=5)
selectitem_existing_number.bind("<KeyRelease>",selectitem_existing_num_command)
                
# SelectItem CreateNew #
selectitem_create_series_label = ttk.Label(selectitem_new_parent, text="Series:  ")
selectitem_create_series_label.grid(row=0, column=0)

selectitem_create_series = ttk.Combobox(selectitem_new_parent, values=series_select_list)
selectitem_create_series.grid(row=0, column=1, pady=5)
selectitem_create_series.bind("<<ComboboxSelected>>",created_series_selected)
selectitem_create_series.bind("<KeyRelease>",created_series_selected) # necessary due to option for Text Entry

selectitem_create_vol_frame = ttk.Frame(selectitem_new_parent)
selectitem_create_vol_frame.grid(row=1, column=0, columnspan=2)

selectitem_create_vol_label = ttk.Label(selectitem_create_vol_frame, text="  Vol.")
selectitem_create_vol_label.grid(row=0, column=0)

selectitem_create_vol_entry_validation = selectitem_create_vol_frame.register(existing_number_validate) # guarantees that only a number can be entered into volume number
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

selectitem_create_init_stock_validation = selectitem_new_parent.register(existing_number_validate) # guarantees that only a number can be entered into initial stock
selectitem_create_init_stock = ttk.Entry(selectitem_new_parent, width=23, textvariable=selectitem_create_init_stock_var, state='disabled', validate='all', validatecommand=(selectitem_create_init_stock_validation, '%S'))
selectitem_create_init_stock.grid(row=2, column=1, pady=5)
selectitem_create_init_stock.bind("<KeyRelease>",created_comic_init_stock_selected) # activates Apply Changes button

# SelectItem Apply Changes #
selectitem_apply_changes_button = ttk.Button(manage_stock_selectitem_parent, text="Apply Changes", command=selectitem_apply_changes, state='disabled', width=70) #triggers function to update window and data
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
sell_series_select_combobox.bind("<<ComboboxSelected>>",sell_series_selected) # triggers value update when combobox is used

sell_comic_select_label = ttk.Label(sell_stock_selectitem_parent, text="Select Comic: |")
sell_comic_select_label.grid(row=1, column=0)

sell_comic_select_combobox = ttk.Combobox(sell_stock_selectitem_parent, values="", state='disabled', width=54)
sell_comic_select_combobox.grid(row=1, column=1, columnspan=3, pady=5, padx=5)
sell_comic_select_combobox.bind("<<ComboboxSelected>>",sell_comic_selected) # triggers value update when combobox is used

# Sell Stock Item Data # (formats item information readout)
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
load_stock_data() # initialise data from file stock.csv
root.mainloop()
