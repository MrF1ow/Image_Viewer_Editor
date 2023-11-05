from tkinter import Frame, Button, LEFT
from file_manager import FileManager
import cv2 as cv

class AppOptions(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master=master)

        self.new_button = Button(self, text="New")
        self.new_button.bind("<ButtonRelease>", self.new_button_click)
        self.new_button.pack(side=LEFT)

        self.save_button = Button(self, text="Save")
        self.save_button.bind("<ButtonRelease>", self.save_button_click)
        self.save_button.pack(side=LEFT)

        self.save_as_button = Button(self, text="Save As")
        self.save_as_button.bind("<ButtonRelease>", self.save_as_button_click)
        self.save_as_button.pack(side=LEFT)


    def new_button_click(self, event):
        fm = FileManager()
        fm.get_file()

        if fm.file is not None:
            self.master.file_location = fm.file
            image = cv.imread(fm.file)
            self.master.original_image = image.copy()
            self.master.image_viewer.display_image(image)

    def save_button_click(self, event):
        fm = FileManager()
        path = self.master.file_location
        fm.find_file(path)

        if fm.file is not None:
            image = cv.imread(fm.file)
            fm.save_file(image)

    def save_as_button_click(self, event):
        fm = FileManager()
        path = self.master.file_location
        fm.find_file(path)

        if fm.file is not None:
            image = cv.imread(fm.file)
            fm.save_as_file(image)
        
