from tkinter import Toplevel, Label, Button, Entry
from image_properties import ImageProperties
import cv2

class ResizeWindow(Toplevel):
    def __init__(self, master=None):
        Toplevel.__init__(self, master=master)

        #Retrieves the image
        self.original_image = self.master.master.original_image
        self.processing_image = self.master.master.processed_image

        #Creates the label for the width input
        Label(self, text="Width").pack()
        #Creates the entry for the width input
        self.width = Entry(self)
        #Inserts the currrently stored values from image properties
        self.width.insert(0, str(ImageProperties.image_width))
        #Packs the widget
        self.width.pack()
        
        #Exactly the same as width, but for height.
        Label(self, text="Height").pack()
        self.height = Entry(self)
        self.height.insert(0, str(ImageProperties.image_height))
        self.height.pack()

        #Applies the resize by calling the apply resize function
        Button(self, text="Apply Resize", command=self._apply_resize).pack()


    def _apply_resize(self):
        #Applies the resize
        self.processing_image = cv2.resize(self.processing_image, (int(self.width.get()), int(self.height.get())))
        #Sends master the processed image
        self.master.master.processed_image = self.processing_image
        #Updates the display
        self.master.master.image_viewer.display_image()

        #Destroys the widget
        self.destroy()