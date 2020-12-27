import time
import datetime

task_list = []

class Task:

    def __init__(self, title, description, finish_date):

        self.task_id = len(task_list)
        self.task_title = title
        self.task_description = description
        self.task_start_date = str(datetime.datetime.fromtimestamp(int(time.time())).strftime('%d/%m/%Y'))
        self.task_finish_date = finish_date
        self.task_active_status = True
        self.update_list = []

    def update_task(self, up_desc, up_date):
        self.update_list.append((up_desc, up_date))

    def change_status_task(self):
        self.task_active_status = False

    def show_infos(self):

        print(f"Id: {self.task_id}\nTitle: {self.task_title}\nDescription: {self.task_description}\nStart Date: {self.task_start_date}\nFinish Date: {self.task_finish_date}\nActive Status: {self.task_active_status}\nUpdate List:\n")
        if len(self.update_list) == 0:
            print("\tThere's no updates.\n")
        else:
            for cont, update in enumerate(self.update_list, start=1):
                print(f"\tUdate {cont}\n\tUpdate Date: {update[0]}\n\tUpdate Description: {update[1]}\n")
        print("----------------------------------------")

# adding tasks
task = Task('Task 1', 'Study Python Functions', '29/12/2020')
task_list.append(task)
task = Task('Task 2', 'Study Python Dict', '30/12/2020')
task_list.append(task)
task = Task('Task 3', 'Study Python Lists', '31/12/2020')
task_list.append(task)

# updating tasks
task_list[0].update_task('First update', '27/12/2020')
task_list[2].update_task('First update', '27/12/2020')
task_list[2].update_task('Second update', '28/12/2020')

# change status task
task_list[1].change_status_task()

# showing tasks
for task in task_list:
    task.show_infos()