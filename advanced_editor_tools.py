from tkinter import Toplevel, Label, Scale, HORIZONTAL, Button, RIGHT
from PIL import Image, ImageTk, ImageFilter
from image_properties import ImageProperties
import cv2

class AdvancedEditorTools(Toplevel):
    def __init__(self, master=None):
        Toplevel.__init__(self, master=master)

        self.original_image = self.master.master.original_image
        self.processing_image = self.master.master.processed_image

        self.brightness_label = Label(self, text="Brightness")
        # slider with range of -1 to 1
        # the command parameter is used to select a function that will be called everytime there is a change in the value of the slider
        self.brightness_scale = Scale(self, from_=0, to_=2, length=250, resolution=0.1, orient=HORIZONTAL, command=self._show_editor_tools)

        self.blur_label = Label(self, text="Blur")
        self.blur_scale = Scale(self, from_=0, to_=100, length=250, resolution=5, orient=HORIZONTAL, command=self._show_editor_tools)

        self.apply_button = Button(self, text="Apply")
        self.apply_button = Button(self, text="Apply", command=self._apply_edits_to_image)

        # set the initial value of the scale
        self.brightness_scale.set(ImageProperties.brightness)
        self.blur_scale.set(ImageProperties.blur_size)

        self.brightness_label.pack()
        self.brightness_scale.pack()
        self.blur_label.pack()
        self.blur_scale.pack()
        self.apply_button.pack()

    def _show_editor_tools(self, event):
        # Apply brightness
        brightness_factor = self.brightness_scale.get()
        self.processing_image = cv2.convertScaleAbs(self.original_image, alpha=brightness_factor)
        ImageProperties.brightness = brightness_factor

        # Apply blur
        blur_size = self.blur_scale.get()
        kernel_size = (blur_size, blur_size)
        kernel_size = tuple(size + 1 if size % 2 == 0 else size for size in kernel_size)
        self.processing_image = cv2.blur(self.processing_image, kernel_size)
        ImageProperties.blur_size = blur_size

        # Update displayed image
        self.update_displayed_image(self.processing_image)

    def _apply_edits_to_image(self):
        self.master.master.processed_image = self.processing_image
        self.destroy()

    def update_displayed_image(self, img=None):
        self.master.master.image_viewer.display_image(img=img)
