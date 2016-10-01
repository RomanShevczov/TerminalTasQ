#!usr/bin/env python 3
import os
import glob
import shelve
import readline
import datetime
from termcolor import colored, cprint

print("\nWelcome to TasQ 0.1.7")
print("Type 'help' to see the list of all avaliable commands\n")

allowed_commands = ["help", "exit", "clear", "save", "load", "erase",
                    "tsk", "+tsk", "done", "-tsk", "+archive",
                    "archive", "dearchive", "-archive"]

def show_local_tsk_list():
    # Gets current date & time
    FileStat = os.stat('.')
    CrTime = FileStat.st_mtime
    FormatedTime = str(datetime.datetime.fromtimestamp(CrTime))[0:10]

    print("\nYour task lists:")
    print("---------------------------------------------")
    if len(glob.glob('*.db')) != 0:
        for tsk_lst in glob.glob('*.db'):
            #  Slice to make file names display without .db
            print(colored(FormatedTime, 'grey','on_white') + "   " + colored(tsk_lst[0:-3], attrs = ['bold']))
    else:
        print("You don't have any saved task lists!")
    print("---------------------------------------------")

task_dict = {}
archive_dict = {}
CompletedTasks = []

while True:
    command = input("→ ")

    #  If command consists only of space or it's empty type in your command again
    if len(command) == 0 or command.isspace() == True:
        command = input("→ ")

    elif command in allowed_commands:

        if command == "help":
            print("\nTasQ is task-control terminal-based applicaion")
            print("To use this program you'll need the following commands:\n")
            print(colored("help", attrs = ['bold']) + " - to see this massage again")
            print(colored("clear", attrs = ['bold']) + " - to clear the screen (or press Ctrl + L)")
            print(colored("exit", attrs = ['bold']) + " - to close the program")
            print(colored("save", attrs = ['bold']) + " - to save all your tasks / changes")
            print(colored("load", attrs = ['bold']) + " - to load saved task list")
            print(colored("erase", attrs = ['bold']) + " - to delete saved task list")
            print(colored("+tsk", attrs = ['bold']) + " - to add new task")
            print(colored("tsk", attrs = ['bold']) + " - to see all your tasks")
            print(colored("done", attrs = ['bold']) + " - marks completed task")
            print(colored("-tsk", attrs = ['bold']) + " - to delete task")
            print(colored("archive", attrs = ['bold']) + " - to see all your archived tasks")
            print(colored("+archive", attrs = ['bold']) + " - to move task to the archive")
            print(colored("dearchive", attrs = ['bold']) + " - to add archived task back into the main task list")
            print(colored("-archive", attrs = ['bold']) + " - to delete archived task\n")
            print(colored("Be the best version of yourself!", attrs = ['bold']))
            print("Program was written just for fun by RomanShevczov.\n")

        elif command == "exit":
            print("\nGoodbye!\n")
            break

        elif command == "clear":
            os.system('clear')

        elif command == "save":
            save_name = input("Enter the name of task list: ") + ".db"

            save_data = shelve.open(save_name)
            try:
                save_data['tasks'] = task_dict
                save_data['archive'] = archive_dict
                save_data['completed_tasks'] = CompletedTasks
            finally:
                save_data.close()

        elif command == "load":
            show_local_tsk_list()

            if len(glob.glob('*.db')) > 0:
                FileToLoad = input("\nWhat task list do u want to load?: ") + ".db"

                if FileToLoad in glob.glob('*.db'):
                    save_data = shelve.open(FileToLoad)

                    try:
                        task_dict = save_data['tasks']
                        archive_dict = save_data['archive']
                        CompletedTasks = save_data['completed_tasks']
                    finally:
                        save_data.close()

                else:
                    print("\nThere isn't such task list in your local storage!\n")

        elif command == "erase":
            show_local_tsk_list()

            if len(glob.glob('*.db')) != 0:
                TaskToErase = input("What task list do you want to erase? : ") + ".db"

                if TaskToErase in glob.glob("*.db"):
                    os.remove(TaskToErase)
                else:
                    print("\nThere isn't such task list in your local storage!\n")

        elif command == "+tsk":
            TaskName = input("Task name: ")

            #  Priority settings
            TaskPriority = input("Set the priority of your task (r,g,b): ")

            if TaskPriority not in ["r","g","b","R","G","B"]:
                print("\nPriority must be 'r','g' or 'b'!\n")
                TaskPriority #  Second chance to input correct data

            #  Adds Task & Priority to the task_dict
            task_dict[TaskName] = TaskPriority

        elif command == "done":
            if len(task_dict) == 0:
                print("\nYour task list is empty!\n")

            else:
                DoneTaskName = input("What task have you done? : ")

                if DoneTaskName not in task_dict:
                    #  Second chance to input correct data
                    DoneTaskName = input("Try one more time. What task have you done? : ")
                    if DoneTaskName not in task_dict:
                        print("\nWrong input\n")

                if DoneTaskName in task_dict:
                    CompletedTasks.append(DoneTaskName)

        elif command == "tsk":
            print()

            #  Checks if there are any tasks to display
            if len(task_dict) == 0:
                print("Your task list is empty!")

            else:
                RedTasks = []
                GreenTasks = []
                BlueTasks = []

                #  Iterates through the keys & values of the dictionary
                for name, attr in task_dict.items():

                    if attr == "r":
                        RedTasks.append(name)
                    elif attr == "g":
                        GreenTasks.append(name)
                    elif attr == "b":
                        BlueTasks.append(name)

                #  Prints all the task hierarchically
                #  Prints 'Done' Mark if it's necessary

                for r in RedTasks:
                    if r in CompletedTasks:
                        print(colored(' done ','grey','on_green') + " " + colored(r,'red'))
                    else:
                        print(colored(r,'red'))

                for g in GreenTasks:
                    if g in CompletedTasks:
                        print(colored(' done ','grey','on_green') + " " + colored(g,'green'))
                    else:
                        print(colored(g,'green'))

                for b in BlueTasks:
                    if b in CompletedTasks:
                        print(colored(' done ','grey','on_green') + " " + colored(b,'cyan'))
                    else:
                        print(colored(b,'cyan'))

            print()

        elif command == "-tsk":
            if len(task_dict) == 0:
                print("\nYour task list is empty!\n")
            else:
                DeleteTask = input("What task do you want to get rid of? : ")

                if DeleteTask not in task_dict:
                    print("There isn't such task in your task list!")
                else:
                    del task_dict[DeleteTask]

        elif command == "+archive":

            if len(task_dict) == 0:
                print("\nThere isn't any task to archive\n")
            else:
                ArchiveTask = input("What task do you want to archive? : ")

                if ArchiveTask in task_dict:
                    archive_dict[ArchiveTask] = task_dict[ArchiveTask]
                    del task_dict[ArchiveTask]
                else:
                    print("\nThere isn't such task in your task list!\n")

        elif command == "dearchive":
            if len(archive_dict) == 0:
                print("\nYour archive is empty!\n")
            else:
                TaskToDearchive = input("What task do you want to dearchive? : ")

                if TaskToDearchive in archive_dict:
                    task_dict[TaskToDearchive] = archive_dict[TaskToDearchive]
                    del archive_dict[TaskToDearchive]
                else:
                    print("\nThere isn't such task in your task list!\n")

        elif command == "archive":

            if len(archive_dict) == 0:
                print("\nYour archive is empty!")
            else:
                print()

                RedTasks = []
                GreenTasks = []
                BlueTasks = []

                for name, attr in archive_dict.items():

                    if attr == "r":
                        RedTasks.append(name)
                    elif attr == "g":
                        GreenTasks.append(name)
                    elif attr == "b":
                        BlueTasks.append(name)

                for r in RedTasks:
                    if r in CompletedTasks:
                        print(colored(' done ','grey','on_green') + " " + colored(r,'red'))
                    else:
                        print(colored(r,'red'))

                for g in GreenTasks:
                    if g in CompletedTasks:
                        print(colored(' done ','grey','on_green') + " " + colored(g,'green'))
                    else:
                        print(colored(g,'green'))

                for b in BlueTasks:
                    if b in CompletedTasks:
                        print(colored(' done ','grey','on_green') + " " + colored(b,'cyan'))
                    else:
                        print(colored(b,'cyan'))

            print()

        elif command == "-archive":
            if len(archive_dict) == 0:
                print("Your archive is empty!")
            else:
                ArchiveTaskToDelete = input("What archived task do you want to get rid of? : ")

                if ArchiveTaskToDelete not in archive_dict:
                    print("There isn't such task in your archive")
                else:
                    del archive_dict[ArchiveTaskToDelete]

    else:
        print("wtf? unknown command!")
