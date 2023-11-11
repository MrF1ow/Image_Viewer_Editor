from tkinter import Toplevel, Label, Scale, HORIZONTAL, Button, RIGHT, IntVar, Entry
from PIL import Image, ImageTk, ImageFilter
from image_properties import ImageProperties
import cv2

class ResizeWindow(Toplevel):
    def __init__(self, master=None):
        Toplevel.__init__(self, master=master)

        self.original_image = self.master.master.original_image
        self.processing_image = self.master.master.processed_image

        Label(self, text="Width").pack()
        self.width = Entry(self)
        self.width.insert(0, str(ImageProperties.image_width))
        self.width.pack()
        
        Label(self, text="Height").pack()
        self.height = Entry(self)
        self.height.insert(0, str(ImageProperties.image_height))
        self.height.pack()

        Button(self, text="Apply Resize", command=self._apply_resize).pack()


    def _apply_resize(self):
        self.processing_image = cv2.resize(self.processing_image, (int(self.width.get()), int(self.height.get())))
        self.master.master.processed_image = self.processing_image
        self.master.master.image_viewer.display_image()

        self.destroy()