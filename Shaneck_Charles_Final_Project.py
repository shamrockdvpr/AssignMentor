# Imports, imports all tkinter modules and imports pickle for data storage
from tkinter import *
import pickle
class Task:
    # Class that defines the bahavior of a single task
    def __init__(self, name):
        # Currently only takes a name value but can be expanded as needed
        self.name = name

    def __repr__(self):
        # returns a string result of the class, uses repr so I can store this as the type too
        return f"{self.name}"

class TaskManager:
    def __init__(self):
        # Initialize attributes
        self.tasks = []  # empty task list
        self.sorted_asc = True # if we press sort it will sort the list in ascending order
        self.savefile = 'savefile.pickle'  # used to avoid 'magic' values

        # Window Setup
        self.root = Tk()
        self.root.geometry('600x400')  # set window size
        self.root.title("AssignMentor")  # assign name
        self.root.resizable(width=False, height=False)  # make it non resizable

        # Create Frames
        self.btn_frm = Frame(master=self.root, relief=SUNKEN, bd=5)

        # Create btn_frm widgets
        # Buttons
        self.add_btn = Button(master=self.btn_frm, text='Add Task', fg='green', bg='white', command=self.create_task_popup)
        self.remove_btn = Button(master=self.btn_frm, fg='green', bg='white', text='Remove Task', command=self.delete_task_popup)
        self.sort_btn = Button(master=self.btn_frm, fg='green', bg='white', text='Sort', command=self.sort_dict)
        self.sort_ord_btn = Button(master=self.btn_frm, fg='green', bg='white', text='\N{UPWARDS BLACK ARROW}', command=self.swap_ord)

        # Title Text
        self.title_lbl = Label(master=self.btn_frm, text='AssignMentor')

        # Save/Load/quit Buttons
        self.save_btn = Button(master=self.btn_frm, fg='green', bg='white', text='Save', command=self.save_file)
        self.load_btn = Button(master=self.btn_frm, fg='green', bg='white', text='Load', command=self.load_file)
        self.quit_btn = Button(master=self.btn_frm, fg='green', bg='white', text='Quit', command=self.quit_prog)

        # Create textbox
        self.tasks_txt = Text(master=self.root, width=50, height=20)
        self.tasks_txt.config(state='disabled')  # make it read only

        # Add widgets to grid
        self.add_btn.grid(row=0, column=0)
        self.remove_btn.grid(row=0, column=1, padx=5)
        self.sort_btn.grid(row=0, column=3)
        self.sort_ord_btn.grid(row=0, column=4)

        self.title_lbl.grid(row=0, column=2, sticky='ew', padx=100)

        self.save_btn.grid(row=0, column=5)
        self.load_btn.grid(row=0, column=6)

        self.quit_btn.grid(row=0, column=7)

        # add frames and text to grid
        self.btn_frm.grid(row=0, column=0, sticky='ew')
        self.tasks_txt.grid(row=1, column=0)

        # Load in save file, skip if there is none yet
        try:
            self.load_file(startup=True)

        except FileNotFoundError:
            pass  # if the file doesn't exist, skip this, we can create one when we save the file

        # start mainloop
        self.root.mainloop()

    def quit_prog(self):
        # Quits the program, saves work space to save file first
        self.save_file(user_gen=False)
        quit()

    def save_file(self, user_gen=True):
        """
        Saves to file using pickle
        :param user_gen: Determines if the program should show the popup declaring it as saved or not
        :return: None
        """
        with open(self.savefile, 'wb') as handle:
            pickle.dump(self.tasks, handle, protocol=pickle.HIGHEST_PROTOCOL)
            if user_gen:  # if the user clicked the save button, display a popup to show the success
                popup = Toplevel()
                save_lbl = Label(master=popup, text=f"Saved to {self.savefile}")
                save_lbl.pack()

    def load_file(self, startup=False):
        """
        Loads save file into workspace
        :param startup: Determines if popup window is needed
        :return: None
        """
        with open(self.savefile, 'rb') as handle:
            self.tasks.clear()  # clear the list
            self.tasks = pickle.load(handle)  # fill the list from the file
            self.update_txt()  # update the text box to show the updated list
            if not startup:  # if the user clicked load, show them a pop up to confirm success
                popup = Toplevel()
                save_lbl = Label(master=popup, text=f"Loaded from {self.savefile}")
                save_lbl.pack()

    def swap_ord(self):
        # Switches between sort ascending or descending, updates button to match
        self.sorted_asc = not self.sorted_asc

        if self.sorted_asc:
            self.sort_ord_btn['text'] = '\N{UPWARDS BLACK ARROW}'

        else:
            self.sort_ord_btn['text'] = '\N{DOWNWARDS BLACK ARROW}'


    def sort_dict(self):
        # Sorts tasks list depending on if sort ascending is true or not
        if self.sorted_asc:
            self.tasks = sorted(self.tasks, key=lambda i: i['name'])

        else:
            self.tasks = sorted(self.tasks, key=lambda i: i['name'], reverse=True)

        # update the user display
        self.update_txt()

    def update_txt(self):
        # Updates text box to display all tasks
        self.tasks_txt.config(state='normal')  # make it so we can edit the text box
        self.tasks_txt.delete('1.0', END)   # clear everything in the text box
        for item in self.tasks:  # go through the list, get each dictionary out
            self.tasks_txt.insert(END, f'{item["name"]}\n')  # for each dictionary, write: the value that corresponds to name, and a new line after
        self.tasks_txt.config(state='disabled')  # Reset text box to read only

    def create_task(self):
        # Creates new task, called by create_task_popup to enter data entered there
        name = self.name_ent.get()  # pull data from input

        if name != '':  # make sure the input isnt blank

            # Creates new task
            task = Task(name)

            # adds task to tasklist
            self.tasks.append({'name' : task.name, 'body' : task})

            # gets rid of popup window
            self.task_popup.destroy()

            # updates text box
            self.update_txt()

        else:
            # display a warning popup
            popup = Toplevel()
            save_lbl = Label(master=popup, text="Task cannot be blank")
            save_lbl.pack()


    def create_task_popup(self):
        # Creates a popup window to enter new tasks into
        self.task_popup = Toplevel()
        self.task_popup.geometry("200x75")  # popup geometry
        self.task_popup.resizable(width=False, height=False)  # non resizeable
        self.task_popup.title("Create new task")  # set title

        # Creates widgets
        self.name_ent = Entry(master=self.task_popup)
        save_btn = Button(master=self.task_popup, text="Save", command=self.create_task, fg='green', bg='white')
        task_lbl = Label(master=self.task_popup, text="Task Name:")

        # Places widgets in space
        task_lbl.grid(row=0, column=0)
        self.name_ent.grid(row=0, column=1, pady=10)
        save_btn.grid(row=1, column=1)

    def delete_task(self):
        # Deletes unwanted tasks
        deleter = self.del_ent.get()

        # Gets all dictionaries and checks that the task name matches the deleted name
        for item in self.tasks:
            if item['name'] == deleter:
                self.tasks.remove(item)  # removes the dictionary from the list if the value for 'name' matches the desired task

        # remove popup
        self.delete_popup.destroy()

        # update text box
        self.update_txt()

    def delete_task_popup(self):
        # Creates popup
        self.delete_popup = Toplevel()
        self.delete_popup.geometry("200x75")
        self.delete_popup.resizable(width=False, height=False)
        self.delete_popup.title('Delete Task')

        # Create widgets
        self.del_ent = Entry(master=self.delete_popup)
        del_btn = Button(master=self.delete_popup, text='Delete', command=self.delete_task, fg='green', bg='white')
        del_lbl = Label(master=self.delete_popup, text="Task Name:")

        # Places widgets in space
        del_lbl.grid(row=0, column=0)
        self.del_ent.grid(row=0, column=1, pady=10)
        del_btn.grid(row=1, column=1)

# Main funtion
def main():
    # Creates new instance of TaskManager
    manager = TaskManager()

# runs main when file is played
if __name__ == '__main__':
    main()