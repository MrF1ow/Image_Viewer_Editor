from tkinter import Toplevel, Label, Scale, HORIZONTAL, Button, RIGHT
from PIL import Image, ImageTk, ImageFilter
from image_properties import ImageProperties
import cv2
import numpy as np


class AdvancedEditorTools(Toplevel):
    def __init__(self, master=None):
        Toplevel.__init__(self, master=master)

        self.original_image = self.master.master.original_image
        self.processing_image = self.master.master.processed_image

        self.brightness_label = Label(self, text="Brightness")
        # slider with range of -1 to 1
        # the command parameter is used to select a function that will be called everytime there is a change in the value of the slider
        self.brightness_scale = Scale(self, from_=0, to_=2, length=250,
                                      resolution=0.1, orient=HORIZONTAL, command=self._show_editor_tools)

        self.blur_label = Label(self, text="Blur")
        self.blur_scale = Scale(self, from_=0, to_=100, length=250,
                                resolution=5, orient=HORIZONTAL, command=self._show_editor_tools)

        self.hue_label = Label(self, text="Hue")
        self.hue_scale = Scale(self, from_=0, to_=179, length=250,
                               resolution=1, orient=HORIZONTAL, command=self._show_editor_tools)

        self.apply_button = Button(self, text="Apply")
        self.apply_button = Button(
            self, text="Apply", command=self._apply_edits_to_image)

        # set the initial value of the scale
        self.brightness_scale.set(ImageProperties.brightness)
        self.blur_scale.set(ImageProperties.blur_size)
        self.hue_scale.set(ImageProperties.hue)

        self.brightness_label.pack()
        self.brightness_scale.pack()
        self.blur_label.pack()
        self.blur_scale.pack()
        self.hue_label.pack()
        self.hue_scale.pack()
        self.apply_button.pack()

    def _show_editor_tools(self, event):
        # Apply brightness
        # retrieves the value from the slider
        brightness_factor = self.brightness_scale.get()
        # applies the actual brightness change
        self.processing_image = cv2.convertScaleAbs(
            self.original_image, alpha=brightness_factor)
        # updates the brightness value
        ImageProperties.brightness = brightness_factor

        # Apply blur
        blur_size = self.blur_scale.get()
        # this is how distorted each pixel will become
        kernel_size = (blur_size, blur_size)
        # the kernel size had to be a positive, ODD number
        kernel_size = tuple(size + 1 if size %
                            2 == 0 else size for size in kernel_size)
        # applies the actual blur
        self.processing_image = cv2.blur(self.processing_image, kernel_size)
        # updates the blur value
        ImageProperties.blur_size = blur_size

        # Apply Hue Alteration
        hue_value = self.hue_scale.get()
        self._change_hue(hue_value)

        # Update displayed image
        self.update_displayed_image(self.processing_image)

    # this function actually sets the newly processed imaged as the image of the application
    def _apply_edits_to_image(self):
        self.master.master.processed_image = self.processing_image
        self.destroy()  # closes the AdvancedEditorTools (destructor pretty much)

    def _change_hue(self, hue_value):
        # Convert image to HSV
        hsv_image = cv2.cvtColor(self.processing_image, cv2.COLOR_BGR2HSV)
        # Change the hue channel
        # Hue values range from 0 to 179
        hsv_image[:, :, 0] = (hsv_image[:, :, 0] + hue_value) % 180

        # Convert back to BGR
        self.processing_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)

        # Update the hue value in ImageProperties (you may need to define ImageProperties class)
        ImageProperties.hue = hue_value

    def update_displayed_image(self, img=None):
        self.master.master.image_viewer.display_image(img=img)
