class Task:

    def __init__(self, id_, title, description, start_date):
        self.task_id = id_
        self.task_title = title
        self.task_description = description
        self.task_start_date = start_date
        self.task_done_status = False
        self.update_list = []

    def add_update_task(self, update_date, up_desc):
        self.update_list.append([update_date, up_desc])
        
    def change_status_task(self):
        self.task_done_status = not self.task_done_status