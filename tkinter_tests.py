from tkinter import *
from tkinter import ttk
from tkinter import font
from tkinter import messagebox

###################################################################################################

# save_path = f"C:\\Users\\{getlogin()}\\Documents\\saves.pkl"
task_list = []

intern_color = "gray4"
extern_color = "gray9"

###################################################################################################

class Window(Tk):
    def __init__(self):
        super(Window, self).__init__()

        self.title('Diary4')
        self.configure(bg=extern_color)
        # self.minsize(500,400)
        self.wm_iconbitmap('icon512.ico')
        # self.state('zoomed')
        
        self.create_style()
        self.create_layout()
        self.create_tv()

        # self.bind('<Escape>', lambda event: self.state('normal'))
        # self.bind('<F11>', lambda event: self.state('zoomed'))

    def create_style(self):
        self.style = ttk.Style()
        self.style.theme_use("default")

    def create_layout(self):
        self.tv_frame = Frame(self,
                        width=200,
                        height=120,
                        bg='white')

        self.tv_frame.pack(expand=True, fill=X)

        self.bt_frame = Frame(self,
                        width=200,
                        height=120,
                        bg='white')

        self.bt_frame.pack(expand=True, fill=X)

        self.entry_frame = Frame(self,
                        width=200,
                        height=120,
                        bg='white')

        self.entry_frame.pack(expand=True, fill=X)

    def create_tv(self):
        self.tabControl = ttk.Notebook(self.tv_frame)
        self.tabControl.pack(expand=1, fill="both") 

        self.tab1 = ttk.Frame(self.tabControl, height=250)
        self.tab2 = ttk.Frame(self.tabControl)

        self.tabControl.add(self.tab1, text='Tab 1')
        self.tabControl.add(self.tab2, text='Tab 2')

        # self.style.configure("TNotebook", background='red')
        # self.style.map("TNotebook.Tab", background=[("selected", 'blue')], foreground=[("selected", 'white')])
        # self.style.configure("TNotebook.Tab", background='black', foreground='white') 
        self.style.theme_create( "yummy", parent="alt", settings={
                                                        "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0] } },
                                                        "TNotebook.Tab": {
                                                            "configure": {  "padding": [5, 1],
                                                                            "background": 'white',"foreground": 'black', "borderwidth": 4},
                                                            "map":       {"background": [("selected", 'black')],
                                                                        "expand": [("selected", [1, 1, 1, 0])],
                                                                        "foreground": [("selected", "white")],
                                                                        "borderwidth":[("selected", 4)] } } } )

        self.style.theme_use("yummy")
        # self.botao = Button(self.tab1, text='click')
        # self.botao.pack()

win = Window()
win.mainloop()