from tkinter import Frame, Button, Listbox, Scrollbar, END, Y, LEFT, RIGHT, BOTH, YES, BOTTOM, X, TOP, CENTER
from tkinter import ttk
from image_properties import ImageProperties

class History(Frame):
    def __init__(self, master=None):
        # Initializes the History class, creating a frame to display history edits

        Frame.__init__(self, master=master, bg="#6b6b6b")

        # Fetches the history array from the master and sets initial indices
        self.history_arr = self.master.master.history
        self.history_length = len(self.history_arr)
        self.current_index = self.history_length - 1
        self.starting_index = 0

        # Creates a frame for the history display
        history_frame = Frame(self, bg="#6b6b6b")
        history_frame.pack(side=TOP, fill=BOTH, expand=YES)

        # Sets up a Treeview widget for displaying history items
        self.history_tree = ttk.Treeview(history_frame, columns=("Title", "Time"), show="headings", height=20)
        self.history_tree.pack(side=TOP, fill=BOTH, expand=YES)

        # Configures columns and headings for the Treeview
        self.history_tree.column("Title", width=150, anchor=CENTER)
        self.history_tree.column("Time", width=100, anchor=CENTER)
        self.history_tree.heading("Title", text="Edit")
        self.history_tree.heading("Time", text="Time")

        # Inserts existing history items into the Treeview
        for item in self.history_arr:
            self.history_tree.insert("", END, values=(item.title, item.time))

        # Creates a frame for buttons related to undo and redo actions
        button_frame = Frame(history_frame, bg="#6b6b6b")
        button_frame.pack(side=BOTTOM, fill=X)

        # Buttons for undo and redo actions
        self.undo_edit_button = Button(button_frame, text="Undo", command=self.undo_action)
        self.redo_edit_button = Button(button_frame, text="Redo", command=self.redo_action)
        self.undo_edit_button.pack(side=LEFT)
        self.redo_edit_button.pack(side=LEFT)


    def undo_action(self):
        # Handles the undo action by decrementing the current index and retrieving the property instance
        if self.current_index > self.starting_index:
            self.current_index -= 1
        property_instance = self.history_arr[self.current_index]
        print(property_instance)  # Outputs the property instance to console

    def redo_action(self):
        # Handles the redo action by incrementing the current index and retrieving the property instance
        if self.current_index < self.history_length - 1:
            self.current_index += 1
        property_instance = self.history_arr[self.history_length-1]
        print(property_instance)  # Outputs the property instance to console

    def update_history_listbox(self):
        # Clears the existing history items in the Treeview
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)

        # Inserts new items from the updated history list into the Treeview
        for item in self.history_arr:
            self.history_tree.insert("", END, values=(item.title, item.time))
