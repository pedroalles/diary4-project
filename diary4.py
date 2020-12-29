import os
import sys

import time
import datetime
import pickle

from tkinter import *
from tkinter import ttk
from tkinter import font
from tkinter import messagebox


from Task import Task

###################################################################################################

save_path = f"C:\\Users\\{os.getlogin()}\\Documents\\saves.pkl"
task_list = []

###################################################################################################

root = Tk()
root.title('Diary 4')
root.configure(background='black')

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

window_height = 700
window_width = 1250

x_cordinate = int((screen_width/2) - (window_width/2))
y_cordinate = int((screen_height/2) - (window_height/2))

root.geometry("+{}+{}".format(x_cordinate, 0))
root.resizable(False, False)

###################################################################################################

def deselect(event):
    selection = tv.selection()
    if len(selection) > 0:
        tv.selection_remove(tv.selection()[0])

root.bind('<Escape>', deselect)    

def done_update():

    selection = tv.selection()
    if selection:

        item = tv.item(selection)
        id_ = int(item["values"][0])
        task_list[id_ -1].change_status_task()
        add_tv_rows()
        child_id = tv.get_children()[id_ -1]
        tv.selection_set(child_id)


def task_update(event=None):

    up_task_title = entryTitle.get()
    up_task_decription = entryDescription.get()
    up_task_updecription = entryUpdateDescription.get()


    selection = tv.selection()
    if selection:

        item = tv.item(selection)
        id_ = int(item["values"][0])

        task_list[id_ -1].task_title = up_task_title
        task_list[id_ -1].task_description = up_task_decription

        updates = (len(task_list[int(item['values'][0])-1].update_list))
        if updates > 0:
            task_list[id_ -1].update_list[-1][1] = up_task_updecription

        add_tv_rows()
        child_id = tv.get_children()[id_ -1]
        tv.selection_set(child_id)
     

root.bind('<Return>', task_update)

###################################################################################################

frame_inputs = Frame(root, bg='black')
frame_inputs.grid(row=2, column=0)

frame_variable = StringVar()
lf = LabelFrame(frame_inputs, text="Task ID:  00  ", font=(None, 11), bg='black', fg='white')
lf.grid(row=0, column=0, padx=10, pady=10, ipadx=5, ipady=3)

labelStartDate = Label(lf, text="Start Date", font=(None, 11), bg='black', fg='white')
labelStartDate.grid(row=0, column=1, sticky=EW, padx=10, pady=0)

startDate_variable = StringVar()
entryStartDate = Entry(lf, width= 13, justify='center', textvariable=startDate_variable, font=(None, 11), bg='black', fg='white', insertbackground='white')
entryStartDate.grid(row=1, column=1, sticky=EW, padx=10, pady=0)

labelTitle = Label(lf, text="Title", font=(None, 11), bg='black', fg='white')
labelTitle.grid(row=0, column=2, sticky=EW, padx=0, pady=0)

title_variable = StringVar()
entryTitle = Entry(lf, width= 15, justify='center', textvariable=title_variable, font=(None, 11), bg='black', fg='white', insertbackground='white')
entryTitle.grid(row=1, column=2, sticky=EW, padx=0, pady=0)

labelDescription = Label(lf, text="Description", font=(None, 11), bg='black', fg='white')
labelDescription.grid(row=0, column=3, sticky=EW, padx=10, pady=0)

description_variable = StringVar()
entryDescription = Entry(lf, width= 20, justify='center', textvariable=description_variable, font=(None, 11), bg='black', fg='white', insertbackground='white')
entryDescription.grid(row=1, column=3, sticky=EW, padx=10, pady=0)

labelUpdateDate = Label(lf, text="Last Update", font=(None, 11), bg='black', fg='white')
labelUpdateDate.grid(row=0, column=4, sticky=EW, padx=0, pady=0)

updateDate_variable = StringVar()
entryUpdateDate = Entry(lf, width= 13, justify='center', textvariable=updateDate_variable, font=(None, 11), bg='black', fg='white', insertbackground='white')
entryUpdateDate.grid(row=1, column=4, sticky=EW, padx=0, pady=0)

labelUpdateDescription = Label(lf, text="Last Update Description", font=(None, 11), bg='black', fg='white')
labelUpdateDescription.grid(row=0, column=5, sticky=EW, padx=10, pady=0)

updateDescription_variable = StringVar()
entryUpdateDescription = Entry(lf, width= 15, justify='center', textvariable=updateDescription_variable, font=(None, 11), bg='black', fg='white', insertbackground='white')
entryUpdateDescription.grid(row=1, column=5, sticky=EW, padx=10, pady=0)

labelDone = Label(lf, text="Done", font=(None, 11), bg='black', fg='white')
labelDone.grid(row=0, column=8, sticky=EW, padx=(10,0), pady=0)

var = BooleanVar() 
var.set(False)
entryActive = Checkbutton(lf, variable=var, font=(None, 11), bg='black', activebackground='black', command=done_update)
entryActive.grid(row=1, column=8, sticky=EW, padx=(20,0), pady=0)

labelListUpdates = Label(lf, text="Update List", font=(None, 11), bg='black', fg='white')
labelListUpdates.grid(row=0, column=7, sticky=EW)

box_value = StringVar()
box = ttk.Combobox(lf, width= 41, justify='center', textvariable=box_value, state='readonly', font=(None, 11))
box.grid(row=1, column=7, sticky=EW)

###################################################################################################

frame_tree = Frame(root, bg='black')
frame_tree.grid(row=1, column=0, pady=(10,0), padx=(10))

tv_scroll = Scrollbar(frame_tree)
tv_scroll.pack(side=RIGHT, fill=Y, pady=(0))

def disableEvent(event):
    if tv.identify_region(event.x, event.y) == "separator":
        return "break"

tv = ttk.Treeview(frame_tree, yscrollcommand=tv_scroll.set)
tv.pack()

tv.bind("<Button-1>", disableEvent)

tv_scroll.config(command=tv.yview)

tv["column"] = ['ID','Start Date','Title','Description','Last Update','Last Update Description','Done']
tv["show"] = "headings"

tv.column("ID", minwidth=50, width=50, anchor='center')
tv.column("Start Date", minwidth=150, width=150, anchor='center')
tv.column("Title", minwidth=190, width=190, anchor='w')
tv.column("Description", minwidth=250, width=250, anchor='w')
tv.column("Last Update", minwidth=150, width=150, anchor='center')
tv.column("Last Update Description", minwidth=250, width=250, anchor='w')
tv.column("Done", minwidth=70, width=70, anchor='center')

def treeview_sort_column(tv, col, reverse):

    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    try:
        l.sort(key=lambda t: float(t[0]), reverse=reverse)

    except ValueError:
        l.sort(reverse=reverse)

    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)

    tv.heading(col, command=lambda: treeview_sort_column(tv, col, not reverse)) 

    tv.yview_moveto(0) #move scrollbar to top

for column in tv["column"]:
    tv.heading(column, text=column, command=lambda _col=column: treeview_sort_column(tv, _col, False))

###################################################################################################

def add_task():

    global task_list
    id_ = len(task_list) + 1

    newWindow = Toplevel(root) 
    newWindow.title('Diary 4')
    newWindow.configure(background='black')

    screen_width = newWindow.winfo_screenwidth()
    screen_height = newWindow.winfo_screenheight()

    window_height = 450
    window_width = 200

    x_cordinate = int((screen_width/2) - (window_width/2))
    y_cordinate = int((screen_height/2) - (window_height/2))

    newWindow.geometry("+{}+{}".format(x_cordinate, y_cordinate))
    newWindow.resizable(False, False)

    frame_add = Frame(newWindow, bg='black')
    frame_add.grid(row=0, column=0)

    frame_add_var = StringVar()
    lfadd = LabelFrame(frame_add, text=f"Task ID:  {id_}  ", font=(None, 11), bg='black', fg='white')
    lfadd.grid(row=0, column=0, padx=10, pady=10, ipadx=5, ipady=0)

    labeladd = Label(lfadd, text="Title", font=(None, 11), bg='black', fg='white')
    labeladd.grid(row=0, column=0, sticky=EW, padx=10, pady=5)

    add_var_title = StringVar()
    entryadd = Entry(lfadd, width= 30, justify='center', textvariable=add_var_title, font=(None, 11), bg='black', fg='white', insertbackground='white')
    entryadd.grid(row=1, column=0, sticky=EW, padx=10, pady=0)

    labeladddesc = Label(lfadd, text="Description", font=(None, 11), bg='black', fg='white')
    labeladddesc.grid(row=2, column=0, sticky=EW, padx=10, pady=5)

    add_var_desc = StringVar()
    entryadddesc = Entry(lfadd, width= 30, justify='center', textvariable=add_var_desc, font=(None, 11), bg='black', fg='white', insertbackground='white')
    entryadddesc.grid(row=3, column=0, sticky=EW, padx=10, pady=0)

    entryadd.focus()

    def add_task_commit():

        new_task_title = entryadd.get()
        new_task_decription = entryadddesc.get()
        start_date = str(datetime.datetime.fromtimestamp(int(time.time())).strftime('%d/%m/%y  %H:%M'))
        task_list.append(Task(id_, new_task_title, new_task_decription, start_date))

        add_tv_rows()
        child_id = tv.get_children()[id_ -1]
        tv.selection_set(child_id)
        newWindow.destroy()

    buttonaddup = Button(lfadd, text='Add Task', command=add_task_commit)
    buttonaddup.grid(row=4, column=0, padx=10, pady=(10,8), ipadx=5)

def delete_task():

    selection = tv.selection()
    if selection:

        item = tv.item(selection)

        id_ = int(item["values"][0])
        result = messagebox.askquestion("Delete", "Are You Sure?", icon='warning')
        if result == 'yes':
            
            task_list.pop(id_ -1)

            for cont, task in enumerate(task_list, start=1):
                task.task_id = cont 

            add_tv_rows()
            clear_inputs()

        else:
            pass

def call_delete(event):
    delete_task()

root.bind('<Delete>', call_delete)

def clear_inputs():

    entryStartDate.delete(0, "end")
    entryTitle.delete(0, "end")
    entryDescription.delete(0, "end")
    entryUpdateDate.delete(0, "end")
    entryUpdateDescription.delete(0, "end")
    var.set(False)
    box.set('')
    box['values'] = ""

def add_update():

    selection = tv.selection()
    if selection:

        item = tv.item(selection)
        id_ = int(item["values"][0])

        newWindow = Toplevel(root) 
        newWindow.title('Diary 4')
        newWindow.configure(background='black')

        screen_width = newWindow.winfo_screenwidth()
        screen_height = newWindow.winfo_screenheight()

        window_height = 450
        window_width = 200

        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))

        newWindow.geometry("+{}+{}".format(x_cordinate, y_cordinate))
        newWindow.resizable(False, False)

        frame_up = Frame(newWindow, bg='black')
        frame_up.grid(row=0, column=0)

        frame_up_var = StringVar()
        lfup = LabelFrame(frame_up, text=f"Task ID:  {id_}  ", font=(None, 11), bg='black', fg='white')
        lfup.grid(row=0, column=0, padx=10, pady=10, ipadx=5, ipady=0)

        labelupdesc = Label(lfup, text="Update Description", font=(None, 11), bg='black', fg='white')
        labelupdesc.grid(row=0, column=0, sticky=EW, padx=10, pady=5)

        update_var = StringVar()
        entryupdesc = Entry(lfup, width= 30, justify='center', textvariable=update_var, font=(None, 11), bg='black', fg='white', insertbackground='white')
        entryupdesc.grid(row=1, column=0, sticky=EW, padx=10, pady=0)
        entryupdesc.focus()
    
        def add_update_commit():

            new_update_desc = entryupdesc.get()
            update_date = str(datetime.datetime.fromtimestamp(int(time.time())).strftime('%d/%m/%y  %H:%M'))
            task_list[id_ -1].add_update_task(update_date, new_update_desc)
            add_tv_rows()
            child_id = tv.get_children()[id_ -1]
            tv.selection_set(child_id)
            newWindow.destroy()

        buttonaddup = Button(lfup, text='Add Update', command=add_update_commit)
        buttonaddup.grid(row=2, column=0, padx=10, pady=(10,8), ipadx=5)

###################################################################################################

frame_buttons = Frame(root, bg='black')
frame_buttons.grid(row=3, column=0, pady=(0,10))

buttonAddTask = Button(frame_buttons, borderwidth=4, font=(None, 11), width=10, text='Add Task', command=add_task, bg='SteelBlue2')
buttonAddTask.grid(row=0, column=0, padx=(0,50))

buttonDeleteTask = Button(frame_buttons, borderwidth=4, font=(None, 11), width=10, text='Delete Task', command=delete_task, bg='Tomato3')
buttonDeleteTask.grid(row=0, column=1)

buttonAddUpdate = Button(frame_buttons, borderwidth=4, font=(None, 11), width=10, text='Add Update', command=add_update, bg='Green3')
buttonAddUpdate.grid(row=0, column=2, padx=(50,50))

###################################################################################################

style = ttk.Style()
style.theme_use("default")

style.configure("Treeview.Heading", font=(None, 13), borderwidth=4, background='SteelBlue2', foreground="black", fieldbackground='black')
style.configure("Treeview", font=(None, 12), borderwidth=4, background='black', foreground="white", fieldbackground='black')

style.map("Treeview.Heading", foreground=[('pressed', 'white')], background=[('pressed', 'black')])
style.map("Treeview", foreground=[('selected', 'black')],  background=[('selected', 'SteelBlue2')])

style.map('TCombobox', fieldbackground=[('readonly','black')])
style.map('TCombobox', background=[('readonly', 'SteelBlue2')])
style.map('TCombobox', foreground=[('readonly', 'white')])
style.map('TCombobox', selectbackground=[('readonly', 'black')])
style.map('TCombobox', selectforeground=[('readonly', 'white')])

bigfont = font.Font(family="Helvetica",size=11)
root.option_add("*TCombobox*Listbox*Font", bigfont)

root.option_add('*TCombobox*Listbox.Background', 'black') 
root.option_add('*TCombobox*Listbox.Foreground', 'white') 
root.option_add('*TCombobox*Listbox.selectBackground', 'SteelBlue2') 

# root.option_add('*TCombobox*Listbox.Justify', 'center')

style.configure( 'Vertical.TScrollbar', background='SteelBlue2' )

###################################################################################################

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

if os.path.exists((save_path)):
    with open((save_path), 'rb') as f:
        task_list = pickle.load(f)

def add_tv_rows():

    for i in tv.get_children():
        tv.delete(i)

    rows = []
    for cont, task in enumerate(task_list):

        task_id_ = f'{int(task_list[cont].task_id):02d}'

        try:
            last_update_date =  task_list[cont].update_list[-1][0]
            last_update_description =  task_list[cont].update_list[-1][1]
        except:
            last_update_date = ''
            last_update_description = ''

        done_status_print = ''
        done_status = str(task_list[cont].task_done_status)
        if done_status == "False":
            done_status_print = 'No'
        else:
            done_status_print = 'Yes'

        rows.append([   task_id_,
                        task_list[cont].task_start_date,
                        task_list[cont].task_title,
                        task_list[cont].task_description,
                        last_update_date,
                        last_update_description,
                        done_status_print
                        ])

    for row in rows:
        tv.insert("", "end", values=row)

add_tv_rows()

def handle_selection(event):

    global item

    clear_inputs()

    selection = tv.selection()
    if selection:

        item = tv.item(selection)

        lf.configure(text=f'Task ID:  {item["values"][0]:02d}  ')
        entryStartDate.insert(0, item['values'][1])
        entryTitle.insert(0, item['values'][2])
        entryDescription.insert(0, item['values'][3])
        entryUpdateDate.insert(0, item['values'][4])
        entryUpdateDescription.insert(0, item['values'][5])

        var_ = item['values'][6]
        if var_.strip() == "Yes":
            var.set(True)
        else:
            var.set(False)

        updates = [f'{cont:02d} - {update[0]} - {update[1]}' for cont, update in enumerate(task_list[int(item['values'][0])-1].update_list, start=1)]
        updates.reverse()
        box['values'] = updates
        if len(updates) > 0:
            box.current(0)
    
tv.bind("<<TreeviewSelect>>", handle_selection)

def close_window():

    result = messagebox.askquestion("Exit Program", "Are You Sure?", icon='warning')
    if result == 'yes':
        #saving tasks
        with open((save_path), "wb") as f:
            pickle.dump(task_list, f, protocol=pickle.HIGHEST_PROTOCOL)

        root.destroy()
        sys.exit(0)
    else:
        pass

root.protocol("WM_DELETE_WINDOW", close_window)

root.mainloop()