from tkinter import Toplevel, Label, Scale, HORIZONTAL
import cv2

class AdvancedEditorTools(Toplevel):
    def __init__(self, master=None):
        Toplevel.__init__(self, master=master)

        self.original_image = self.master.master.processed_image
        self.processing_image = self.master.master.processed_image

        self.brightness_label = Label(self, text="Brightness")
        # slider with range of -1 to 1
        # the command parameter is used to select a function that will be called everytime there is a change in the value of the slider
        self.brightness_scale = Scale(self, from_=0, to_=2, length=250, resolution=0.1, orient=HORIZONTAL, command=self._change_brightness_of_image)

        # set the initial value of the scale
        self.brightness_scale.set(1)

        self.brightness_label.pack()
        self.brightness_scale.pack()

    def _change_brightness_of_image(self, event):
        # alpha is set to retrieve the value of the slider (review documentation on convertScaleAbs
        self.processing_image = cv2.convertScaleAbs(self.original_image, alpha=self.brightness_scale.get())
        self.update_displayed_image()

    def update_displayed_image(self):
        self.master.master.image_viewer.display_image(img=self.processing_image)
