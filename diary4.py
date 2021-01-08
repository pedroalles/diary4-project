from os import getlogin
from os.path import exists

import time
import datetime
import pickle

from tkinter import *
from tkinter import ttk
from tkinter import font
from tkinter import messagebox

from Task import Task

###################################################################################################

save_path = f"C:\\Users\\{getlogin()}\\Documents\\saves.pkl"
task_list = []


index_ = 0

###################################################################################################

intern_color = "gray4"
extern_color = "gray9"

###################################################################################################

root = Tk()
root.title('Diary 4')
root.configure(background=extern_color)

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

window_height = 768 
window_width = 1360

x_cordinate = int((screen_width/2) - (window_width/2))
y_cordinate = int((screen_height/2) - (window_height/2))

root.geometry("+0+0")
root.resizable(False, False)

###################################################################################################

def deselect(event):
    clear_inputs()
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

editing = "task"
deleting = "task"

def task_update(event=None):

    global updates
    up_task_title = entryTitle.get()
    up_task_decription = entryDescription.get()
    up_task_updecription = entryUpdateDescription.get()

    updates_len = len(updates)
    index_ = box.current()

    index_final = (index_+1 - updates_len) * -1

    selection = tv.selection()
    if selection:

        item = tv.item(selection)
        id_ = int(item["values"][0])

        task_list[id_ -1].task_title = up_task_title
        task_list[id_ -1].task_description = up_task_decription

        updates = (len(task_list[int(item['values'][0])-1].update_list))

        if updates > 0:
            task_list[id_ -1].update_list[index_final][1] = up_task_updecription

        add_tv_rows()
        child_id = tv.get_children()[id_ -1]
        tv.selection_set(child_id)

        root.focus()

root.bind('<Return>', task_update)

###################################################################################################

frame_inputs = Frame(root, bg=extern_color)
frame_inputs.grid(row=2, column=1, padx=(10), pady=(0,10))

frame_variable = StringVar()
lf = LabelFrame(frame_inputs, borderwidth= 3, text="  Task ID:  00  ", font=(None, 12, 'bold'), bg=extern_color, fg='white')
lf.grid(row=0, column=0, padx=0, pady=(0,0), ipadx=0, ipady=3)

labelStartDate = Label(lf, text="Start Date", font=(None, 11, 'bold'), bg=extern_color, fg='white', anchor="w")
labelStartDate.grid(row=0, column=1, sticky=EW, padx=15, pady=(5,0))

startDate_variable = StringVar()
entryStartDate = Entry(lf, borderwidth= 4, width= 13, justify='center', textvariable=startDate_variable, font=(None, 12), bg=intern_color, fg='white', insertbackground='white')
entryStartDate.grid(row=1, column=1, sticky=EW, padx=15, pady=0)
entryStartDate.config(disabledbackground=intern_color, disabledforeground='white')

labelTitle = Label(lf, text="Task Title", font=(None, 11, 'bold'), bg=extern_color, fg='white', anchor="w")
labelTitle.grid(row=0, column=2, sticky=EW, padx=0, pady=(5,0))

title_variable = StringVar()
entryTitle = Entry(lf, borderwidth= 4, width= 23, justify='left', textvariable=title_variable, font=(None, 12), bg=intern_color, fg='white', insertbackground='white')
entryTitle.grid(row=1, column=2, sticky=EW, padx=0, pady=0)
entryTitle.config(disabledbackground=intern_color, disabledforeground='white')

labelDescription = Label(lf, text="Task Description", font=(None, 11, 'bold'), bg=extern_color, fg='white', anchor="w")
labelDescription.grid(row=0, column=3, sticky=EW, padx=15, pady=(5,0))

description_variable = StringVar()
entryDescription = Entry(lf, borderwidth= 4, width= 31, justify='left', textvariable=description_variable, font=(None, 12), bg=intern_color, fg='white', insertbackground='white')
entryDescription.grid(row=1, column=3, sticky=EW, padx=15, pady=0)
entryDescription.config(disabledbackground=intern_color, disabledforeground='white')

labelUpdateDate = Label(lf, text="Last Update", font=(None, 11, 'bold'), bg=extern_color, fg='white', anchor="w")
labelUpdateDate.grid(row=0, column=4, sticky=EW, padx=0, pady=(5,0))

updateDate_variable = StringVar()
entryUpdateDate = Entry(lf, borderwidth= 4, width= 13, justify='center', textvariable=updateDate_variable, font=(None, 12), bg=intern_color, fg='white', insertbackground='white')
entryUpdateDate.grid(row=1, column=4, sticky=EW, padx=0, pady=0)
entryUpdateDate.config(disabledbackground=intern_color, disabledforeground='white')

labelUpdateDescription = Label(lf, text="Last Update Description", font=(None, 11, 'bold'), bg=extern_color, fg='white', anchor="w")
labelUpdateDescription.grid(row=0, column=5, sticky=EW, padx=(15, 15), pady=(5,0))

updateDescription_variable = StringVar()
entryUpdateDescription = Entry(lf, borderwidth= 4, width= 31, justify='left', textvariable=updateDescription_variable, font=(None, 12), bg=intern_color, fg='white', insertbackground='white')
entryUpdateDescription.grid(row=1, column=5, sticky=EW, padx=(15, 15), pady=0)
entryUpdateDescription.config(disabledbackground=intern_color, disabledforeground='white')

labelDone = Label(lf, text="Task Done", font=(None, 11, 'bold'), bg=extern_color, fg='white')
labelDone.grid(row=2, column=5, sticky=EW, padx=(10,0), pady=(10,0))

var = BooleanVar() 
var.set(False)
entryActive = Checkbutton(lf, variable=var, font=(None, 11), bg=extern_color, activebackground=extern_color, command=done_update)
entryActive.grid(row=3, column=5, sticky=EW, padx=(20,0), pady=(0,5))

labelListUpdates = Label(lf, text="Update List", font=(None, 11, 'bold'), bg=extern_color, fg='white', anchor="w")
labelListUpdates.grid(row=2, column=0, sticky=EW, columnspan=5, padx=(15,0), pady=(10,0))

box_value = StringVar()
box = ttk.Combobox(lf, width= 41, justify='left', textvariable=box_value, state='readonly', font=(None, 12))
box.grid(row=3, column=0, sticky=EW, columnspan=5, padx=(15,0), pady=(0,5), ipady=(0))

entryStartDate.config(state='disabled')
entryTitle.config(state='disabled')
entryDescription.config(state='disabled')
entryUpdateDate.config(state='disabled')
entryUpdateDescription.config(state='disabled')

def make_ordinal(n):

    n = int(n)
    suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    return str(n) + suffix

def select_update(event):

    global editing
    global deleting
    global index_
    global index_final
    global update_to_edit

    updates_len = len(updates)
    index_ = box.current()

    # print(index_)

    index_final = (index_+1 - updates_len) * -1

    # print(index_final)

    update_to_edit = task_list[int(item['values'][0])-1].update_list[index_final]

    # print(update_to_edit)
 
    updateDate_variable.set("")
    updateDescription_variable.set("")
    updateDate_variable.set(update_to_edit[0])
    updateDescription_variable.set(update_to_edit[1])

    if int(index_) != 0:
        labelUpdateDate.config(text=f'{make_ordinal(index_final+1)} Update')
        labelUpdateDescription.config(text=f'{make_ordinal(index_final+1)} Update Description')
    else:
        labelUpdateDate.config(text=f'Last Update')
        labelUpdateDescription.config(text=f'Last Update Description')

    deleting = "updates"

    # print('edit ' +editing)
    # print('del ' +deleting)

box.bind("<<ComboboxSelected>>", select_update)

###################################################################################################

frame_tree = Frame(root, bg=extern_color)
frame_tree.grid(row=1, column=0, pady=(10,0), padx=(10), columnspan=2)

tv_scroll = Scrollbar(frame_tree)
tv_scroll.pack(side=RIGHT, fill=Y, pady=(0))

def disableEvent(event):
    if tv.identify_region(event.x, event.y) == "separator":
        return "break"

tv = ttk.Treeview(frame_tree, yscrollcommand=tv_scroll.set, height=15)
tv.pack()

tv.bind("<Button-1>", disableEvent)

tv_scroll.config(command=tv.yview)

tv["column"] = ['ID','Start Date','Task Title','Task Description','Last Update','Last Update Description','Done']
tv["show"] = "headings"

tv.column("ID", minwidth=75, width=75, anchor='center')
tv.column("Start Date", minwidth=175, width=175, anchor='center')
tv.column("Task Title", minwidth=200, width=200, anchor='w')
tv.column("Task Description", minwidth=300, width=300, anchor='w')
tv.column("Last Update", minwidth=175, width=175, anchor='center')
tv.column("Last Update Description", minwidth=300, width=300, anchor='w')
tv.column("Done", minwidth=75, width=75, anchor='center')

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
    newWindow.title('New Task')
    newWindow.configure(background=extern_color)

    screen_width = newWindow.winfo_screenwidth()
    screen_height = newWindow.winfo_screenheight()

    window_height = 460
    window_width = 320

    x_cordinate = int((screen_width/2) - (window_width/2))
    y_cordinate = int((screen_height/2) - (window_height/2))

    newWindow.geometry("+{}+{}".format(x_cordinate, y_cordinate))
    newWindow.resizable(False, False)

    frame_add = Frame(newWindow, bg=extern_color)
    frame_add.grid(row=0, column=0)

    frame_add_var = StringVar()
    lfadd = LabelFrame(frame_add, text=f"  Task ID:  {id_}  ", font=(None, 11, 'bold'), bg=extern_color, fg='white')
    lfadd.grid(row=0, column=0, padx=10, pady=10, ipadx=5, ipady=0)

    labeladd = Label(lfadd, text="Task Title", font=(None, 11, 'bold'), bg=extern_color, fg='white', anchor='w')
    labeladd.grid(row=0, column=0, sticky=EW, padx=10, pady=(5,0))

    add_var_title = StringVar()
    entryadd = Entry(lfadd, width= 30, justify='left', textvariable=add_var_title, font=(None, 11), bg=intern_color, fg='white', insertbackground='white')
    entryadd.grid(row=1, column=0, sticky=EW, padx=10, pady=0)

    labeladddesc = Label(lfadd, text="Task Description", font=(None, 11, 'bold'), bg=extern_color, fg='white', anchor='w')
    labeladddesc.grid(row=2, column=0, sticky=EW, padx=10, pady=(5,0))

    add_var_desc = StringVar()
    entryadddesc = Entry(lfadd, width= 30, justify='left', textvariable=add_var_desc, font=(None, 11), bg=intern_color, fg='white', insertbackground='white')
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

    def enter_add_task(event):
        add_task_commit()

    buttonaddup = Button(lfadd, text='Add Task', command=add_task_commit, bg='SteelBlue2', activebackground=intern_color, activeforeground='white', font=(None, 12, 'bold'))
    buttonaddup.grid(row=4, column=0, padx=10, pady=(10,8), ipadx=5)

    newWindow.bind('<Return>', enter_add_task)

def delete_task():

    selection = tv.selection()
    if selection:

        item = tv.item(selection)

        id_ = int(item["values"][0])
        result = messagebox.askquestion("Delete Task", "Are You Sure?", icon='warning')
        if result == 'yes':
            
            task_list.pop(id_ -1)

            for cont, task in enumerate(task_list, start=1):
                task.task_id = cont 

            add_tv_rows()
            clear_inputs()

        else:
            pass

def delete_update():

    
    selection = tv.selection()
    if selection:

        item = tv.item(selection)

        id_ = int(item["values"][0]) - 1

        result = messagebox.askquestion("Delete Update", "Are You Sure?", icon='warning')
        if result == 'yes':
            
            task_list[id_].update_list.pop(index_final)

            for cont, task in enumerate(task_list, start=1):
                task.task_id = cont 

            add_tv_rows()
            clear_inputs()
            child_id = tv.get_children()[id_]
            tv.selection_set(child_id)

        else:
            pass


def call_delete(event):
    if deleting == "task":
        delete_task()
    if deleting == "updates":
        delete_update()

def call_delete_bt():
    if deleting == "task":
        delete_task()
    if deleting == "updates":
        delete_update()

root.bind('<Delete>', call_delete)

def clear_inputs():

    entryStartDate.config(state='normal')
    entryTitle.config(state='normal')
    entryDescription.config(state='normal')
    entryUpdateDate.config(state='normal')
    entryUpdateDescription.config(state='normal')

    entryStartDate.delete(0, "end")
    entryTitle.delete(0, "end")
    entryDescription.delete(0, "end")
    entryUpdateDate.delete(0, "end")
    entryUpdateDescription.delete(0, "end")
    var.set(False)
    box.set('')
    box['values'] = ""

    entryStartDate.config(state='disabled')
    entryTitle.config(state='disabled')
    entryDescription.config(state='disabled')
    entryUpdateDate.config(state='disabled')
    entryUpdateDescription.config(state='disabled')

def add_update():

    selection = tv.selection()
    if selection:

        item = tv.item(selection)
        id_ = int(item["values"][0])

        newWindow = Toplevel(root) 
        newWindow.title('Add Update')
        newWindow.configure(background=extern_color)

        screen_width = newWindow.winfo_screenwidth()
        screen_height = newWindow.winfo_screenheight()

        window_height = 450
        window_width = 200

        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))

        newWindow.geometry("+{}+{}".format(x_cordinate, y_cordinate))
        newWindow.resizable(False, False)

        frame_up = Frame(newWindow, bg=extern_color)
        frame_up.grid(row=0, column=0)

        frame_up_var = StringVar()
        lfup = LabelFrame(frame_up, text=f"  Task ID:  {id_}  ", font=(None, 11, 'bold'), bg=extern_color, fg='white')
        lfup.grid(row=0, column=0, padx=10, pady=10, ipadx=5, ipady=0)

        labelupdesc = Label(lfup, text="Update Description", font=(None, 11, 'bold'), bg=extern_color, fg='white', anchor='w')
        labelupdesc.grid(row=0, column=0, sticky=EW, padx=10, pady=5)

        update_var = StringVar()
        entryupdesc = Entry(lfup, width= 30, justify='left', textvariable=update_var, font=(None, 11), bg=intern_color, fg='white', insertbackground='white')
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

        def enter_update(event):
            add_update_commit()

        buttonaddup = Button(lfup, text='Add Update', command=add_update_commit, bg='Lime Green', activebackground=intern_color, activeforeground='white', font=(None, 12, 'bold'))
        buttonaddup.grid(row=2, column=0, padx=10, pady=(10,8), ipadx=5)

        newWindow.bind('<Return>', enter_update)

###################################################################################################

frame_buttons = Frame(root, bg=extern_color)
frame_buttons.grid(row=2, column=0, pady=(10,10), padx=(10,0))

buttonAddTask = Button(frame_buttons, borderwidth=4, font=(None, 12, 'bold'), width=15, text='New Task', command=add_task, bg='SteelBlue2', activebackground=intern_color, activeforeground='white')
buttonAddTask.grid(row=0, column=0, padx=(0,0), pady=(0,10), ipady=(3))

buttonAddUpdate = Button(frame_buttons, borderwidth=4, font=(None, 12, 'bold'), width=15, text='Add Update', command=add_update, bg='Lime Green', activebackground=intern_color, activeforeground='white')
buttonAddUpdate.grid(row=1, column=0, padx=(0,0), pady=(0,10), ipady=(3))

buttonDeleteTask = Button(frame_buttons, borderwidth=4, font=(None, 12, 'bold'), width=15, text='Delete', command=call_delete_bt, bg='Tomato2', activebackground=intern_color, activeforeground='white')
buttonDeleteTask.grid(row=2, column=0, pady=(0,0), ipady=(3))

###################################################################################################

style = ttk.Style()
style.theme_use("default")

style.configure("Treeview.Heading", font=(None, 13, 'bold'), borderwidth=4, background='SteelBlue2', foreground="black", fieldbackground=intern_color)
style.configure("Treeview", font=(None, 12), borderwidth=4, background=intern_color, foreground="white", fieldbackground=intern_color)

style.map("Treeview.Heading", foreground=[('pressed', 'white')], background=[('pressed', intern_color)])
style.map("Treeview", foreground=[('selected', 'black')],  background=[('selected', 'SteelBlue2')])

style.map('TCombobox', fieldbackground=[('readonly',intern_color)])
style.map('TCombobox', background=[('readonly', 'SteelBlue2')])
style.map('TCombobox', foreground=[('readonly', 'white')])
style.map('TCombobox', borderwidth = [('readonly', 4)])
style.map('TCombobox', selectbackground=[('readonly', intern_color)])
style.map('TCombobox', selectforeground=[('readonly', 'white')])
style.map('TCombobox', selectborderwidth = [('readonly', 0)])

bigfont = font.Font(family="Helvetica",size=12)
root.option_add("*TCombobox*Listbox*Font", bigfont)
root.option_add('*TCombobox*Listbox.Background', intern_color) 
root.option_add('*TCombobox*Listbox.Foreground', 'white') 
root.option_add('*TCombobox*Listbox.selectBackground', 'SteelBlue2') 
# root.option_add('*TCombobox*Listbox.Justify', 'center')

style.configure( 'Vertical.TScrollbar', background='SteelBlue2' )

###################################################################################################

if exists((save_path)):
    with open((save_path), 'rb') as f:
        task_list = pickle.load(f)

def add_tv_rows():

    for i in tv.get_children():
        tv.delete(i)

    
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

def detect_entry_click(event):
    global editing
    global index_
    
    # if index_:
    #     index_ = 0
    # # index_ = box.current()
    editing = "updates"
     
entryTitle.bind("<Button-1>", detect_entry_click)
entryDescription.bind("<Button-1>", detect_entry_click)
entryUpdateDescription.bind("<Button-1>", detect_entry_click)

def handle_selection(event):

    clear_inputs()

    entryStartDate.config(state='normal')
    entryTitle.config(state='normal')
    entryDescription.config(state='normal')
    entryUpdateDate.config(state='normal')
    entryUpdateDescription.config(state='normal')

    global item
    global updates
    global editing
    global deleting
    # global index_ 

    # if index_ < 0:
    #     index_ = 0

    labelUpdateDate.config(text=f'Last Update')
    labelUpdateDescription.config(text=f'Last Update Description')


    selection = tv.selection()
    if selection:

        item = tv.item(selection)

        lf.configure(text=f'  Task ID:  {item["values"][0]:02d}  ')
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

        updates = [f'          {cont:02d}                                        {update[0]}                                        {update[1]}' for cont, update in enumerate(task_list[int(item['values'][0])-1].update_list, start=1)]
        # updates = ['{:>10}{:^60}{:40}'.format(str(f'{cont:02d}'), str(update[0]), str(update[1]) ) for cont, update in enumerate(task_list[int(item['values'][0])-1].update_list, start=1)]
        
        updates.reverse()

        box['values'] = updates

        if len(updates) > 0 and editing == "task":
            box.current(0)

        if len(updates) > 0 and editing == "updates":
            try:
                box.current(index_)
                if int(index_) != 0:
                    labelUpdateDate.config(text=f'{make_ordinal(index_final+1)} Update')
                    labelUpdateDescription.config(text=f'{make_ordinal(index_final+1)} Update Description')
                
                    updateDate_variable.set("")
                    updateDescription_variable.set("")
                    updateDate_variable.set(update_to_edit[0])
                    updateDescription_variable.set(update_to_edit[1])
                else:
                    labelUpdateDate.config(text=f'Last Update')
                    labelUpdateDescription.config(text=f'Last Update Description')
            except:
                labelUpdateDate.config(text=f'Last Update')
                labelUpdateDescription.config(text=f'Last Update Description')
                box.current(0)

        editing = "task"
        deleting = "task"

        entryStartDate.config(state='disabled')
        entryUpdateDate.config(state='disabled')

        # print('edit ' +editing)
        # print('del ' +deleting)

tv.bind("<<TreeviewSelect>>", handle_selection)



def close_window():

    result = messagebox.askquestion("Exit Program", "Are You Sure?", icon='warning')
    if result == 'yes':
        #saving tasks
        with open((save_path), "wb") as f:
            pickle.dump(task_list, f, protocol=pickle.HIGHEST_PROTOCOL)

        root.destroy()
        # sys.exit(0)
    else:
        pass

root.protocol("WM_DELETE_WINDOW", close_window)

root.mainloop()