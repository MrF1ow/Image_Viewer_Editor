from tkinter import Frame, Button, Listbox, Scrollbar, END, Y, LEFT, RIGHT, BOTH, YES, BOTTOM, X, TOP, CENTER
from tkinter import ttk
from image_properties import ImageProperties

class History(Frame):
    def __init__(self, master=None):
        # Initializes the History class, creating a frame to display history edits

        Frame.__init__(self, master=master, bg="#6b6b6b")

        # Fetches the history array from the master and sets initial indices
        self.history_arr = self.master.master.history
        self.history_length = 0
        self.current_index = 0
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
        self.undo_edit_button = Button(button_frame, text="Undo")
        self.redo_edit_button = Button(button_frame, text="Redo")
        self.undo_edit_button.bind("<ButtonRelease>", self.undo_action)
        self.redo_edit_button.bind("<ButtonRelease>", self.redo_action)
        self.undo_edit_button.pack(side=LEFT)
        self.redo_edit_button.pack(side=LEFT)

    def _set_indices(self):
        # Sets the current index and starting index
        self.history_length = len(self.history_arr)
        self.current_index = self.history_length - 1
        self.starting_index = 0

    def _set_image_properties(self, property_instance):
        ImageProperties.title = property_instance.title
        ImageProperties.time = property_instance.time
        ImageProperties.is_flipped_horz = property_instance.is_flipped_horz
        ImageProperties.is_flipped_vert = property_instance.is_flipped_vert
        ImageProperties.is_grayscaled = property_instance.is_grayscaled
        ImageProperties.is_sepia = property_instance.is_sepia
        ImageProperties.original_image_height = property_instance.original_image_height
        ImageProperties.original_image_width = property_instance.original_image_width
        ImageProperties.altered_image_height = property_instance.altered_image_height
        ImageProperties.altered_image_width = property_instance.altered_image_width
        ImageProperties.rotation = property_instance.rotation
        ImageProperties.brightness = property_instance.brightness
        ImageProperties.contrast = property_instance.contrast
        ImageProperties.saturation = property_instance.saturation
        ImageProperties.blur = property_instance.blur
        ImageProperties.hue = property_instance.hue
        ImageProperties.crop_start_x = property_instance.crop_start_x
        ImageProperties.crop_start_y = property_instance.crop_start_y
        ImageProperties.crop_end_x = property_instance.crop_end_x
        ImageProperties.crop_end_y = property_instance.crop_end_y
        ImageProperties.crop_ratio = property_instance.crop_ratio

    def undo_action(self, event=None):
        # Handles the undo action by decrementing the current index and retrieving the property instance
        if self.current_index > self.starting_index:
            self.master.master.undo_performed = True
            self.current_index -= 1
        property_instance = self.history_arr[self.current_index]
        self._set_image_properties(property_instance)
        self.update_displayed_image()

    def redo_action(self, event=None):
        # Handles the redo action by incrementing the current index and retrieving the property instance
        if self.current_index < self.history_length - 1:
            self.current_index += 1
            property_instance = self.history_arr[self.current_index]
            self._set_image_properties(property_instance)
            self.update_displayed_image()
        else:
            print("No undo action to redo")

    def update_history_list(self):
        # Clears the existing history items in the Treeview
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)

        # Inserts new items from the updated history list into the Treeview
        for item in self.history_arr:
            self.history_tree.insert("", END, values=(item.title, item.time))

    def _clear_after_edit(self):
        self.history_arr = self.history_arr[:self.current_index + 1]
        self.master.master.history = self.history_arr
        self.master.master.undo_performed = False
        self._set_indices()
        self.update_history_list()

    def update_displayed_image(self):
        self.master.master.image_viewer._apply_all_edits()