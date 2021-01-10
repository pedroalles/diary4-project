import os
from Task2 import Task
import time
import datetime
import pickle
from tkinter import *
from tkinter import ttk
from tkinter import font
from tkinter import messagebox


class Diary(Tk):

    def __init__(self):
        super(Diary, self).__init__()

        self.attributes('-alpha', 0.0)

        self.selection_color = "SteelBlue2"
        self.intern_color = "gray3"
        self.extern_color = "gray7"
        self.font_color = 'white'
        self.font_labels = (None, 12, 'bold')
        self.font_entrys = (None, 12)

        self.user = os.getlogin()
        self.save_path = f"C:\\Users\\{self.user}\\Documents\\Diary\\sv.pkl"
        self.save_directory = f"C:\\Users\\{self.user}\\Documents\\Diary"

        self.taskList = []

        # for task in range(1,11):
        #     startDate = str(datetime.datetime.fromtimestamp(int(time.time())).strftime('%d/%m/%y  %H:%M'))
        #     newTask = Task(task, f'Task {task:02d}', f'Description {task:02d}', startDate)
        #     self.taskList.append(newTask)

        self.config(bg=self.extern_color)

        self.open_database()
       
        self.geometry("1351x690+0+0")
        self.startGui()


    def startGui(self):

        self.create_style()
        self.createLayout()

        self.createButtons()

        self.createCheckTasks()
        self.populateCheckTasks()
        
        self.createTreeView()
        self.populateTvRows()

        self.createUpdateLf()
        self.createUpdateHeaders()

        self.bind("<Return>", self.enter_checkTaskClick)
        self.bind('<Delete>', self.call_delete)
        self.tv.bind("<<TreeviewSelect>>", self.selectTvItens)
        self.protocol("WM_DELETE_WINDOW", self.close_window)
        
        self.after(350, self.attributes, "-alpha", 1.0)


    def open_database(self):
        if os.path.exists(self.save_directory):
            if os.path.exists(self.save_path):
                with open(self.save_path, 'rb') as f:
                    self.taskList = pickle.load(f)
        else:
            os.mkdir(self.save_directory)

    def save_database(self):
        with open(self.save_path, "wb") as f:
            pickle.dump(self.taskList, f, protocol=pickle.HIGHEST_PROTOCOL)

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
        self.style.configure("Treeview.Heading", font=self.font_labels, borderwidth=3, background='SteelBlue2', foreground="black", fieldbackground=self.intern_color)
        self.style.configure("Treeview", font=self.font_entrys, borderwidth=0, background=self.intern_color, foreground=self.font_color, fieldbackground=self.intern_color)
        self.style.configure('Treeview', rowheight=25)

        # self.style.configure('TSeparator', borderwidth=10)


        self.style.map("Treeview.Heading", foreground=[('pressed', 'white')], background=[('pressed', self.intern_color)])
        self.style.map("Treeview", foreground=[('selected', 'black')],  background=[('selected', 'SteelBlue2')])

        # self.style.map('TCombobox', fieldbackground=[('readonly',self.intern_color)])
        # self.style.map('TCombobox', background=[('readonly', 'SteelBlue2')])
        # self.style.map('TCombobox', foreground=[('readonly', self.font_color)])
        # self.style.map('TCombobox', borderwidth = [('readonly', 4)])
        # self.style.map('TCombobox', selectbackground=[('readonly', self.intern_color)])
        # self.style.map('TCombobox', selectforeground=[('readonly', self.font_color)])
        # self.style.map('TCombobox', selectborderwidth = [('readonly', 0)])

        # bigfont = font.Font(family="Helvetica",size=12)
        # self.option_add("*TCombobox*Listbox*Font", bigfont)
        # self.option_add('*TCombobox*Listbox.Background', self.intern_color) 
        # self.option_add('*TCombobox*Listbox.Foreground', self.font_color) 
        # self.option_add('*TCombobox*Listbox.selectBackground', 'SteelBlue2') 
        # self.option_add('*TCombobox*Listbox.Justify', 'center')

        # style.configure( 'Vertical.TScrollbar', background='SteelBlue2' )


    def createLayout(self):

        self.btFrame = LabelFrame(self, bg=self.extern_color, bd=3)
        # self.btFrame.grid(row=0, column=0, padx=(10,0), pady=(10,10), sticky=EW, columnspan=4)
        self.btFrame.pack(side=TOP, expand=1, fill=BOTH, padx=(10,10), pady=(10,10))
        # self.btFrame.pack_propagate(False)


        self.labelframe = LabelFrame(self, bg=self.intern_color, bd=3)
        # self.labelframe.grid(row=1, column=0, padx=(10,10), pady=(0,5), columnspan=2)
        self.labelframe.pack(side=LEFT, expand=1, fill=BOTH, padx=(10,10), pady=(10,10))
        # self.labelframe.pack_propagate(False)

        self.taskCheckFrame = Frame(self.labelframe, bg=self.intern_color, width=48)
        self.taskCheckFrame.pack(side=LEFT, expand=0, fill=BOTH, padx=(0,0), pady=(25,0))
        # self.taskCheckFrame.grid(row=1, column=0, padx=(0,0), pady=(25,0), sticky=N)
        
        self.tvFrame = Frame(self.labelframe, bg=self.intern_color)
        self.tvFrame.pack(side=LEFT, expand=1, fill=BOTH, padx=(0,0), pady=(0,10))
        # self.tvFrame.grid(row=1, column=1, padx=(0,0), pady=(0,0), sticky=N)

        self.updateLf = LabelFrame(self, text=f'  Updates:  00  ', bd=3, bg=self.extern_color, font=self.font_labels, fg=self.font_color)
        self.updateLf.pack(side=LEFT, expand=1, fill=BOTH, padx=(10,10), pady=(0,10))
        # self.updatesFrame.grid(row=1, column=3, padx=(10,0), pady=(0,5), sticky=N)
        # self.updateLf.pack_propagate(False)
        
    
    def createButtons(self):
        bt_borderwidth = 4
        bt_width = 14

        self.bt_add_task = Button(self.btFrame,
            text='New Task',
            borderwidth=bt_borderwidth,
            width=bt_width,
            font=self.font_labels,
            bg='SteelBlue2',
            command=self.new_win_add_task,
            activebackground=self.intern_color,
            activeforeground='white')
        # self.bt_add_task.grid(row=0, column=0, padx=(0,10), pady=(0,0), ipady=(3), sticky=N)
        self.bt_add_task.pack(side=LEFT, expand=1, fill=BOTH, padx=(0,0), pady=(0,0), ipady=(0))
        self.bt_add_update = Button(self.btFrame,
            borderwidth=bt_borderwidth,
            font=self.font_labels,
            width=bt_width,
            text='Add Update',
            command=self.new_win_update_tak,
            bg='Lime Green',
            activebackground=self.intern_color,
            activeforeground='white')
        self.bt_add_update.pack(side=LEFT, expand=1, fill=BOTH, padx=(0,0), pady=(0,0), ipady=(0))
        # self.bt_add_update.grid(row=0, column=1, padx=(0,10), pady=(0,0), ipady=(3), sticky=N)

        self.bt_del_task = Button(self.btFrame,
            borderwidth=bt_borderwidth,
            font=self.font_labels,
            width=bt_width,
            text='Delete',
            command=self.delete_task,
            bg='Tomato2',
            activebackground=self.intern_color,
            activeforeground='white')
        self.bt_del_task.pack(side=LEFT, expand=1, fill=BOTH, padx=(0,0), pady=(0,0), ipady=(0))
        # self.bt_del_task.grid(row=0, column=2, pady=(0,0), ipady=(3), sticky=N)


    def createCheckTasks(self):
        
        self.checksTasksWidgets = []
        self.checksTasksVars = [] 

        for task in range(len(self.taskList)):

            self.c_var = BooleanVar()
            self.checksTasksVars.append(self.c_var)

            self.c = Checkbutton(self.taskCheckFrame,
                variable=self.checksTasksVars[task],
                bg=self.intern_color,
                activebackground=self.selection_color,
                state=DISABLED)

            self.checksTasksWidgets.append(self.c)
            self.c.grid(row=task, column=0, padx=(0,0), pady=(0,0), ipadx=(10), sticky=N)
            self.c.bind("<ButtonPress-1>", self.checkTasksClick)

    def populateCheckTasks(self):

        for cont, check in enumerate(self.taskList):

            taskStatus =  self.taskList[cont].task_done_status
            if taskStatus == False:
                self.checksTasksVars[cont].set(False)
            else:
                self.checksTasksVars[cont].set(True)

    def checkTasksClick(self, event):

        check = event.widget
        check_id = self.checksTasksWidgets.index(check)

        # print(self.currentSelectionTv)
        # print(check_id)

        if (check_id + 1) == self.currentSelectionTv:

            self.taskList[check_id].change_status_task()

            # print(self.taskList[check_id].task_done_status)

    def enter_checkTaskClick(self, event):

        selection = self.tv.selection()
        if selection: 

            # print(self.currentSelectionTv)
            self.taskList[self.currentSelectionTv-1].change_status_task()
            self.checksTasksVars[self.currentSelectionTv-1].set(self.taskList[self.currentSelectionTv-1].task_done_status)


    def createTreeView(self):
        self.tv = ttk.Treeview(self.tvFrame, height=22)
        self.tv.pack(expand=1, fill=BOTH, side=TOP)

        self.currentSelectionTv = 0

        self.tv["column"] = ['ID','Start Date','Task Title','Task Description']
        self.tv["show"] = "headings"

        self.tv.column("ID", minwidth=55, width=55, anchor='center')
        self.tv.column("Start Date", minwidth=150, width=150, anchor='center')
        self.tv.column("Task Title", minwidth=230, width=230, anchor='w')
        self.tv.column("Task Description", minwidth=300, width=300, anchor='w')

        def treeview_sort_column(tv, col, reverse):

            l = [(tv.set(k, col), k) for k in tv.get_children('')]
            try:
                l.sort(key=lambda t: float(t[0]), reverse=reverse)

            except ValueError:
                l.sort(reverse=reverse)

            for index, (val, k) in enumerate(l):
                tv.move(k, '', index)

            tv.heading(col, command=lambda: treeview_sort_column(tv, col, not reverse)) 

            # tv.yview_moveto(0) #move scrollbar to top

        for column in self.tv["column"]:
            self.tv.heading(column, text=column, command=lambda _col=column: treeview_sort_column(self.tv, _col, False))

    def populateTvRows(self):

        self.rows = []

        for i in self.tv.get_children():
            self.tv.delete(i)

        for cont, task in enumerate(self.taskList):

            taskId = f'{int(self.taskList[cont].task_id):02d}'
            taskStartDate = self.taskList[cont].task_start_date
            taskTitle = self.taskList[cont].task_title
            taskDescription = self.taskList[cont].task_description



            self.rows.append([  taskId,
                                taskStartDate,
                                taskTitle,
                                taskDescription
                            ])
 
        for row in self.rows:
            self.tv.insert("", "end", values=row)

        try:
            child_id = self.tv.get_children()[0]
            self.tv.selection_set(child_id)
            self.tv.focus(child_id)
            self.tv.focus_set()
        except:
            pass

    def selectTvItens(self, event):

        selection = self.tv.selection()
        if selection:
            # print(selection)
            self.item = self.tv.item(selection)

            # print(self.item)

            self.currentSelectionTv = int(self.item['values'][0]) 

            # print(self.currentSelectionTv)
            for cont, check in enumerate(self.checksTasksWidgets):
                check.config(bg=self.intern_color)
                check.config(state=DISABLED)
                

            self.currentCheckTask = self.checksTasksWidgets[self.currentSelectionTv-1]
            self.currentCheckTask.config(bg=self.selection_color)
            self.currentCheckTask.config(state=NORMAL)

            self.updateLf.configure(text=f'  Updates:  {len(self.taskList[self.currentSelectionTv-1].update_list):02d}  ')
            
            self.createUpdateList()
            self.checkTop.config(bg=self.extern_color, fg='white', activebackground=self.extern_color, activeforeground='white',selectcolor=self.extern_color)

            if len(self.taskList[self.currentSelectionTv-1].update_list) == 0:
                self.checkUpdateTopVar.set(0)
            # else:
            #     self.checkUpdateTopVar.set(0)


    def createUpdateLf(self):
        self.updateHeaderFrame = Frame(self.updateLf,
            bg=self.extern_color)
        self.updateHeaderFrame.grid(row=0, column=0, sticky=EW)

        # ttk.Separator(self.updateLf).place(x=0, y=36, relwidth=1)
        ttk.Separator(self.updateLf).place(x=0, y=37, relwidth=1, relheight=0.002)

        self.updateListFrame = Frame(self.updateLf,
            bg=self.extern_color)
        self.updateListFrame.grid(row=2, column=0, sticky=EW, pady=(0,5))

    def createUpdateHeaders(self):

        self.checkUpdateTopVar = BooleanVar()
        # c_vars.append(c_var)
        self.checkTop = Checkbutton(self.updateHeaderFrame,
            variable=self.checkUpdateTopVar,
            bg=self.extern_color,
            activebackground=self.extern_color,
            # state=DISABLED
            )
        
        # self.checkUpdateTopVar.set(True)
        
        if len(self.taskList) > 0:
            for update in self.taskList[self.currentSelectionTv-1].update_list:
                if update[2] == False:
                    self.checkUpdateTopVar.set(False)
            
        self.checkTop.bind("<ButtonPress-1>", self.confirm_mark_all)

        # update_check_objects.append(c)

        self.checkTop.grid(row=0, column=0, padx=(10,10), pady=(5,15))

        lb1 = Label(self.updateHeaderFrame,
            width=13,
            text='Update Date',
            bg=self.extern_color,
            fg=self.font_color,
            font=self.font_labels,
            anchor='w')
        lb1.grid(row=0, column=1, sticky=EW, padx=(0,0), pady=(5,15))

        lb2 = Label(self.updateHeaderFrame,
        width=28,
        bg=self.extern_color,
        fg=self.font_color,
        text='Update Description',
        font=self.font_labels,
        anchor='w')
        lb2.grid(row=0, column=2, sticky=EW, padx=(10,0), pady=(5,15))
    
    def createUpdateList(self):

        self.update_check_objects = []
        self.update_date_objects = []
        self.update_description_objects = []

        self.c_vars = []
        e_update_date_vars = []
        e_description_vars = []

        for child in self.updateListFrame.winfo_children():
            child.grid_remove()

        for cont, update in enumerate(self.taskList[self.currentSelectionTv-1].update_list):

            c_var = BooleanVar()
            self.c_vars.append(c_var)
            c = Checkbutton(self.updateListFrame,
                variable=self.c_vars[cont],
                bg=self.extern_color,
                activebackground=self.extern_color,
                # state=DISABLED
                )
            c.bind("<ButtonPress-1>", self.checkUpdatesClick)
            self.update_check_objects.append(c)
            c.grid(row=cont, column=0, padx=(10,10), pady=(0,5), sticky=EW)

            self.update_check = self.taskList[self.currentSelectionTv-1].update_list[cont][2]

            if self.update_check == False:
                self.c_vars[cont].set(False)
            else:
                self.c_vars[cont].set(True)


            e_update_date_var = StringVar()
            e_update_date_vars.append(e_update_date_var)
            e = Entry(self.updateListFrame,
                textvariable=e_update_date_vars[cont],
                bg=self.intern_color,
                fg=self.font_color,
                font=(None, 12),
                width=14,
                justify='center'
                )

            self.update_date_objects.append(e)
            # update_date_objects[cont].bind('<ButtonPress-1>', press_enter)

            e.grid(row=cont, column=1, padx=(0,10), pady=(0,5), sticky=EW)
            e.insert(0, update[0])

            e_description_var = StringVar()
            e_description_vars.append(e_description_var)
            e = Entry(self.updateListFrame,
                textvariable=e_description_vars[cont],
                bg=self.intern_color,
                fg=self.font_color,
                font=(None, 12),
                width=30)

            self.update_description_objects.append(e)
            # update_description_objects[cont].bind('<ButtonPress-1>', press_enter)

            e.grid(row=cont, column=2, padx=(10,10), pady=(0,5), sticky=EW)
            e.insert(0, update[1])

            if len(self.taskList[self.currentSelectionTv-1].update_list) > 0:
                self.checkUpdateTopVar.set(1)
            else:
                self.checkUpdateTopVar.set(0)

            for update in self.taskList[self.currentSelectionTv-1].update_list:
                if update[2] == False:
                    self.checkUpdateTopVar.set(False)

    def checkUpdatesClick(self, event):
        check = event.widget
        check_id = self.update_check_objects.index(check)

        # print(check_id)

        self.taskList[self.currentSelectionTv-1].update_list[check_id][2] = not self.taskList[self.currentSelectionTv-1].update_list[check_id][2]

        self.checkUpdateTopVar.set(True)
        for update in self.taskList[self.currentSelectionTv-1].update_list:
            if update[2] == False:
                self.checkUpdateTopVar.set(False)

        # update_all()
        # root.focus()
        # print(update_check_list)
        # if False in update_check_list:
        #     c1_var.set(False)
        # else:
        #     c1_var.set(True)

        # if True in update_check_list:
        #     print("tem true")
        # else:
        #     c1_var.set(False)
        # print(update_date_list)
        # print(update_description_list)


    def confirm_mark_all(self, event):

        if self.currentSelectionTv == 0:
            return

        if len(self.taskList[self.currentSelectionTv-1].update_list) == 0:
            return

        self.checkUpdateTopVarStatus = self.checkUpdateTopVar.get()

        if self.checkUpdateTopVarStatus == 0:
            msg = "Mark all updates as complete."
        else:
            msg = "Mark all updates as incomplete."

        result = messagebox.askquestion("Confirm", f"{msg} Are you sure?", icon='warning')
        if result == 'yes':
            for cont, check in enumerate(self.c_vars):
                if self.taskList[self.currentSelectionTv-1].update_list[cont][2] == self.checkUpdateTopVarStatus:
                    self.taskList[self.currentSelectionTv-1].update_list[cont][2] = not self.taskList[self.currentSelectionTv-1].update_list[cont][2]
                else:
                    pass
                # self.c_vars[cont].set(not self.checkUpdateTopVarStatus)

                self.checkUpdateTopVar.set(not self.checkUpdateTopVarStatus)
            # print(update_check_list)

            child_id = self.tv.get_children()[self.currentSelectionTv-1]
            self.tv.selection_set(child_id)

        else:
            pass

        # root.focus()


    def new_win_add_task(self):

        try:
            self.tv.yview_moveto(0)
        except:
            pass
        
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
        self.taskList.append(Task(self.new_task_id, self.new_task_title, self.new_task_decription, self.start_date))

        self.tv.config(height=len(self.taskList))

        self.c_var = BooleanVar()
        self.checksTasksVars.append(self.c_var)

        self.c = Checkbutton(self.taskCheckFrame,
            variable=self.checksTasksVars[-1],
            bg=self.intern_color,
            activebackground=self.selection_color,
            state=DISABLED)

        self.checksTasksWidgets.append(self.c)
        self.c.grid(row=len(self.checksTasksVars), column=0, padx=(0,0), pady=(0,0), ipadx=(10))
        self.c.bind("<ButtonPress-1>", self.checkTasksClick)

        self.populateCheckTasks()

        self.populateTvRows()

        child_id = self.tv.get_children()[len(self.taskList)-1]
        self.tv.yview_moveto(self.new_task_id) 
        self.tv.selection_set(child_id)
        self.tv.focus(child_id)
        self.newWindow.destroy()

        # self.labelframe.grid_propagate(False)
        self.btFrame.pack_propagate(False)
        self.labelframe.pack_propagate(False)
        self.updateLf.pack_propagate(False)

    def enter_add_task(self, event):
        self.add_task_commit()


    def new_win_update_tak(self):

        try:
            self.newWindow.destroy()
        except:
            try:
                if self.currentSelectionTv == 0:
                    return
            except:
                pass

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
            text=f"  Task ID:  {self.currentSelectionTv}  ",
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
        self.taskList[self.currentSelectionTv-1].add_update_task(self.update_date, self.new_update_desc, False)

        # self.create_tv_rows()
        
        child_id = self.tv.get_children()[self.currentSelectionTv-1]
        self.tv.selection_set(child_id)
        # self.tv.yview_moveto(self.currentSelectionTv)  
        self.newWindow.destroy()
        
    def enter_update(self,event):
        self.add_update_commit()


    def delete_task(self):

        selection = self.tv.selection()
        if selection:

            result = messagebox.askquestion("Delete Task", "Are You Sure?", icon='warning')
            if result == 'yes':
                
                self.taskList.pop(self.currentSelectionTv -1)

                for cont, task in enumerate(self.taskList, start=1):
                    task.task_id = cont

                self.checksTasksWidgets[-1].grid_remove()
                self.checksTasksWidgets.pop(-1)

                self.populateCheckTasks()

                self.populateTvRows()

                # self.clear_inputs()

                self.currentSelectionTv = 0

        else:
            pass
    
    def call_delete(self, event):
            self.delete_task()

    def start(self):
        self.mainloop()

if __name__ == "__main__":
    Diary().start()