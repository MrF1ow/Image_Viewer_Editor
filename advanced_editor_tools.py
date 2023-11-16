from tkinter import Toplevel, Label, Scale, TOP, HORIZONTAL, Button, RIGHT, LEFT, BOTTOM
from PIL import Image, ImageTk, ImageFilter
from image_properties import ImageProperties
import cv2
import time


class AdvancedEditorTools(Toplevel):
    def __init__(self, master=None):
        Toplevel.__init__(self, master=master)

        self.original_image = self.master.master.original_image
        self.processing_image = self.master.master.processed_image
        self.pre_image_properties = ImageProperties()
        self.displaying_processed_image = True
        self.history_arr = self.master.master.history

        # slider with range of -1 to 1
        # the command parameter is used to select a function that will be called everytime there is a change in the value of the slider
        self.brightness_scale = Scale(self, from_=0, to_=100, length=250,
                                      resolution=5, orient=HORIZONTAL, command=self._show_editor_tools)
        self.brightness_label = Label(self, text="Brightness")

        self.contrast_scale = Scale(self, from_=0, to_=100, length=250,
                                    resolution=5, orient=HORIZONTAL, command=self._show_editor_tools)
        self.contrast_label = Label(self, text="Contrast")

        self.blur_scale = Scale(self, from_=0, to_=100, length=250,
                                resolution=5, orient=HORIZONTAL, command=self._show_editor_tools)
        self.blur_label = Label(self, text="Blur")

        self.hue_scale = Scale(self, from_=0, to_=100, length=250,
                               resolution=5, orient=HORIZONTAL, command=self._show_editor_tools)
        self.hue_label = Label(self, text="Hue")

        self.saturation_scale = Scale(self, from_=0, to_=100, length=250,
                                      resolution=5, orient=HORIZONTAL, command=self._show_editor_tools)
        self.saturation_label = Label(self, text="Saturation")

        self.apply_button = Button(
            self, text="Apply", command=self._confirm_edits_to_image)

        self.cancel_button = Button(self, text="Cancel")
        self.cancel_button.bind("<ButtonRelease>", self._cancel_edits_to_image)

        self.preview_button = Button(self, text="Preview")
        self.preview_button.bind(
            "<ButtonRelease>", self._preview_edits_on_image)

        self.clear_button = Button(self, text="Clear")
        self.clear_button.bind("<ButtonRelease>", self._clear_edits_to_image)

        # set the initial value of the scales to the current value of the image
        self._set_scale_values()

        # this is how they are structured on the popup
        self.brightness_label.pack()
        self.brightness_scale.pack()
        self.contrast_label.pack()
        self.contrast_scale.pack()
        self.blur_label.pack()
        self.blur_scale.pack()
        # cannot change hue or saturation if the image is grayscaled
        if ImageProperties.is_grayscaled == False:
            self.hue_label.pack()
            self.hue_scale.pack()
            self.saturation_label.pack()
            self.saturation_scale.pack()

        self.preview_button.pack(side=LEFT)
        self.cancel_button.pack(side=LEFT)
        self.apply_button.pack(side=LEFT)
        self.clear_button.pack(side=LEFT)

    def _convert_brightness(self, num):
        return num * 2.54 - 127

    def _convert_contrast(self, num):
        return num * 0.02

    # need to fix conversion
    def _convert_saturation(self, num):
        return int(num * 2.55)

    def _convert_hue(self, num):
        return int(num * 3.58 - 179)

    def _show_editor_tools(self, event):

        self._change_brightness_value(event)
        self._change_contrast_value(event)
        self._change_blur_value(event)
        self._change_hue_value(event)
        self._change_saturation_value(event)

        self._update_image_property_values()

    def _change_blur_value(self, event):
        ImageProperties.blur = self.blur_scale.get()

    def _change_hue_value(self, event):
        ImageProperties.hue = self.hue_scale.get()

    def _change_saturation_value(self, event):
        ImageProperties.saturation = self.saturation_scale.get()

    def _change_brightness_value(self, event):
        ImageProperties.brightness = self.brightness_scale.get()

    def _change_contrast_value(self, event):
        ImageProperties.contrast = self.contrast_scale.get()

    def _apply_blur_to_image(self, img=None):
        image=img
        # this is how distorted each pixel will become
        kernel_size = (ImageProperties.blur, ImageProperties.blur)
        # the kernel size had to be a positive, ODD number
        kernel_size = tuple(size + 1 if size %
                            2 == 0 else size for size in kernel_size)
        # applies the actual blur
        image = cv2.blur(img, kernel_size)
        return image

    def _apply_hue_to_image(self, img=None):
        image=img
        hue_value = self._convert_hue(ImageProperties.hue)
        # Convert image to HSV
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        # Change the hue channel
        # Hue values range from 0 to 179
        hsv_image[:, :, 0] = (hsv_image[:, :, 0] + hue_value) % 180

        # Convert back to BGR
        image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)
        return image

    def _apply_saturation_to_image(self, img=None):
        image = img
        saturation_value = self._convert_saturation(ImageProperties.saturation)
        # Convert image to HSV
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Saturation values range 0 - 255
        hsv_image[:, :, 1] += saturation_value

        # Convert back to BGR
        image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)
        return image

    def _apply_brightness_and_contrast_to_image(self, img=None):
        image = img
        brightness_factor = self._convert_brightness(ImageProperties.brightness)
        contrast_factor = self._convert_contrast(ImageProperties.contrast)
        # applies the actual brightness change
        image = cv2.convertScaleAbs(image, alpha=contrast_factor, beta=brightness_factor)
        return image

        # this function actually sets the newly processed imaged as the image of the application
    def _confirm_edits_to_image(self):
        self.destroy()  # closes the AdvancedEditorTools (destructor pretty much)

    def _preview_edits_on_image(self, event):
        if self.displaying_processed_image:
            self.master.master.image_viewer.display_image(self.original_image)
            self.displaying_processed_image = False
        else:
            self.master.master.image_viewer.display_image(self.processing_image)
            self.displaying_processed_image = True

    def _cancel_edits_to_image(self, event):
        self._reset_advanced_image_properties()
        self._update_image_property_values()
        self.destroy()

    def _clear_edits_to_image(self, event):
        self._reset_advanced_image_properties()
        self._set_scale_values()
        self._update_image_property_values()

    def _reset_advanced_image_properties(self):
        ImageProperties.brightness = self.pre_image_properties.brightness
        ImageProperties.contrast = self.pre_image_properties.contrast
        ImageProperties.saturation = self.pre_image_properties.saturation
        ImageProperties.blur = self.pre_image_properties.blur
        ImageProperties.hue = self.pre_image_properties.hue

    def _set_scale_values(self):
        self.brightness_scale.set(ImageProperties.brightness)
        self.blur_scale.set(ImageProperties.blur)
        self.hue_scale.set(ImageProperties.hue)
        self.contrast_scale.set(ImageProperties.contrast)
        self.saturation_scale.set(ImageProperties.saturation)

    def _apply_all_advanced_edits(self, img=None):
        image = img
        image = self._apply_blur_to_image(image)
        image = self._apply_brightness_and_contrast_to_image(image)
        if ImageProperties.is_grayscaled == False:
            image = self._apply_hue_to_image(image)
            image = self._apply_saturation_to_image(image)

        self.processing_image = image

        return image

    def _update_image_property_values(self):
        self.master.master.image_viewer._apply_all_edits()

    def _insert_into_history(self, property_name, scale):
        new_value = scale.get()
        setattr(ImageProperties, property_name, new_value)
        title = f"{property_name.capitalize()} Changed to {new_value}"
        edit_instance = ImageProperties(
            title=title,
            time=str(time.strftime('%H:%M:%S')),
             **{property_name: new_value}
        )
        self.history_arr.append(edit_instance)
        self.master.master.history_of_edits.update_history_listbox()
