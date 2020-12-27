import time
import datetime
import pickle
import os

from tasks import Task, save_path, task_list

# save_path = "saves.pickle"
# task_list = []

if __name__=='__main__':
    if os.path.exists(save_path):
        with open(save_path, 'rb') as f:
            task_list = pickle.load(f)

    # showing tasks
    for task in task_list:
        task.show_infos()
