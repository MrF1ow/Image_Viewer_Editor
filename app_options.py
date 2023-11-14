from tkinter import Frame, Button, LEFT, Menu
from file_manager import FileManager
import cv2 as cv

class AppOptions(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master=master)

        self.file_options_button = Button(self, text="File", command=self._show_file_menu)
        self.file_options_button.pack(side=LEFT)

        self.file_menu = Menu(self, tearoff=0)
        self.file_menu.add_command(label="New", command=self.new_button_click)
        self.file_menu.add_command(label="Save", command=self.save_button_click)
        self.file_menu.add_command(label="Save As", command=self.save_as_button_click)

        self.edit_options_button = Button(self, text="Edit", command=self._show_edit_menu)
        self.edit_options_button.pack(side=LEFT)

        self.edit_menu = Menu(self, tearoff=0)
        #add undo and redo once implemented
        self.edit_menu.add_command(label="Batch Processing")

    def _show_file_menu(self, event=None):
        self.file_menu.post(self.file_options_button.winfo_rootx(), self.file_options_button.winfo_rooty() + self.file_options_button.winfo_height())

    def _show_edit_menu(self, event=None):
        self.edit_menu.post(self.edit_options_button.winfo_rootx(), self.edit_options_button.winfo_rooty() + self.edit_options_button.winfo_height())

    def new_button_click(self, event=None):
        fm = FileManager()
        fm.get_file()

        if fm.file is not None:
            self.master.file_location = fm.file
            image = cv.imread(fm.file)
            self.master.master.original_image = image.copy()
            self.master.master.processed_image = image.copy()
            self.master.master.image_viewer.display_image(image)

    def save_button_click(self, event=None):
        fm = FileManager()
        path = self.master.file_location
        fm.find_file(path)

        if fm.file is not None:
            fm.save_file(self.master.master.processed_image)

    def save_as_button_click(self, event=None):
        fm = FileManager()
        path = self.master.file_location
        fm.find_file(path)

        if fm.file is not None:
            fm.save_as_file(self.master.master.processed_image)

