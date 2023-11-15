from tkinter import Toplevel, Label, Scale, TOP, HORIZONTAL, Button, RIGHT, LEFT, BOTTOM
from PIL import Image, ImageTk, ImageFilter
from image_properties import ImageProperties
import cv2
import numpy as np


class AdvancedEditorTools(Toplevel):
    def __init__(self, master=None):
        Toplevel.__init__(self, master=master)

        self.original_image = self.master.master.original_image
        self.processing_image = self.master.master.processed_image
        self.displaying_processed_image = True

        # slider with range of -1 to 1
        # the command parameter is used to select a function that will be called everytime there is a change in the value of the slider
        self.brightness_scale = Scale(self, from_=0, to_=100, length=250,
                                      resolution=0.1, orient=HORIZONTAL, command=self._show_editor_tools)
        self.brightness_label = Label(self, text="Brightness")

        self.contrast_label = Label(self, text="Contrast")
        self.contrast_scale = Scale(self, from_=1, to_=127, length=250,
                                    resolution=1, orient=HORIZONTAL, command=self._show_editor_tools)

        self.blur_scale = Scale(self, from_=0, to_=100, length=250,
                                resolution=1, orient=HORIZONTAL, command=self._show_editor_tools)
        self.blur_label = Label(self, text="Blur")

        self.hue_scale = Scale(self, from_=0, to_=179, length=250,
                               resolution=1, orient=HORIZONTAL, command=self._show_editor_tools)
        self.hue_label = Label(self, text="Hue")

        self.saturation_scale = Scale(self, from_=0, to_=255, length=250,
                                      resolution=5, orient=HORIZONTAL, command=self._show_editor_tools)
        self.saturation_label = Label(self, text="Saturation")

        self.apply_button = Button(
            self, text="Apply", command=self._apply_edits_to_image)

        self.cancel_button = Button(self, text="Cancel")
        self.cancel_button.bind("<ButtonRelease>", self._cancel_edits_to_image)

        self.preview_button = Button(self, text="Preview")
        self.preview_button.bind(
            "<ButtonRelease>", self._preview_edits_on_image)

        # set the initial value of the scale
        self.brightness_scale.set(ImageProperties.brightness)
        self.blur_scale.set(ImageProperties.blur_size)
        self.hue_scale.set(ImageProperties.hue)
        self.contrast_scale.set(ImageProperties.contrast)
        self.saturation_scale.set(ImageProperties.saturation)

        # this is how they are structured on the popup
        self.brightness_label.pack()
        self.brightness_scale.pack()
        self.contrast_label.pack()
        self.contrast_scale.pack()
        self.blur_label.pack()
        self.blur_scale.pack()
        self.hue_label.pack()
        self.hue_scale.pack()
        self.saturation_label.pack()
        self.saturation_scale.pack()
        self.preview_button.pack(side=LEFT, anchor='center')
        self.cancel_button.pack(side=LEFT, anchor='center')
        self.apply_button.pack(side=LEFT, anchor='center')

    def _show_editor_tools(self, event):
        # Apply brightness/contrast

        # retrieves the value from the slider
        brightness_factor = self.brightness_scale.get()
        contrast_factor = self.contrast_scale.get()
        # applies the actual brightness change
        self.processing_image = cv2.convertScaleAbs(
            self.original_image, alpha=contrast_factor, beta=brightness_factor)
        # updates the brightness value

        # Apply blur
        blur_size = self.blur_scale.get()
        # this is how distorted each pixel will become
        kernel_size = (blur_size, blur_size)
        # the kernel size had to be a positive, ODD number
        kernel_size = tuple(size + 1 if size %
                            2 == 0 else size for size in kernel_size)
        # applies the actual blur
        self.processing_image = cv2.blur(self.processing_image, kernel_size)

        # Apply Hue Alteration
        hue_value = self.hue_scale.get()
        self._change_hue(hue_value)

        # Apply saturation
        saturation_value = self.saturation_scale.get()
        self._change_saturation(saturation_value)

        # Update displayed image
        self.update_displayed_image(self.processing_image)

    def _change_hue(self, hue_value):
        # Convert image to HSV
        hsv_image = cv2.cvtColor(self.processing_image, cv2.COLOR_BGR2HSV)
        # Change the hue channel
        # Hue values range from 0 to 179
        hsv_image[:, :, 0] = (hsv_image[:, :, 0] + hue_value) % 180

        # Convert back to BGR
        self.processing_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)

    def _change_saturation(self, saturation_value):
        # Convert image to HSV
        hsv_image = cv2.cvtColor(self.processing_image, cv2.COLOR_BGR2HSV)

        # Saturation values range 0 - 255
        hsv_image[:, :, 1] += saturation_value

        # Convert back to BGR
        self.processing_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)

    def update_displayed_image(self, img=None):
        self.master.master.image_viewer.display_image(img=img)

        # this function actually sets the newly processed imaged as the image of the application
    def _apply_edits_to_image(self):
        self.master.master.processed_image = self.processing_image
        ImageProperties.brightness = self.brightness_scale.get()
        ImageProperties.contrast = self.contrast_scale.get()
        ImageProperties.blur_size = self.blur_scale.get()
        ImageProperties.hue = self.hue_scale.get()
        ImageProperties.saturation = self.saturation_scale.get()

        hsv_image = cv2.cvtColor(self.processing_image, cv2.COLOR_BGR2HSV)
        ImageProperties.saturation = hsv_image[:, :, 1]

        self.destroy()  # closes the AdvancedEditorTools (destructor pretty much)

    def _preview_edits_on_image(self, event):
        if self.displaying_processed_image:
            self.update_displayed_image(self.original_image)
            self.displaying_processed_image = False
        else:
            self.update_displayed_image(self.processing_image)
            self.displaying_processed_image = True

    def _cancel_edits_to_image(self, event):
        self.update_displayed_image(self.original_image)
        self.destroy()
