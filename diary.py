import os
from Task2 import Task
import time
import datetime
import pickle
from tkinter import *
from tkinter import ttk
from tkinter import font
from tkinter import messagebox


class Window(Tk):

    def __init__(self):
        super(Window, self).__init__()

        self.intern_color = "gray4"
        self.extern_color = "gray9"
        self.font_color = 'white'
        self.font_labels = (None, 12, 'bold')
        self.font_entrys = (None, 12)

        self.action = "default"
        self.deleting = "task"

        self.user = os.getlogin()
        self.save_path = f"C:\\Users\\{self.user}\\Documents\\Diary\\sv.pkl"
        self.save_directory = f"C:\\Users\\{self.user}\\Documents\\Diary"
        self.task_list= []

        self.title('Diary4')
        self.configure(bg=self.extern_color)
        self.geometry("+0+0")
        self.wm_iconbitmap('icon512.ico')
        # self.state('zoomed')
        
        self.open_database()
        self.create_style()
        self.create_layout()
        self.create_tv()
        self.create_buttons()
        self.create_lb()
        self.create_labels()
        self.create_entrys()
        self.create_checkbox()
        self.create_combobox()
        self.create_tv_rows()
    
        self.tv.bind("<<TreeviewSelect>>", self.select_tv_item)

        self.box.bind("<<ComboboxSelected>>", self.select_box_item)

        self.bind('<Escape>', self.deselect)

        self.bind('<Delete>', self.call_delete)

        self.protocol("WM_DELETE_WINDOW", self.close_window)

    def deselect(self,event):
        self.clear_inputs()
        self.current_selection_tv_id = 0
        selection = self.tv.selection()
        if selection:
            self.tv.selection_remove(self.tv.selection())

    def open_database(self):
        if os.path.exists(self.save_directory):
            if os.path.exists(self.save_path):
                with open(self.save_path, 'rb') as f:
                    self.task_list = pickle.load(f)
        else:
            os.mkdir(self.save_directory)

    def save_database(self):
        with open(self.save_path, "wb") as f:
            pickle.dump(self.task_list, f, protocol=pickle.HIGHEST_PROTOCOL)

    def close_window(self):
        result = messagebox.askquestion("Exit Program", "Are You Sure?", icon='warning')
        if result == 'yes':

            self.save_database()

            self.destroy()
        else:
            pass

    def create_style(self):
        self.style = ttk.Style()
        self.style.theme_use("default")
        self.style.configure("Treeview.Heading", font=self.font_labels, borderwidth=4, background='SteelBlue2', foreground="black", fieldbackground=self.intern_color)
        self.style.configure("Treeview", font=self.font_entrys, borderwidth=4, background=self.intern_color, foreground=self.font_color, fieldbackground=self.intern_color)
        self.style.map("Treeview.Heading", foreground=[('pressed', 'white')], background=[('pressed', self.intern_color)])
        self.style.map("Treeview", foreground=[('selected', 'black')],  background=[('selected', 'SteelBlue2')])

        self.style.map('TCombobox', fieldbackground=[('readonly',self.intern_color)])
        self.style.map('TCombobox', background=[('readonly', 'SteelBlue2')])
        self.style.map('TCombobox', foreground=[('readonly', self.font_color)])
        self.style.map('TCombobox', borderwidth = [('readonly', 4)])
        self.style.map('TCombobox', selectbackground=[('readonly', self.intern_color)])
        self.style.map('TCombobox', selectforeground=[('readonly', self.font_color)])
        self.style.map('TCombobox', selectborderwidth = [('readonly', 0)])

        bigfont = font.Font(family="Helvetica",size=12)
        self.option_add("*TCombobox*Listbox*Font", bigfont)
        self.option_add('*TCombobox*Listbox.Background', self.intern_color) 
        self.option_add('*TCombobox*Listbox.Foreground', self.font_color) 
        self.option_add('*TCombobox*Listbox.selectBackground', 'SteelBlue2') 
        # self.option_add('*TCombobox*Listbox.Justify', 'center')

        # style.configure( 'Vertical.TScrollbar', background='SteelBlue2' )

    def create_layout(self):
        self.tv_frame = Frame(self,
                        bg=self.extern_color)
        self.tv_frame.grid(row=0, column=0, pady=(10,0), padx=(10), columnspan=2)

        self.bt_frame = Frame(self,
                        bg=self.extern_color)
        self.bt_frame.grid(row=1, column=0, padx=(10), pady=(5,10))

        self.entry_frame = Frame(self,
                        bg=self.extern_color)
        self.entry_frame.grid(row=1, column=1, padx=(10), pady=(5,10))

    def create_tv(self):

        self.current_selection_tv_id = 0
        self.new_selection_tv_id = 0

        self.tv = ttk.Treeview(self.tv_frame)
        self.tv.pack(expand=1, fill="both")

        self.tv["column"] = ['ID','Start Date','Task Title','Task Description','Last Update','Last Update Description','Done']
        self.tv["show"] = "headings"

        self.tv.column("ID", minwidth=75, width=75, anchor='center')
        self.tv.column("Start Date", minwidth=175, width=175, anchor='center')
        self.tv.column("Task Title", minwidth=200, width=200, anchor='w')
        self.tv.column("Task Description", minwidth=300, width=300, anchor='w')
        self.tv.column("Last Update", minwidth=175, width=175, anchor='center')
        self.tv.column("Last Update Description", minwidth=300, width=300, anchor='w')
        self.tv.column("Done", minwidth=75, width=75, anchor='center')

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

        for column in self.tv["column"]:
            self.tv.heading(column, text=column, command=lambda _col=column: treeview_sort_column(self.tv, _col, False))
    
    def create_tv_rows(self):

        self.rows = []

        for i in self.tv.get_children():
            self.tv.delete(i)

        for cont, task in enumerate(self.task_list):

            task_id_ = f'{int(self.task_list[cont].task_id):02d}'

            try:
                last_update_date =  self.task_list[cont].update_list[-1][0]
                last_update_description =  self.task_list[cont].update_list[-1][1]
            except:
                last_update_date = ''
                last_update_description = ''

            done_status_print = ''
            done_status = str(self.task_list[cont].task_done_status)
            if done_status == "False":
                done_status_print = 'No'
            else:
                done_status_print = 'Yes'

            self.rows.append([  task_id_,
                                self.task_list[cont].task_start_date,
                                self.task_list[cont].task_title,
                                self.task_list[cont].task_description,
                                last_update_date,
                                last_update_description,
                                done_status_print
                                ])
 
        for row in self.rows:
            self.tv.insert("", "end", values=row)

    def create_buttons(self):
        # self.frame_buttons = Frame(root, bg=self.extern_color)
        # self.frame_buttons.grid(row=2, column=0, pady=(10,10), padx=(10,0))

        bt_borderwidth = 4
        bt_width = 17

        self.bt_add_task = Button(self.bt_frame,
            text='New Task',
            borderwidth=bt_borderwidth,
            width=bt_width,
            font=self.font_labels,
            bg='SteelBlue2',
            command=self.new_win_add_task,
            activebackground=self.intern_color,
            activeforeground='white')
        self.bt_add_task.grid(row=0, column=0, padx=(0,0), pady=(10,10), ipady=(3))

        self.bt_add_update = Button(self.bt_frame,
            borderwidth=bt_borderwidth,
            font=self.font_labels,
            width=bt_width,
            text='Add Update',
            command=self.new_win_update_tak,
            bg='Lime Green',
            activebackground=self.intern_color,
            activeforeground='white')
        self.bt_add_update.grid(row=1, column=0, padx=(0,0), pady=(0,10), ipady=(3))

        self.bt_del_task = Button(self.bt_frame,
            borderwidth=bt_borderwidth,
            font=self.font_labels,
            width=bt_width,
            text='Delete',
            command=self.call_delete_bt,
            bg='Tomato2',
            activebackground=self.intern_color,
            activeforeground='white')
        self.bt_del_task.grid(row=2, column=0, pady=(0,0), ipady=(3))

    def create_lb(self):

        self.frame_var = StringVar()
        self.lf = LabelFrame(self.entry_frame,
            borderwidth= 3,
            text="  Task ID:  00  ",
            font=self.font_labels,
            bg=self.extern_color,
            fg=self.font_color)
        self.lf.pack()

    def create_labels(self):

        self.label_task_date = Label(self.lf, text="Start Date", font=self.font_labels, bg=self.extern_color, fg=self.font_color, anchor="w")
        self.label_task_date.grid(row=0, column=0, sticky=EW, padx=10, pady=(5,0))

        self.label_title = Label(self.lf, text="Task Title", font=self.font_labels, bg=self.extern_color, fg=self.font_color, anchor="w")
        self.label_title.grid(row=0, column=1, sticky=EW, padx=0, pady=(5,0))

        self.label_title = Label(self.lf, text="Task Description", font=self.font_labels, bg=self.extern_color, fg=self.font_color, anchor="w")
        self.label_title.grid(row=0, column=2, sticky=EW, padx=10, pady=(5,0))

        self.label_update = Label(self.lf, text="Last Update", font=self.font_labels, bg=self.extern_color, fg=self.font_color, anchor="w")
        self.label_update.grid(row=0, column=3, sticky=EW, padx=0, pady=(5,0))

        self.label_update_description = Label(self.lf, text="Last Update Description", font=self.font_labels, bg=self.extern_color, fg=self.font_color, anchor="w")
        self.label_update_description.grid(row=0, column=4, sticky=EW, padx=10, pady=(5,0))

    def create_entrys(self):

        entrys_borderwidth = 4
        entrys_insertbackgroud = 'white'

        task_date_var = StringVar()
        self.entry_task_date = Entry(self.lf,
            borderwidth= entrys_borderwidth,
            width= 13,
            justify='center',
            textvariable=task_date_var,
            font=self.font_entrys,
            bg=self.intern_color,
            fg=self.font_color,
            insertbackground=entrys_insertbackgroud)
        self.entry_task_date.grid(row=1, column=0, sticky=EW, padx=10, pady=(0,10))
        self.entry_task_date.config(disabledbackground=self.intern_color, disabledforeground='white')

        title_var = StringVar()
        self.entry_title = Entry(self.lf,
            borderwidth= entrys_borderwidth,
            width= 23,
            justify='left',
            textvariable=title_var,
            font=self.font_entrys,
            bg=self.intern_color,
            fg=self.font_color,
            insertbackground=entrys_insertbackgroud)
        self.entry_title.grid(row=1, column=1, sticky=EW, padx=0, pady=(0,10))
        self.entry_title.config(disabledbackground=self.intern_color, disabledforeground='white')

        description_var = StringVar()
        self.entry_description = Entry(self.lf,
            borderwidth= entrys_borderwidth,
            width= 23,
            justify='left',
            textvariable=description_var,
            font=self.font_entrys,
            bg=self.intern_color,
            fg=self.font_color,
            insertbackground='white')
        self.entry_description.grid(row=1, column=2, sticky=EW, padx=10, pady=(0,10))
        self.entry_description.config(disabledbackground=self.intern_color, disabledforeground='white')

        self.update_var = StringVar()
        self.entry_update = Entry(self.lf,
            borderwidth= entrys_borderwidth,
            width= 13, justify='center',
            textvariable=self.update_var,
            font=self.font_entrys,
            bg=self.intern_color,
            fg=self.font_color,
            insertbackground='white')
        self.entry_update.grid(row=1, column=3, sticky=EW, padx=0, pady=(0,10))
        self.entry_update.config(disabledbackground=self.intern_color, disabledforeground='white')

        self.update_description_var = StringVar()
        self.entry_update_description = Entry(self.lf,
            borderwidth= entrys_borderwidth,
            width= 31,
            justify='left',
            textvariable=self.update_description_var,
            font=self.font_entrys,
            bg=self.intern_color,
            fg=self.font_color,
            insertbackground='white')
        self.entry_update_description.grid(row=1, column=4, sticky=EW, padx=10, pady=(0,10))
        self.entry_update_description.config(disabledbackground=self.intern_color, disabledforeground='white')

        self.entry_task_date.config(state='disabled')
        self.entry_title.config(state='disabled')
        self.entry_description.config(state='disabled')
        self.entry_update.config(state='disabled')
        self.entry_update_description.config(state='disabled')

    def create_combobox(self):

        self.label_update_list = Label(self.lf, text="Update List", font=self.font_labels, bg=self.extern_color, fg=self.font_color, anchor="w")
        self.label_update_list.grid(row=2, column=2, sticky=EW, columnspan=4, padx=(10,0), pady=(0,0))

        box_var = StringVar()
        self.box = ttk.Combobox(self.lf,
            width= 41,
            justify='left',
            textvariable=box_var,
            state='readonly',
            font=self.font_entrys)
        self.box.grid(row=3, column=2, sticky=EW, columnspan=4, padx=(10,10), pady=(0,10), ipady=(0))

    def create_checkbox(self):

        self.label_check_task = Label(self.lf, text="Task Done", font=self.font_labels, bg=self.extern_color, fg=self.font_color, anchor='w')
        self.label_check_task.grid(row=2, column=0, padx=(0,0), pady=(10,0))

        self.var_check_task = BooleanVar() 
        self.var_check_task.set(False)
        self.check_task = Checkbutton(self.lf, variable=self.var_check_task, font=self.font_labels, bg=self.extern_color, activebackground=self.extern_color, command=...)
        self.check_task.grid(row=3, column=0, padx=(0,0), pady=(0,5))

        self.label_check_update = Label(self.lf, text="Update Done", font=self.font_labels, bg=self.extern_color, fg=self.font_color)
        self.label_check_update.grid(row=2, column=1, padx=(0,0), pady=(10,0))

        self.var_check_update = BooleanVar() 
        self.var_check_update.set(False)
        self.check_update = Checkbutton(self.lf, variable=self.var_check_update, font=self.font_labels, bg=self.extern_color, activebackground=self.extern_color, command=self.check_update_click)
        self.check_update.grid(row=3, column=1, padx=(0,0), pady=(0,5))

    def select_tv_item(self, event):

        self.deleting = "task"
        print(self.action)

        selection = self.tv.selection()
        if selection:

            self.item = self.tv.item(selection)
            self.new_selection_tv_id = int(self.item['values'][0]) 
            
            if self.current_selection_tv_id == self.new_selection_tv_id:
                
                self.populate_combobox(self.new_selection_tv_id)
                if self.action == "new_update" or self.action == "del_update":
                    self.populate_entrys(self.new_selection_tv_id)
                    self.populate_combobox(self.new_selection_tv_id)
                    print("1")
                    if len(self.updates_list) > 0:
                        print()
                        self.box.current(0)


                    print("mudando label desc")
                    self.label_update.config(text=f'Last Update')
                    self.label_update_description.config(text=f'Last Update Description')

                if self.action == "click_update_check":
                    print(self.current_selection_box_id)
                    self.box.current(self.current_selection_box_id)

                    if len(self.updates_list) > 0:
                        print("oi")
                        self.label_update.config(text=f'{self.make_ordinal(self.var_updates + 1)} Update')
                        self.label_update_description.config(text=f'{self.make_ordinal(self.var_updates + 1)} Update Description')
                    else:
                        print("mudando nome label desc")
                        self.label_update.config(text=f'Last Update')
                        self.label_update_description.config(text=f'Last Update Description')

                print("mesmo")
                
            else:
                self.populate_entrys(self.new_selection_tv_id)
                self.populate_combobox(self.new_selection_tv_id)

                print( len(self.updates_list))

                if len(self.updates_list) > 0:
                    self.box.current(0)

                    print(self.updates_list[-1][2])

                    if self.updates_list[-1][2] == 0:
                        # update_status = 'TO DO'
                        print("colocando false")
                        self.var_check_update.set(False)
                    else:
                        # update_status = 'DONE '
                        print("colocando true")
                        self.var_check_update.set(True)
                    
                print("mudando nome dif")
                self.label_update.config(text=f'Last Update')
                self.label_update_description.config(text=f'Last Update Description')
                print("diferente")

            self.current_selection_tv_id = self.new_selection_tv_id

            self.action = "default"

    def clear_inputs(self):

        self.entry_task_date.config(state='normal')
        self.entry_title.config(state='normal')
        self.entry_description.config(state='normal')
        self.entry_update.config(state='normal')
        self.entry_update_description.config(state='normal')

        self.lf.config(text='  Task ID:  00  ')
        self.entry_task_date.delete(0, "end")
        self.entry_title.delete(0, "end")
        self.entry_description.delete(0, "end")
        self.entry_update.delete(0, "end")
        self.entry_update_description.delete(0, "end")
        # var.set(False)
        self.box.set('')
        self.box['values'] = ""

        self.label_update.config(text=f'Last Update')
        self.label_update_description.config(text=f'Last Update Description')

        self.entry_task_date.config(state='disabled')
        self.entry_title.config(state='disabled')
        self.entry_description.config(state='disabled')
        self.entry_update.config(state='disabled')
        self.entry_update_description.config(state='disabled')

    def populate_entrys(self, id_selection):

        self.clear_inputs()

        self.entry_task_date.config(state='normal')
        self.entry_title.config(state='normal')
        self.entry_description.config(state='normal')
        self.entry_update.config(state='normal')
        self.entry_update_description.config(state='normal')


        self.lf.configure(text=f'  Task ID:  {id_selection:02d}  ')
        self.entry_task_date.insert(0, self.item['values'][1])
        self.entry_title.insert(0, self.item['values'][2])
        self.entry_description.insert(0, self.item['values'][3])

        self.entry_update.insert(0, self.item['values'][4])
        self.entry_update_description.insert(0, self.item['values'][5])

        self.entry_task_date.config(state='disabled')
        self.entry_update.config(state='disabled')

    def populate_combobox(self, id_selection):

        self.updates_list_box = []
        self.updates_list = []
        for cont, update in enumerate(self.task_list[id_selection -1].update_list, start=1):

            self.update_check = update[2]
            
            if self.update_check == 0:
                update_status = 'TO DO'
                # var_update.set(False)
            else:
                update_status = 'DONE '
                # var_update.set(True)

            line = f'{update_status:^20}{f"{cont:02d}":^40}{update[0]:<35}{update[1]:<35}'

            self.updates_list_box.append(line)
            self.updates_list.append(update)

        self.updates_list_box_reversed = self.updates_list_box.copy()
        self.updates_list_reversed = self.updates_list.copy()

        self.updates_list_box_reversed.reverse()
        self.updates_list_reversed.reverse()

        self.box['values'] = self.updates_list_box_reversed

    def new_win_add_task(self):

        selection = self.tv.selection()
        if selection:
            
            self.tv.selection_remove(self.tv.selection())

        self.tv.yview_moveto(0)
        
        self.new_task_id = len(self.rows) + 1
 
        try:
            self.newWindow.destroy()
        except:
            pass

        self.newWindow = Toplevel(self) 
        self.newWindow.title('New Task')
        self.newWindow.configure(background=self.extern_color)
        screen_width = self.newWindow.winfo_screenwidth()
        screen_height = self.newWindow.winfo_screenheight()
        window_height = 460
        window_width = 300
        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))
        self.newWindow.geometry("+{}+{}".format(x_cordinate, y_cordinate))
        self.newWindow.resizable(False, False)

        self.frame_add_task = Frame(self.newWindow, bg=self.extern_color)
        self.frame_add_task.grid(row=0, column=0)

        self.add_frame_var = StringVar()
        self.lf_add_task = LabelFrame(self.frame_add_task,
            text=f"  Task ID:  {self.new_task_id:02d}  ",
            font=self.font_labels,
            bg=self.extern_color,
            fg=self.font_color)
        self.lf_add_task.grid(row=0, column=0, padx=10, pady=10, ipadx=0, ipady=0)

        self.label_add_task_title = Label(self.lf_add_task,
            text="Task Title",
            font=self.font_labels,
            bg=self.extern_color,
            fg=self.font_color,
            anchor='w')
        self.label_add_task_title.grid(row=0, column=0, sticky=EW, padx=10, pady=(5,0))

        self.add_title_var = StringVar()
        self.entry_add_task_title = Entry(self.lf_add_task,
            width= 30, justify='left',
            textvariable=self.add_title_var,
            font=self.font_entrys,
            bg=self.intern_color,
            fg=self.font_color,
            insertbackground='white')
        self.entry_add_task_title.grid(row=1, column=0, sticky=EW, padx=10, pady=0)

        self.label_add_task_desc = Label(self.lf_add_task,
            text="Task Description",
            font=self.font_labels,
            bg=self.extern_color,
            fg=self.font_color,
            anchor='w')
        self.label_add_task_desc.grid(row=2, column=0, sticky=EW, padx=10, pady=(5,0))

        self.add_desc_var = StringVar()
        self.entry_add_task_desc = Entry(self.lf_add_task,
            width= 30,
            justify='left',
            textvariable=self.add_desc_var,
            font=self.font_entrys,
            bg=self.intern_color,
            fg=self.font_color,
            insertbackground='white')
        self.entry_add_task_desc.grid(row=3, column=0, sticky=EW, padx=10, pady=0)

        self.entry_add_task_title.focus()

        self.bt_new_task = Button(self.lf_add_task, text='Add Task', command=self.add_task_commit, bg='SteelBlue2', activebackground=self.intern_color, activeforeground='white', font=(None, 12, 'bold'))
        self.bt_new_task.grid(row=4, column=0, padx=10, pady=(10,8), ipadx=5)

        self.newWindow.bind('<Return>', self.enter_add_task)

    def add_task_commit(self):

        self.new_task_title = self.entry_add_task_title.get()
        self.new_task_decription = self.entry_add_task_desc.get()
        self.start_date = str(datetime.datetime.fromtimestamp(int(time.time())).strftime('%d/%m/%y  %H:%M'))
        self.task_list.append(Task(self.new_task_id, self.new_task_title, self.new_task_decription, self.start_date))

        self.create_tv_rows()

        child_id = self.tv.get_children()[len(self.task_list)-1]
        self.tv.yview_moveto(self.new_task_id) 
        self.tv.selection_set(child_id)
        self.newWindow.destroy()

    def enter_add_task(self, event):
        self.add_task_commit()

    def new_win_update_tak(self):

        try:
            self.newWindow.destroy()
        except:
            pass

        if self.current_selection_tv_id == 0:
            return
 
        self.newWindow = Toplevel(self) 
        self.newWindow.title('Add Update')
        self.newWindow.configure(background=self.extern_color)
        screen_width = self.newWindow.winfo_screenwidth()
        screen_height = self.newWindow.winfo_screenheight()
        window_height = 460
        window_width = 300
        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))
        self.newWindow.geometry("+{}+{}".format(x_cordinate, y_cordinate))
        self.newWindow.resizable(False, False)

        self.frame_update_task = Frame(self.newWindow, bg=self.extern_color)
        self.frame_update_task.grid(row=0, column=0)

        self.update_frame_var = StringVar()
        self.lf_update_task = LabelFrame(self.frame_update_task,
            text=f"  Task ID:  {self.current_selection_tv_id}  ",
            font=self.font_labels,
            bg=self.extern_color,
            fg='white')
        self.lf_update_task.grid(row=0, column=0, padx=10, pady=10, ipadx=0, ipady=0)

        self.label_update_desc = Label(self.lf_update_task,
            text="Update Description",
            font=self.font_labels,
            bg=self.extern_color,
            fg='white', anchor='w')
        self.label_update_desc.grid(row=0, column=0, sticky=EW, padx=10, pady=5)

        self.update_entry_var = StringVar()
        self.entry_update_desc = Entry(self.lf_update_task,
            width= 30,
            justify='left',
            textvariable= self.update_entry_var,
            font=self.font_entrys,
            bg=self.intern_color,
         
            fg='white',
            insertbackground='white')
        self.entry_update_desc.grid(row=1, column=0, sticky=EW, padx=10, pady=(0,0))
        self.entry_update_desc.focus()
    
        self.bt_new_update_task = Button(self.lf_update_task, text='Add Update', command=self.add_update_commit, bg='Lime Green', activebackground=self.intern_color, activeforeground='white', font=self.font_labels)
        self.bt_new_update_task.grid(row=2, column=0, padx=10, pady=(10,8), ipadx=5)

        self.newWindow.bind('<Return>', self.enter_update)

    def add_update_commit(self):

        self.new_update_desc = self.entry_update_desc.get()
        self.update_date = str(datetime.datetime.fromtimestamp(int(time.time())).strftime('%d/%m/%y  %H:%M'))
        self.task_list[self.current_selection_tv_id-1].add_update_task(self.update_date, self.new_update_desc, False)

        self.create_tv_rows()
        
        child_id = self.tv.get_children()[self.current_selection_tv_id-1]
        self.tv.selection_set(child_id)
        self.tv.yview_moveto(self.current_selection_tv_id)  
        self.newWindow.destroy()
        
        self.action = "new_update"

    def enter_update(self,event):
        self.add_update_commit()

    def make_ordinal(self, n):

        n = int(n)
        suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
        if 11 <= (n % 100) <= 13:
            suffix = 'th'
        return str(n) + suffix

    def select_box_item(self, event):

        print("box selected")

        self.deleting = "update"

        updates_len = len(self.updates_list)

        self.current_selection_box_id = self.box.current()

        self.update_var.set("")
        self.update_description_var.set("")

        self.update_var.set(self.updates_list_reversed[self.current_selection_box_id][0])
        self.update_description_var.set(self.updates_list_reversed[self.current_selection_box_id][1])

        # self.var_updates = self.updates_list.index(self.updates_list_reversed[self.current_selection_box_id])
        self.var_updates = (self.current_selection_box_id + 1 - updates_len) * -1


        self.update_check = self.updates_list_reversed[self.current_selection_box_id][2]
        
        if self.update_check == 0:
            # update_status = 'TO DO'
            self.var_check_update.set(False)
        else:
            # update_status = 'DONE '
            self.var_check_update.set(True)

        # print(self.var_updates)

        if len(self.updates_list) > 0:
            self.label_update.config(text=f'{self.make_ordinal(self.var_updates + 1)} Update')
            self.label_update_description.config(text=f'{self.make_ordinal(self.var_updates + 1)} Update Description')
        else:
            print("mudando nome label desc")
            self.label_update.config(text=f'Last Update')
            self.label_update_description.config(text=f'Last Update Description')

        # self.current_selection_box_id = None

    def delete_task(self):

        selection = self.tv.selection()
        if selection:

            result = messagebox.askquestion("Delete Task", "Are You Sure?", icon='warning')
            if result == 'yes':
                
                self.task_list.pop(self.current_selection_tv_id -1)

                for cont, task in enumerate(self.task_list, start=1):
                    task.task_id = cont

                self.create_tv_rows()
                self.clear_inputs()

                self.current_selection_tv_id = 0

        else:
            pass

    def delete_update(self):

        self.action = "del_update"

        selection = self.tv.selection()
        if selection:

            result = messagebox.askquestion("Delete Update", "Are You Sure?", icon='warning')
            if result == 'yes':

                self.task_list[self.current_selection_tv_id -1].update_list.pop(self.var_updates)

                self.create_tv_rows()
                self.clear_inputs()

                child_id = self.tv.get_children()[self.current_selection_tv_id-1]
                self.tv.selection_set(child_id)
                self.tv.yview_moveto(self.current_selection_tv_id)

            else:
                pass

    def call_delete(self, event):
        if self.deleting == "task":
            self.delete_task()
        if self.deleting == "update":
            self.delete_update()

    def call_delete_bt(self):
        if self.deleting == "task":
            self.delete_task()
        if self.deleting == "update":
            self.delete_update()

    def check_update_click(self):

        # self.action = "new_update"

        selection = self.tv.selection()
        if selection:

                try:
                    self.action = "click_update_check"

                    print(self.task_list[self.current_selection_tv_id -1].update_list[self.var_updates][2])
                    self.task_list[self.current_selection_tv_id -1].change_status_update(self.var_updates)
                    print(self.task_list[self.current_selection_tv_id -1].update_list[self.var_updates][2])

                    self.create_tv_rows()

                    child_id = self.tv.get_children()[self.current_selection_tv_id-1]
                    self.tv.selection_set(child_id)
                    self.tv.yview_moveto(self.current_selection_tv_id)  
                    self.box.current(self.var_updates)

                except:
                    print("passou")
                    pass

            # print(index_)
            # box.current(index_)

            # var_update_ = task_list[id_-1].update_list[index_final][2]
        
            # if var_update_ == 0:
            #     # update_status = 'TO DO'
            #     var_update.set(True)
            # else:
            #     # update_status = 'DONE '
            #     var_update.set(False)


if __name__ == "__main__":
    win = Window()
    win.mainloop()