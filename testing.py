import os
from Task2 import Task
import time
import datetime
import pickle
from tkinter import *
from tkinter import ttk
from tkinter import font
from tkinter import messagebox


root = Tk()

update_check_list = [True,True,True,True]
update_date_list = ['01/01/21  12:00','02/01/21  12:00','03/01/21  12:00','04/01/21  12:00']
update_description_list = ['description 1','description 2','description 3','description 4']

frm1 = Frame(root)
frm1.pack(side=LEFT, expand=1, fill=Y, padx=(5,10), pady=(5,10))

tv = ttk.Treeview(frm1)
tv.grid()


lb_var = StringVar()
frm2 = LabelFrame(root, text=f"  Updates:  {len(update_check_list):02d}  ")
frm2.pack(side=LEFT, expand=1, fill=Y, padx=(5,10), pady=(5,10))

def confirm_mark_all(event):

    c1_status = c1_var.get()
    if c1_status == 0:
        msg = "Mark all updates as complete."
    else:
        msg = "Mark all updates as incomplete."

    result = messagebox.askquestion("Confirm", f"{msg} Are you sure?", icon='warning')
    if result == 'yes':
        for cont, check in enumerate(c_vars):
            if update_check_list[cont] == c1_status:
                update_check_list[cont] = not update_check_list[cont]
            else:
                pass
            c_vars[cont].set(not c1_status)
            c1_var.set(not c1_status)
        print(update_check_list)
    else:
        pass

    root.focus()

c1_var = BooleanVar()
# c_vars.append(c_var)
c1 = Checkbutton(frm2, variable=c1_var)
c1_var.set(True)
for item in update_check_list:
    if item == False:
        c1_var.set(False)
    
c1.bind("<ButtonPress-1>", confirm_mark_all)
# update_check_objects.append(c)
c1.grid(row=0, column=0, padx=(0,0), pady=(0,0))

lb1 = Label(frm2, text='Date', anchor='w')
lb1.grid(row=0, column=1, sticky=EW, padx=(0,0), pady=(0,0))

lb2 = Label(frm2, text='Description', anchor='w')
lb2.grid(row=0, column=2, sticky=EW, padx=(10,0), pady=(0,0))

update_check_objects = []
update_date_objects = []
update_description_objects = []

c_vars = []
e_update_date_vars = []
e_description_vars = []

def update_all():
    for cont, date in enumerate(update_date_objects):
        # check = c_vars[cont].get()
        update_date = date.get()
        description = update_description_objects[cont].get()

        # update_check_list[cont] = check
        update_date_list[cont] = update_date
        update_description_list[cont] = description

def press_enter(event):
    update_all()

def check_click(event):
    check = event.widget
    check_id = update_check_objects.index(check)
    update_check_list[check_id] = not update_check_list[check_id]
    update_all()
    root.focus()
    print(update_check_list)
    if False in update_check_list:
        c1_var.set(False)
    else:
        c1_var.set(True)

    if True in update_check_list:
        print("tem true")
    else:
        c1_var.set(False)
    print(update_date_list)
    print(update_description_list)

for cont, item in enumerate(update_date_list):

    c_var = BooleanVar()
    c_vars.append(c_var)
    c = Checkbutton(frm2, variable=c_vars[cont])
    c.bind("<ButtonPress-1>", check_click)
    update_check_objects.append(c)
    c.grid(row=cont+1, column=0, padx=(0,0), pady=(0,0))

    if update_check_list[cont] == 0:
        c_vars[cont].set(False)
    else:
        c_vars[cont].set(True)


    e_update_date_var = StringVar()
    e_update_date_vars.append(e_update_date_var)
    e = Entry(frm2, textvariable=e_update_date_vars[cont])

    update_date_objects.append(e)
    update_date_objects[cont].bind('<ButtonPress-1>', press_enter)

    e.grid(row =cont+1, column=1, padx=(0,0), pady=(0,0))
    e.insert(0, item)

    e_description_var = StringVar()
    e_description_vars.append(e_description_var)
    e = Entry(frm2, textvariable=e_description_vars[cont], width=30)

    update_description_objects.append(e)
    update_description_objects[cont].bind('<ButtonPress-1>', press_enter)

    e.grid(row =cont+1, column=2, padx=(10,0), pady=(0,0))
    e.insert(0, update_description_list[cont])


root.bind('<Return>', press_enter) 

root.mainloop()