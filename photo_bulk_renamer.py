from datetime import datetime
import os
import glob
import re
import tkinter as tk
import tkinter.filedialog
from tkinter import ttk

# Function that actually renames the files
def pick_folder():
    path = tk.filedialog.askdirectory(title = "Select a folder")
    entry_directory.delete(0, tk.END)
    entry_directory.insert(0, path)


# Checks if there are any files in the given path which do NOT match the regex expression
# but are of the same file type. These files should be renamed. The function returns the
# number of files left.
def find_files_to_rename(path, list_of_filetypes_to_change):
    global file_count
    file_count = 0
    for filetype in list_file_types:
        for file in glob.glob(pathname = ("*." + filetype)):        # goes over each file in the directory
            if re.match("^...._..__([A-Z][a-z]*)*__[0-9][0-9][0-9].*$", file):
                # TODO: WARN USER THAT THERE IS ALREADY A FILE WITH THE SAME NAME FORMAT IN THIS FOLDER
                print("Whoops, there is already a file in this folder which has been renamed.")
            else:
                print("File found: " + path + "/" + file)
                new_file_name = create_new_file_name( file_count + 1, filetype )
                print("Created new file name: " + new_file_name)
                print(new_file_name) 
                change_file_name(file, new_file_name)
                file_count += 1
    return(file_count)


def create_new_file_name(file_number, filetype):
    year = str(drop_year.current() + 1994)
    int_month = drop_month.current() + 1
    if int_month < 10:
        month = "0" + str(int_month)
    else:
        month = str(int_month)
    theme = str(entry_theme.get())
    if file_number < 10:
        number = "00" + str(file_number)
    elif file_number <100:
        number = "0" + str(file_number)
    else:
        number = str(file_number)
    new_filename = year + "_" + month + "__" + theme + "__" + number + "." + filetype
    return(new_filename)


def change_file_name(old_file_name, new_file_name):
    print("changing file name:      from: " + old_file_name + "           to: " + new_file_name)
    os.rename(old_file_name, new_file_name)

def execute(path, list_file_types):
    path = entry_directory.get()
    os.chdir( path )
    print("Working directory changed to " + path )    
    
    print("Total found: " + str(find_files_to_rename( path, list_file_types )))
    #if( find_files_to_rename( path, list_file_types ) != 0 ):
    #    #create_new_file_name(file_number)

###############
## Variables ## 
###############

path = ""


####################
##  Current Date  ##
####################

# Date as strings
current_date = str(datetime.today())
current_year = current_date[:4]
current_month = current_date[5:7]


##############
## Mainloop ##
##############
root = tk.Tk()
topframe = tk.Frame(root)
bottomframe = tk.Frame(root)

topframe.pack()
bottomframe.pack()

root.title("Bulk Photo Renamer")

list_years = [1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005,
              2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017,
              2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027, 2028, 2029, 2030]
list_months = ["January", "February", "March", "April", "May", "June", "July", "August",
               "September", "October", "November", "December"]
label_howto      = tk.Label(topframe, text = "Select a folder to rename all the photos inside.")
entry_directory  = tk.Entry(topframe, width = 77)
button_directory = tk.Button(topframe, text = "Pick folder", command = pick_folder)
tkstr_theme      = tk.StringVar(root)
drop_year        = ttk.Combobox(bottomframe, values = list_years)
drop_year.current(int(current_year) - 1994)
drop_month       = ttk.Combobox(bottomframe, values = list_months)
drop_month.current(int(current_month) - 1)
entry_theme      = tk.Entry(bottomframe, width = 30)
list_file_types       = ["jpg", "png", "jpeg", "gif", "tiff"]
button_execute   = tk.Button(bottomframe, text = "Change names", command = lambda: execute( path, list_file_types ))
radio_file_type = tk.Radiobutton(root, text = ".jpg")

#warning_file_found_with_format = tk.messagebox.askquestion(title = "Warning", message = "At least one file in this folder has already been renamed. Do you wish to rename this file?")

label_howto.grid(row = 0, column = 0, padx = 10, pady = 10)
entry_directory.grid(row = 1, column = 0, padx = (10,5))
button_directory.grid(row = 1, column = 3, padx = (5,10))
drop_year.grid(row = 2, column = 1, padx = (10,5))
drop_month.grid(row = 2, column = 2, padx = (5,5))
entry_theme.grid(row = 2, column = 3, padx = (5,5))
button_execute.grid(row = 2, column = 4, padx = 10, pady = (5, 10))
#label_howto.pack(side = tk.TOP)
#entry_directory.pack(side = tk.TOP)
#button_directory.pack(side = tk.TOP)


root.mainloop()