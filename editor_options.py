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

                # Create a frame for buttons
        self.button_frame = Frame(self, bg="#6b6b6b")
        self.button_frame.grid(row=0, column=0, rowspan=4, padx=5, pady=2, sticky="nsew")

        # Create buttons with image icons and place them in the button_frame
        self.advanced_edits_button = Button(
            self.button_frame, text="Advanced", width=button_width, height=button_height, command=self._open_advanced_edits)
        self.advanced_edits_button.grid(row=0, column=0, padx=5, pady=2, sticky="w")

        self.crop_button = Button(self.button_frame, text="Crop", width=button_width, height=button_height)
        self.crop_button.bind("<ButtonRelease>", self._initiate_crop_mode)
        self.crop_button.grid(row=0, column=1, padx=5, pady=2, sticky='e')

        self.horz_flip_button = Button(
            self.button_frame, text="Horz Flip", width=button_width, height=button_height, command=self._change_horizontal_flip_value)
        self.horz_flip_button.grid(row=1, column=0, padx=5, pady=2, sticky="w")

        self.vert_flip_button = Button(
            self.button_frame, text="Vert Flip", width=button_width, height=button_height, command=self._change_vertical_flip_value)
        self.vert_flip_button.grid(row=1, column=1, padx=5, pady=2, sticky="e", columnspan=2)

        self.rotate_button = Button(
            self.button_frame, text="Rotate", width=button_width, height=button_height, command=self._change_rotation_value)
        self.rotate_button.grid(row=2, column=0, padx=5, pady=2, sticky="w", columnspan=2)

        self.resize_button = Button(
            self.button_frame, text="Resize", width=button_width, height=button_height, command=self._open_resize_window)
        self.resize_button.grid(row=2, column=1, padx=5, pady=2, sticky="e")

        self.apply_grayscale = Button(
            self.button_frame, text="GrayScale", width=button_width, height=button_height, command=self._change_grayscale_value)
        self.apply_grayscale.grid(row=3, column=0, padx=5, pady=2, sticky="w", columnspan=2)

        self.apply_sepia = Button(
            self.button_frame, text="Sepia", width=button_width, height=button_height, command=self._change_sepia_value)
        self.apply_sepia.grid(row=3, column=1, padx=5, pady=2, sticky="e", columnspan=2)

        self.clear_all_button = Button(
            self.button_frame, text="Clear All", width=button_width * 2 + 5, height=button_height, command=self._clear_all_edits_to_image)
        self.clear_all_button.grid(row=4, column=0, padx=5, pady=2, sticky="we", columnspan=2)


        # New frame for metadata labels
        self.metadata_frame = Frame(self, bg="#6b6b6b", width=15, highlightthickness=1, highlightbackground="white")
        self.metadata_frame.grid(row=7, column=0, padx=1, pady=2, sticky="nsew")

        # Labels for displaying image metadata
        self.size_label = Label(self.metadata_frame, text="Size: ", bg="#6b6b6b", fg="white")
        self.resolution_label = Label(self.metadata_frame, text="Resolution: ", bg="#6b6b6b", fg="white")
        self.filename_label = Label(self.metadata_frame, text="File Name: ", bg="#6b6b6b", fg="white")
        self.extension_label = Label(self.metadata_frame, text="Extension: ", bg="#6b6b6b", fg="white")
        self.bytes_per_pixel_label = Label(self.metadata_frame, text="Bytes per Pixel: ", bg="#6b6b6b", fg="white")
        self.zoom_resolution_label = Label(self.metadata_frame, text="Zoomed-in Resolution: ", bg="#6b6b6b", fg="white")

        # Packing labels in the metadata frame
        self.size_label.grid(row=0, column=0, padx=5, pady=1, sticky="w")
        self.resolution_label.grid(row=1, column=0, padx=5, pady=1, sticky="w")
        self.filename_label.grid(row=2, column=0, padx=5, pady=1, sticky="w")
        self.extension_label.grid(row=3, column=0, padx=5, pady=1, sticky="w")
        self.bytes_per_pixel_label.grid(row=4, column=0, padx=5, pady=1, sticky="w")
        self.zoom_resolution_label.grid(row=5, column=0, padx=5, pady=1, sticky="w")

    def _open_advanced_edits(self):
        # initializes the AdvancedEditorTools
        self.master.master._switch_crop_to_off()
        self.master.master.advanced_tools = AdvancedEditorTools(
            master=self.master)
        self.master.master.advanced_tools.grab_set()

    def _change_vertical_flip_value(self):
        self.master.master._switch_crop_to_off()
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
        self.master.master._switch_crop_to_off()
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
        self.master.master._switch_crop_to_off()
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
        self.master.master._switch_crop_to_off()
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
        self.master.master._switch_crop_to_off()
        if self.master.master.image_properties.rotation == 360:
            self.master.master.image_properties.rotation = 0
        self.master.master.image_properties.rotation += 90
        title = "Rotation Applied"

        self._insert_into_history(
            title=title)

        self.update_displayed_image()

    def _reset_basic_image_properties(self):
        self.master.master.image_properties.is_flipped_horz = False
        self.master.master.image_properties.is_flipped_vert = False
        self.master.master.image_properties.is_grayscaled = False
        self.master.master.image_properties.is_sepia = False
        self.master.master.image_properties.is_cropped = False
        self.master.master.image_properties.rotation = 0
        self.master.master.image_properties.altered_image_height = self.master.master.image_properties.original_image_height
        self.master.master.image_properties.altered_image_width = self.master.master.image_properties.original_image_width
        self.master.master.image_properties.resize_image_height = self.master.master.image_properties.original_image_height
        self.master.master.image_properties.resize_image_width = self.master.master.image_properties.original_image_width
        self.master.master.image_properties.crop_start_x = 0
        self.master.master.image_properties.crop_start_y = 0
        self.master.master.image_properties.crop_end_x = 0
        self.master.master.image_properties.crop_end_y = 0
        self.master.master.image_properties.crop_ratio = 0
        self.master.master.image_properties.crop_rectangle_width = 0
        self.master.master.image_properties.crop_rectangle_height = 0

    def _reset_advanced_image_properties(self):
        self.master.master.image_properties.brightness = 50
        self.master.master.image_properties.contrast = 50
        self.master.master.image_properties.saturation = 0
        self.master.master.image_properties.blur = 0
        self.master.master.image_properties.hue = 0

    def _clear_all_edits_to_image(self):
        self.master.master._switch_crop_to_off()
        self._reset_basic_image_properties()
        self._reset_advanced_image_properties()
        title = "Cleared All Edits"
        self._insert_into_history(title)
        self.update_displayed_image()

    def _open_resize_window(self):
        self.master.master._switch_crop_to_off()
        MAXIMUM_SIZE = 7680
        MINIMUM_SIZE = 1

        def _in_range(value):
            if MINIMUM_SIZE <= value <= MAXIMUM_SIZE:
                return True
            return False

        def _change_resize_values():
            self.master.master.image_properties.is_resized = True
            self.master.master.image_properties.resize_image_width = int(
                width.get())
            self.master.master.image_properties.resize_image_height = int(
                height.get())
            title = f"Resize: {self.master.master.image_properties.resize_image_width}x{self.master.master.image_properties.resize_image_height}"
            image_was_resized = False
            if _in_range(int(width.get())):
                self.master.master.image_properties.resize_image_width = int(
                    width.get())
                image_was_resized = True
            if _in_range(int(height.get())):
                self.master.master.image_properties.resize_image_height = int(
                    height.get())
                image_was_resized = True

            if image_was_resized:
                title = f"Resize: {self.master.master.image_properties.resize_image_width}x{self.master.master.image_properties.resize_image_height}"

                self._insert_into_history(title)

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
            is_resized=self.master.master.image_properties.is_resized,
            original_image_height=self.master.master.image_properties.original_image_height,
            original_image_width=self.master.master.image_properties.original_image_width,
            altered_image_height=self.master.master.image_properties.altered_image_height,
            altered_image_width=self.master.master.image_properties.altered_image_width,
            resize_image_height=self.master.master.image_properties.resize_image_height,
            resize_image_width=self.master.master.image_properties.resize_image_width,
            zoom_scale_factor=self.master.master.image_properties.zoom_scale_factor,
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
            crop_ratio=self.master.master.image_properties.crop_ratio,
            crop_rectangle_width=self.master.master.image_properties.crop_rectangle_width,
            crop_rectangle_height=self.master.master.image_properties.crop_rectangle_height,
            at_time_canvas_width=self.master.master.image_properties.at_time_canvas_width,
            at_time_canvas_height=self.master.master.image_properties.at_time_canvas_height,
            pan_start_x=self.master.master.image_properties.pan_start_x,
            pan_start_y=self.master.master.image_properties.pan_start_y,
            pan_coord_x=self.master.master.image_properties.pan_coord_x,
            pan_coord_y=self.master.master.image_properties.pan_coord_y
        )
        return edit_instance

    def update_metadata_labels(self, file_size, resolution, file_name, file_extension, bytes_per_pixel, zoom_resolution):
        self.size_label.config(text=f"Size: {file_size} Bytes ")
        self.resolution_label.config(text=f"Resolution: {resolution[1]} x {resolution[0]}")
        self.filename_label.config(text=f"File Name: {file_name} ")
        self.extension_label.config(text=f"Extension: {file_extension} ")
        self.bytes_per_pixel_label.config(text=f"Color Depth: {bytes_per_pixel} Bytes ")
        self.zoom_resolution_label.config(text=f"Zoomed-in Resolution: {zoom_resolution[1]} x {zoom_resolution[0]} ")
