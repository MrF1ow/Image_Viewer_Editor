import numpy as np
import time
from tkinter import Frame, Button, Toplevel, Label, Button, Entry, NW
from PIL import Image, ImageTk
from image_properties import ImageProperties
from advanced_editor_tools import AdvancedEditorTools
import cv2


class EditorOptions(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master=master, bg="#6b6b6b")

        # Set a common width and height for the buttons
        button_width = 10
        button_height = 5

        self.history_arr = self.master.master.history

        # Create buttons with image icons
        self.advanced_edits_button = Button(
            self, text="Advanced", width=button_width, height=button_height, command=self._open_advanced_edits)
        self.advanced_edits_button.grid(
            row=0, column=0, padx=5, pady=5, sticky="w")

        self.horz_flip_button = Button(self, text="Horz Flip", width=button_width,
                                       height=button_height, command=self._change_horizontal_flip_value)
        self.horz_flip_button.grid(row=0, column=1, padx=5, pady=5, sticky="e")

        self.vert_flip_button = Button(self, text="Vert Flip", width=button_width,
                                       height=button_height, command=self._change_vertical_flip_value)
        self.vert_flip_button.grid(
            row=1, column=0, padx=5, pady=5, sticky="sw", columnspan=2)

        self.rotate_button = Button(self, text="Rotate", width=button_width,
                                    height=button_height, command=self._change_rotation_value)
        self.rotate_button.grid(row=1, column=1, padx=5,
                                pady=5, sticky="se", columnspan=2)

        self.resize_button = Button(
            self, text="Resize", width=button_width, height=button_height, command=self._open_resize_window)
        self.resize_button.grid(row=2, column=0, padx=5, pady=5, sticky="w")

        self.apply_grayscale = Button(self, text="GrayScale", width=button_width,
                                      height=button_height, command=self._change_grayscale_value)
        self.apply_grayscale.grid(
            row=2, column=1, padx=5, pady=5, sticky="nw", columnspan=2)

        self.apply_sepia = Button(self, text="Sepia", width=button_width,
                                  height=button_height, command=self._change_sepia_value)
        self.apply_sepia.grid(row=3, column=0, padx=5,
                              pady=5, sticky="nw", columnspan=2)

        self.crop_button = Button(
            self, text="Crop", width=button_width, height=button_height)
        self.crop_button.bind("<ButtonRelease>", self._initiate_crop_mode)
        self.crop_button.grid(row=3, column=1, padx=5,
                              pady=5, sticky='e', columnspan=2)

        self.clear_all_button = Button(self, text="Clear All", width=button_width,
                                       height=button_height, command=self._clear_all_edits_to_image)
        self.clear_all_button.grid(
            row=4, column=0, padx=5, pady=5, sticky="w", columnspan=2)

    # this function opens the place where we are going to have all the sliders for our advanced editor tools

    def _open_advanced_edits(self):
        # initializes the AdvancedEditorTools
        self.master.master.advanced_tools = AdvancedEditorTools(
            master=self.master)
        self.master.master.advanced_tools.grab_set()

    def _change_vertical_flip_value(self):
        if self.master.master.image_properties.is_flipped_vert:
            # If it's flipped, revert back to the original
            self.master.master.image_properties.is_flipped_vert = False
        else:
            self.master.master.image_properties.is_flipped_vert = True

        title = "Flipped Vertically"

        self._insert_into_history(
            title=title)

        self.update_displayed_image()

    def _change_horizontal_flip_value(self):
        if self.master.master.image_properties.is_flipped_horz:
            # If it's flipped, revert back to the original
            self.master.master.image_properties.is_flipped_horz = False
        else:
            self.master.master.image_properties.is_flipped_horz = True

        title = "Flipped Horizontally"

        self._insert_into_history(
            title=title)

        self.update_displayed_image()

    def _change_grayscale_value(self):
        if self.master.master.image_properties.is_sepia == False:
            if self.master.master.image_properties.is_grayscaled:
                self.master.master.image_properties.is_grayscaled = False
                title = "Grayscale Removed"
            else:
                self.master.master.image_properties.is_grayscaled = True
                title = "Grayscale Applied"

            self._insert_into_history(
                title=title)

        self.update_displayed_image()

    def _change_sepia_value(self):
        if self.master.master.image_properties.is_grayscaled == False:
            if self.master.master.image_properties.is_sepia:
                self.master.master.image_properties.is_sepia = False
                title = "Sepia Removed"
            else:
                self.master.master.image_properties.is_sepia = True
                title = "Sepia Applied"

            self._insert_into_history(
                title=title)

        self.update_displayed_image()

    def _change_rotation_value(self):
        if self.master.master.image_properties.rotation == 360:
            self.master.master.image_properties.rotation = 0
        self.master.master.image_properties.rotation += 90
        title = "Rotation Applied"

        self._insert_into_history(
            title=title)

        self.update_displayed_image()

    def _apply_horizontal_flip_image(self, img=None):
        # Get the processed image from the master
        image = img
        # Convert the numpy array of pixels to a Pillow image
        image = Image.fromarray(image)

        # Check if the image is already horizontally flipped
        if self.master.master.image_properties.is_flipped_horz:
            flipped_image = image.transpose(method=Image.FLIP_LEFT_RIGHT)
        else:
            flipped_image = image

        # Convert the flipped image back to a numpy array
        numpy_image = np.array(flipped_image)
        return numpy_image

    def _apply_vertical_flip_image(self, img=None):
        # Get the processed image from the master
        image = img
        # Convert the numpy array of pixels to a Pillow image
        image = Image.fromarray(image)

        # Check if the image is already vertically flipped
        if self.master.master.image_properties.is_flipped_vert:
            flipped_image = image.transpose(method=Image.FLIP_TOP_BOTTOM)
        else:
            flipped_image = image

        # Convert the flipped image back to a numpy array
        numpy_image = np.array(flipped_image)
        return numpy_image

    def _apply_grayscale_to_image(self, img=None):
        image = img
        if self.master.master.image_properties.is_grayscaled:
            grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            grayscale_image = image
        return grayscale_image

    def _apply_sepia_to_image(self, img=None):
        image = img
        if self.master.master.image_properties.is_sepia:
            # Applying Sepia to the uploaded image.
            # Converting the image to a numpy array representing pixels.
            array_image = np.array(image, dtype=np.float64)
            sepia_filter = np.array([[0.272, 0.534, 0.131],
                                    [0.349, 0.686, 0.168],
                                    [0.393, 0.769, 0.189]])  # Sepia converter values (constants).
            # Performs dot prodcut with array_image and transposed sepia_filter. Also ensures valid range and data type for pixels.
            sepia_image = np.dot(array_image, sepia_filter.T).clip(
                0, 255).astype(np.uint8)
            # Converting the sepia_image into valid np array. Common step to ensure proper data type.
            sepia_image = np.array(sepia_image, dtype=np.uint8)
        else:
            sepia_image = image
        return sepia_image

    def _apply_rotation_to_image(self, img=None):
        image = img
        angle = self.master.master.image_properties.rotation
        # Convert the numpy array of pixels to a Pillow image
        image = Image.fromarray(image)

        # Rotate the image to degrees specified by the angle variable
        rotated_image = image.rotate(
            angle=angle, resample=Image.NEAREST, expand=True)
        # Convert the rotated image back to a numpy array
        numpy_image = np.array(rotated_image)

        resize_height = self.master.master.image_properties.resize_image_height
        resize_width = self.master.master.image_properties.resize_image_width

        if angle == 90 or angle == 270:
            self.master.master.image_properties.altered_image_height = resize_width
            self.master.master.image_properties.altered_image_width = resize_height
        elif angle == 180 or angle == 360 or angle == 0:
            self.master.master.image_properties.altered_image_height = resize_height
            self.master.master.image_properties.altered_image_width = resize_width

        return numpy_image

    def _apply_resize_to_image(self, img=None):
        image = img
        # print(f"In Resize Function Altered Height: {self.master.master.image_properties.altered_image_height}")
        # print(f"In Resize Function Altered Width: {self.master.master.image_properties.altered_image_width}")
        resized_image = cv2.resize(image, (self.master.master.image_properties.altered_image_width,
                                           self.master.master.image_properties.altered_image_height))

        return resized_image

    def _reset_basic_image_properties(self):
        self.master.master.image_properties.is_flipped_horz = False
        self.master.master.image_properties.is_flipped_vert = False
        self.master.master.image_properties.is_grayscaled = False
        self.master.master.image_properties.is_sepia = False
        self.master.master.image_properties.rotation = 0
        self.master.master.image_properties.altered_image_height = self.master.master.image_properties.original_image_height
        self.master.master.image_properties.altered_image_width = self.master.master.image_properties.original_image_width
        self.master.master.image_properties.resize_image_height = self.master.master.image_properties.original_image_height
        self.master.master.image_properties.resize_image_width = self.master.master.image_properties.original_image_width

    def _reset_advanced_image_properties(self):
        self.master.master.image_properties.brightness = 50
        self.master.master.image_properties.contrast = 50
        self.master.master.image_properties.saturation = 0
        self.master.master.image_properties.blur_size = 0
        self.master.master.image_properties.hue = 0

    def _clear_all_edits_to_image(self):
        self._reset_basic_image_properties()
        self._reset_advanced_image_properties()
        self.history_arr.clear()
        self.master.master.history_of_edits.update_history_list()
        self.update_displayed_image()

    def _open_resize_window(self):

        def _change_resize_values():
            self.master.master.image_properties.resize_image_width = int(
                width.get())
            self.master.master.image_properties.resize_image_height = int(
                height.get())
            title = f"Resize: {self.master.master.image_properties.altered_image_width}x{self.master.master.image_properties.altered_image_height}"

            self._insert_into_history(
                title=title)

            self.update_displayed_image()
            resize_window.destroy()

        resize_window = Toplevel(self)
        resize_window.title("Resize Image")

        Label(resize_window, text="Width").pack()
        width = Entry(resize_window)
        width.insert(
            0, str(self.master.master.image_properties.altered_image_width))
        width.pack()
        Label(resize_window, text="Height").pack()
        height = Entry(resize_window)
        height.insert(
            0, str(self.master.master.image_properties.altered_image_height))
        height.pack()
        Button(resize_window, text="Apply Resize",
               command=_change_resize_values).pack()

    def update_displayed_image(self):
        self.master.master.image_viewer._apply_all_edits()

    def _initiate_crop_mode(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.crop_button:
            if self.master.master.in_crop_mode:
                self.master.master.image_viewer._deactive_crop_mode(event)
            else:
                self.master.master.image_viewer._active_crop_mode(event)

    def _apply_all_basic_edits(self, img=None):
        image = img
        image = self._apply_rotation_to_image(image)
        image = self._apply_resize_to_image(image)
        image = self._apply_grayscale_to_image(image)
        image = self._apply_horizontal_flip_image(image)
        image = self._apply_vertical_flip_image(image)
        image = self._apply_sepia_to_image(image)

        return image

    def _check_undo_performed(self):
        if self.master.master.undo_performed:
            self.master.master.history_of_edits._clear_after_edit()

    def _insert_into_history(self, title):
        """
        Inserts a new edit instance into the history array and updates the history listbox.

        Args:
            title (str): Title for the edit instance.
            property_name (str): Name of the property to be updated in self.master.master.image_properties.
            new_value (any): New value to be set for the specified property.

        Returns:
            None
        """
        edit_instance = self._make_edit_instance(title)
        # print(f"Edit Instance Altered Height: {edit_instance.altered_image_height}")
        # print(f"Edit Instance Altered Width: {edit_instance.altered_image_width}")
        self._check_undo_performed()
        self.master.master.history.append(edit_instance)
        self.master.master.history_of_edits.update_history_list()
        self.master.master.history_of_edits._set_indices()

    def _make_edit_instance(self, title):
        """
        Creates an edit instance with the current self.master.master.image_properties values.
        """
        edit_instance = ImageProperties(
            title=title,
            time=str(time.strftime('%H:%M:%S')),
            is_flipped_horz=self.master.master.image_properties.is_flipped_horz,
            is_flipped_vert=self.master.master.image_properties.is_flipped_vert,
            is_grayscaled=self.master.master.image_properties.is_grayscaled,
            is_sepia=self.master.master.image_properties.is_sepia,
            is_cropped=self.master.master.image_properties.is_cropped,
            original_image_height=self.master.master.image_properties.original_image_height,
            original_image_width=self.master.master.image_properties.original_image_width,
            altered_image_height=self.master.master.image_properties.altered_image_height,
            altered_image_width=self.master.master.image_properties.altered_image_width,
            resize_image_height=self.master.master.image_properties.resize_image_height,
            resize_image_width=self.master.master.image_properties.resize_image_width,
            rotation=self.master.master.image_properties.rotation,
            brightness=self.master.master.image_properties.brightness,
            contrast=self.master.master.image_properties.contrast,
            saturation=self.master.master.image_properties.saturation,
            blur=self.master.master.image_properties.blur,
            hue=self.master.master.image_properties.hue,
            crop_start_x=self.master.master.image_properties.crop_start_x,
            crop_start_y=self.master.master.image_properties.crop_start_y,
            crop_end_x=self.master.master.image_properties.crop_end_x,
            crop_end_y=self.master.master.image_properties.crop_end_y,
            crop_ratio=self.master.master.image_properties.crop_ratio
        )
        return edit_instance

