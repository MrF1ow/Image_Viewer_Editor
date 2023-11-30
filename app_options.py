from tkinter import Frame, Button, LEFT, Menu, Label, Scale, Toplevel
from file_manager import FileManager
from image_properties import ImageProperties
from settings import Settings
import cv2
import time


class AppOptions(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master=master, bg="#6b6b6b")

        self.file_options_button = Button(
            self, text="File", command=self._show_file_menu)
        self.file_options_button.pack(side=LEFT)

        self.file_menu = Menu(self, tearoff=0)
        self.file_menu.add_command(label="New", command=self.new_button_click)
        self.file_menu.add_command(
            label="Save", command=self.save_button_click)
        self.file_menu.add_command(
            label="Save As", command=self.save_as_button_click)

        self.edit_options_button = Button(
            self, text="Edit", command=self._show_edit_menu)
        self.edit_options_button.pack(side=LEFT)

        self.edit_menu = Menu(self, tearoff=0)
        self.edit_menu.add_command(
            label="Batch Processing", command=self.batch_processing_button_click)

        # SETTINGS
        # Creating the instance of Settings.
        self.settings = Settings(master=master)
        self.settings_menu_button = Button(
            self, text="Settings", command=self._show_settings_menu)
        self.settings_menu_button.pack(side="left")

    def _show_file_menu(self, event=None):
        self.file_menu.post(self.file_options_button.winfo_rootx(
        ), self.file_options_button.winfo_rooty() + self.file_options_button.winfo_height())

    def _show_edit_menu(self, event=None):
        self.edit_menu.post(self.edit_options_button.winfo_rootx(
        ), self.edit_options_button.winfo_rooty() + self.edit_options_button.winfo_height())

    def _show_settings_menu(self, event=None):
        self.settings.toggle_visibility()

    def new_button_click(self, event=None):
        fm = FileManager()
        fm.get_file()

        if fm.file is not None:
            self.master.file_location = fm.file
            image = cv2.imread(fm.file)
            self.master.master.original_image = image.copy()
            self.master.master.processed_image = image.copy()
            self.master.master.image_properties = ImageProperties()
            self._set_dimensions_of_image(image)
            self._insert_into_history(image)
            self.master.master.image_viewer._reset()
            self.master.master.image_viewer.display_image(image)

    def _set_dimensions_of_image(self, img=None):
        image = img
        height, width = image.shape[:2]
        self.master.master.image_properties.original_image_height = height
        self.master.master.image_properties.original_image_width = width
        self.master.master.image_properties.altered_image_height = height
        self.master.master.image_properties.altered_image_width = width
        self.master.master.image_properties.resize_image_height = height
        self.master.master.image_properties.resize_image_width = width

    def save_button_click(self, event=None):
        fm = FileManager()
        path = self.master.file_location
        fm.find_file(path)

        if fm.file is not None:
            fm.save_file(self.master.master.processed_image)

    def save_as_button_click(self, event=None):
        fm = FileManager()
        path = self.master.file_location
        fm.find_file(path)

        if fm.file is not None:
            fm.save_as_file(self.master.master.processed_image)

    def batch_processing_button_click(self, event=None):
        fm = FileManager()
        fm.get_files()

        if fm.batch_files is not None:
            for i in fm.batch_files:
                self.master.file_location = i
                image = cv2.imread(i)

                self.master.master.original_image = image.copy()
                self.master.master.processed_image = image.copy()
                height, width, channels = image.shape
                self.master.master.image_properties.original_image_height = height
                self.master.master.image_properties.original_image_height = width
                self.master.master.image_properties.altered_image_height = height
                self.master.master.image_properties.altered_image_width = width
                self.master.master.editor_options.original_image = image.copy()

                self.master.master.image_viewer._apply_all_edits()

                fm = FileManager()
                path = self.master.file_location
                fm.find_file(path)

                if fm.file is not None:
                    fm.save_file(self.master.master.processed_image)

    # Allows the user to set the current filters on the image as the default fitlers applied to all images.

    def _set_current_filters_as_default(self):
        # call a function that applys all the current self.master.master.image_properties values to a config file
        print("Default values updates")

    def _show_zoom_slider(self):
        # Creating the Zoom slider windo.
        zoom_slider_window = Toplevel(self)
        zoom_slider_window.title("Change Zoom Percentage")

        # Initial Zoom value for the zoom scale. THIS VALUE SHOULD BE SET BASED ON THE CONFIG FILE ONCE THAT IS CREATED.
        self.current_default_zoom_percentage = 10

        # Creating the scale and specifying its attributes.
        zoom_scale = Scale(zoom_slider_window, from_=10, to_=150,
                           orient="horizontal", label="Zoom Percentage", resolution=10)
        # Sets the initial Zoom value of the scale.
        zoom_scale.set(self.current_default_zoom_percentage)
        zoom_scale.pack()

        # Creating a reset button for the scale.
        # Using Lambda function to set the zoom scale to a dfault value and destroy the window.
        # Once we have the config file, this value will not merely be 10. It will be the users default value from past use.
        reset_button = Button(zoom_slider_window, text="Reset", command=lambda: [
                              zoom_scale.set(10), zoom_slider_window.destroy()])
        reset_button.pack(side="right")

        # Creating an apply button for the scale.
        # Using Lambda function to print the current zoom value (for testing purposed) and close the window. Once the config file is created, we may need a full function to update the config file. To be determined!
        # Using lambda function to create a reference to the function to avoid errors in the function being called when the button is corrected instead of when the button is clicked.
        apply_button = Button(zoom_slider_window, text="Apply", command=lambda: self._apply_new_default_zoom_percentage(
            zoom_scale, zoom_slider_window))
        apply_button.pack(side="right")

    # This function saves the new zoom percentage and destroys the window when the user applys the zoom slider.
    def _apply_new_default_zoom_percentage(self, zoom_scale, zoom_slider_window):
        print(zoom_scale.get())  # Printing for testing.
        # FAKE VARIABLE; use a real one when the config file is created.
        # Setting the value in the config file to the new scale value.
        configFileDefaultZoom = zoom_scale.get()
        zoom_slider_window.destroy()  # Destroying the window

    def _insert_into_history(self, img=None):
        image = img
        height, width = image.shape[:2]
        # Inserts the current self.master.master.image_properties into the history array
        title = "File Imported"
        import_instance = ImageProperties(
            title=title,
            time=str(time.strftime('%H:%M:%S')),
            is_flipped_horz=self.master.master.image_properties.is_flipped_horz,
            is_flipped_vert=self.master.master.image_properties.is_flipped_vert,
            is_grayscaled=self.master.master.image_properties.is_grayscaled,
            is_sepia=self.master.master.image_properties.is_sepia,
            is_cropped=self.master.master.image_properties.is_cropped,
            original_image_height=height,
            original_image_width=width,
            altered_image_height=height,
            altered_image_width=width,
            resize_image_height=height,
            resize_image_width=width,
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
        self.master.master.history.append(import_instance)
        self.master.master.history_of_edits._set_indices()
        self.master.master.history_of_edits.update_history_list()

    def _reset_all_edits(self):
        # Resets all edits to the original image
        self.master.master.processed_image = self.master.master.original_image
        self.master.master.image_viewer.display_image(
            self.master.master.processed_image)
        self.master.master.editor_options.reset_all_edits()
        self.master.master.editor_options.display_image(
            self.master.master.processed_image)
        self.master.master.image_properties = self.master.master.image_properties()
