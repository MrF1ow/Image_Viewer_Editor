from tkinter import Frame, Canvas, CENTER
from PIL import Image, ImageTk
import cv2
import math
from tkinter import Frame, Button, Toplevel, Label, Button, Entry
from edit_functions import AllEditFunctions
from image_properties import ImageProperties
import time
import numpy as np


class ImageManager(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master=master, bg="black",
                       width=720, height=405)

        self.current_image = None  # store currently displayed image
        self.crop_start_x = 0
        self.crop_start_y = 0
        self.crop_end_x = 0
        self.crop_end_y = 0
        self.rectangle_id = 0
        self.ratio = 0

        self.scale_factor = 1.0
        self.canvas_width = 1440
        self.canvas_height = 810
        self.canvas_ratio_x = 0
        self.canvas_ratio_y = 0
        self.original_canvas_width = 1440
        self.original_canvas_height = 810

        # inside of the frame, make a canvas for image using the 'Canvas' widget (look it up)
        self.canvas = Canvas(self, bg="black",  width=self.canvas_width,
                             height=self.canvas_height, highlightthickness=0)

        # center the image
        self.canvas.place(relx=0.5, rely=0.5, anchor="center")
        self.canvas.config(scrollregion=(
            0, 0, self.canvas_width, self.canvas_height))

        # Starting coordinates for panning
        self.start_x = 0
        self.start_y = 0
        self.coord_x = 0
        self.coord_y = 0

        # Binding for panning
        self.canvas.bind("<ButtonPress-1>", self._activate_pan)
        self.canvas.bind("<B1-Motion>", self._pan_image)

        # Arroow key bindings for panning
        self.master.master.bind("<Left>", self._pan_left)
        self.master.master.bind("<Right>", self._pan_right)
        self.master.master.bind("<Up>", self._pan_up)
        self.master.master.bind("<Down>", self._pan_down)

        # Canvas reset button for zoom and pan
        button_width = 5
        button_height = 2
        self.pan_reset_button = Button(
            self, text="Reset", width=button_width, height=button_height, command=self._reset)
        self.pan_reset_button.pack(anchor="sw", side="left", padx=5, pady=5)

        # Zoom functionality
        self.scale_factor = 1.0

    def display_image(self, img=None):
        self.clear_canvas()
        if img is None:
            # this uses the processed image if none is given
            image = self.master.master.processed_image.copy()
        else:
            image = img

        zoom = self.master.master.image_properties.is_zoomed

        # use openCV to convert the image from BGR to RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        height, width = image.shape[:2]
        ratio = height / width

        self.master.master.image_properties.altered_image_height = height
        self.master.master.image_properties.altered_image_width = width

        new_height = height
        new_width = width

        # need to check if the image size is bigger than the frame
        if height > self.original_canvas_width or width > self.original_canvas_height:
            if ratio < 1:
                new_width = self.winfo_width()
                new_ratio = new_width / width
                new_height = int(new_height * new_ratio)
            else:
                new_height = self.winfo_height()
                new_width = int(math.floor(new_height * (width / height)))
        # For zoom functionality
        if zoom:
            size = int(
                new_width * self.scale_factor), int(new_height * self.scale_factor)
            self.current_image = cv2.resize(image, size)
            self.master.master.image_properties.zoom_image_height = size[1]
            self.master.master.image_properties.zoom_image_width = size[0]
        else:
            self.current_image = cv2.resize(image, (new_width, new_height))

        self.current_image = ImageTk.PhotoImage(
            Image.fromarray(self.current_image))

        self.ratio = height / new_height

        # self.canvas.config(width=new_width, height=new_height)
        canvas_center_x = self.canvas_width / 2
        canvas_center_y = self.canvas_height / 2

        image_center_x = canvas_center_x - new_width / 2
        image_center_y = canvas_center_y - new_height / 2

        self.canvas.create_image(
            image_center_x, image_center_y, anchor="nw", image=self.current_image)

        self.canvas.move("all", self.master.master.image_properties.pan_coord_x,
                         self.master.master.image_properties.pan_coord_y)

        self.canvas_ratio_y = self.canvas_height / new_height
        self.canvas_ratio_x = self.canvas_width / new_width
        # Finds the click location
    def _activate_pan(self, event):
        if self.master.master.in_crop_mode:
            return
        if self.master.master.original_image is None:
            return
        if self.master.master.processed_image is None:
            return

        self.start_x = event.x
        self.start_y = event.y

    def _pan_image(self, event):
        if self.master.master.in_crop_mode or self.master.master.original_image is None or self.master.master.processed_image is None:
            return

        dest_x = event.x - self.start_x
        dest_y = event.y - self.start_y

        # Get the bounding box of all elements on the canvas
        bbox = self.canvas.bbox("all")
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()


        if dest_x > 0:
            if bbox[2] + dest_x <= canvas_width:
                self.canvas.move("all", dest_x, 0)
                self.master.master.image_properties.pan_coord_x += dest_x
        else:
            if bbox[0] + dest_x >= 0:
                self.canvas.move("all", dest_x, 0)
                self.master.master.image_properties.pan_coord_x += dest_x

        if dest_y > 0:
            if bbox[3] + dest_y <= canvas_height:
                self.canvas.move("all", 0, dest_y)
                self.master.master.image_properties.pan_coord_y += dest_y
        else:
            if bbox[1] + dest_y >= 0:
                self.canvas.move("all", 0, dest_y)
                self.master.master.image_properties.pan_coord_y += dest_y

        self.start_x = event.x
        self.start_y = event.y

    # Functions for panning macros
    def _pan_left(self, event):
        current_x, current_y = self.canvas.coords("all")
        if current_x-(self.canvas.winfo_width()*.1) >= 0:
            self.canvas.move("all", -(self.canvas.winfo_width()*.1), 0)
            self.start_x -= (self.canvas.winfo_width()*.1)
            self.master.master.image_properties.pan_coord_x -= (
                self.canvas.winfo_width()*.1)
        if current_x-(self.canvas.winfo_width()*.1) < 0:
            self.canvas.move("all", -current_x, 0)
            self.start_x -= current_x
            self.master.master.image_properties.pan_coord_x -= current_x

    def _pan_right(self, event):
        # Get the bounding box of all elements on the canvas
        bbox = self.canvas.bbox("all")
        if bbox[2]+(self.canvas.winfo_width()*.1) <= self.canvas.winfo_width():
            self.canvas.move("all", +(self.canvas.winfo_width()*.1), 0)
            self.start_x += (self.canvas.winfo_width()*.1)
            self.master.master.image_properties.pan_coord_x += (
                self.canvas.winfo_width()*.1)
        if bbox[2]+(self.canvas.winfo_width()*.1) > self.canvas.winfo_width():
            self.canvas.move("all", self.canvas.winfo_width()-bbox[2], 0)
            self.start_x += self.canvas.winfo_width()-bbox[2]
            self.master.master.image_properties.pan_coord_x += self.canvas.winfo_width() - \
                bbox[2]

    def _pan_down(self, event):
        # Get the bounding box of all elements on the canvas
        bbox = self.canvas.bbox("all")
        if bbox[3]+(self.canvas.winfo_height()*.1) <= self.canvas.winfo_height():
            self.canvas.move("all", 0, +(self.canvas.winfo_height()*.1))
            self.start_y += (self.canvas.winfo_height()*.1)
            self.master.master.image_properties.pan_coord_y += (
                self.canvas.winfo_height()*.1)
        if bbox[3]+(self.canvas.winfo_height()*.1) > self.canvas.winfo_height():
            self.canvas.move("all", 0, self.canvas.winfo_height()-bbox[3])
            self.start_y += self.canvas.winfo_height()-bbox[3]
            self.master.master.image_properties.pan_coord_y += self.canvas.winfo_height() - \
                bbox[3]

    def _pan_up(self, event):
        current_x, current_y = self.canvas.coords("all")
        if current_y-(self.canvas.winfo_height()*.1) >= 0:
            self.canvas.move("all", 0, -(self.canvas.winfo_height()*.1))
            self.start_y -= (self.canvas.winfo_height()*.1)
            self.master.master.image_properties.pan_coord_y -= (
                self.canvas.winfo_height()*.1)
        if current_y-(self.canvas.winfo_height()*.1) < 0:
            self.canvas.move("all", 0, -current_y)
            self.start_y -= current_y
            self.master.master.image_properties.pan_coord_y -= current_y

    # Resets the pan coordinates
    def _reset(self):
        i = 0
        while i < 2:
            self.start_x = 0
            self.start_y = 0
            self.scale_factor = 1.0
            self.display_image()

            self.canvas_width = self.original_canvas_width
            self.canvas_height = self.original_canvas_height
            self.canvas.config(width=self.canvas_width,
                               height=self.canvas_height)

            self.canvas.move("all", -self.master.master.image_properties.pan_coord_x, -
                             self.master.master.image_properties.pan_coord_y)
            self.master.master.image_properties.pan_coord_x = 0
            self.master.master.image_properties.pan_coord_y = 0
            i += 1

    def _active_crop_mode(self, event):
        self.canvas.unbind("<ButtonPress-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.bind("<ButtonPress>", self._start_crop)
        self.canvas.bind("<B1-Motion>", self._update_crop)
        self.canvas.bind("<ButtonRelease>", self._end_crop)
        self.master.master.in_crop_mode = True

    def _deactive_crop_mode(self, event):
        self.canvas.unbind("<ButtonPress>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease>")
        self.master.master.in_crop_mode = False
        self.canvas.bind("<ButtonPress-1>", self._activate_pan)
        self.canvas.bind("<B1-Motion>", self._pan_image)

    def _start_crop(self, event):
        self.crop_start_x = event.x
        self.crop_start_y = event.y

    def _update_crop(self, event):
        if self.rectangle_id:
            self.canvas.delete(self.rectangle_id)

        self.crop_end_x = event.x
        self.crop_end_y = event.y

        self.rectangle_id = self.canvas.create_rectangle(self.crop_start_x, self.crop_start_y,
                                                         self.crop_end_x, self.crop_end_y, width=2, outline="red")

    def _set_crop_coordinates(self, start_x, start_y, end_x, end_y):
        self.master.master.image_properties.is_cropped = True
        self.master.master.image_properties.crop_start_x = start_x
        self.master.master.image_properties.crop_start_y = start_y
        self.master.master.image_properties.crop_end_x = end_x
        self.master.master.image_properties.crop_end_y = end_y
        self.master.master.image_properties.crop_ratio = self.ratio
        self.master.master.image_properties.altered_image_width = end_x - start_x
        self.master.master.image_properties.altered_image_height = end_y - start_y
        self.master.master.image_properties.resize_image_height = self.master.master.image_properties.altered_image_height
        self.master.master.image_properties.resize_image_width = self.master.master.image_properties.altered_image_width
        print(f"Altered Image Height: {self.master.master.image_properties.altered_image_height}, Altered Image Width: {self.master.master.image_properties.altered_image_width}")
        print(f"Resize Image Height: {self.master.master.image_properties.resize_image_height}, Resize Image Width: {self.master.master.image_properties.resize_image_width}")

    def _check_crop_coordinates(self):

        columns, rows = self.master.master.processed_image.shape[:2]
        image_height = columns
        image_width = rows
        pan_offset_x = self.master.master.image_properties.pan_coord_x
        pan_offset_y = self.master.master.image_properties.pan_coord_y
        canvas_height = self.canvas.winfo_height()
        canvas_width = self.canvas.winfo_width()

        top_left_x = (canvas_width - image_width) / 2 + pan_offset_x
        top_left_y = (canvas_height - image_height) / 2 + pan_offset_y

        bottom_left_x = top_left_x
        bottom_left_y = top_left_y + image_height

        bottom_right_x = top_left_x + image_width
        bottom_right_y = top_left_y + image_height

        top_right_x = top_left_x + image_width
        top_right_y = top_left_y

        print(f"Top Left: ({top_left_x}, {top_left_y})")
        print(f"Bottom Left: ({bottom_left_x}, {bottom_left_y})")
        print(f"Bottom Right: ({bottom_right_x}, {bottom_right_y})")
        print(f"Top Right: ({top_right_x}, {top_right_y})")

        if self.crop_start_x < top_left_x:
            self.crop_start_x = top_left_x
        if self.crop_start_y < top_left_y:
            self.crop_start_y = top_left_y
        if self.crop_end_x > bottom_right_x:
            self.crop_end_x = bottom_right_x
        if self.crop_end_y > bottom_right_y:
            self.crop_end_y = bottom_right_y

        if self.crop_start_x > top_right_x:
            self.crop_start_x = top_right_x
        if self.crop_start_y < top_right_y:
            self.crop_start_y = top_right_y
        if self.crop_end_x < bottom_left_x:
            self.crop_end_x = bottom_left_x
        if self.crop_end_y > bottom_left_y:
            self.crop_end_y = bottom_left_y

        self.crop_start_x = (self.crop_start_x - top_left_x) / self.scale_factor
        self.crop_start_y = (self.crop_start_y - top_left_y) / self.scale_factor
        self.crop_end_x = (self.crop_end_x - top_left_x) / self.scale_factor
        self.crop_end_y = (self.crop_end_y - top_left_y) / self.scale_factor

    def _end_crop(self, event):
        self._check_crop_coordinates()

        if self.crop_start_x <= self.crop_end_x and self.crop_start_y <= self.crop_end_y:
            start_x = int(self.crop_start_x * self.ratio)
            start_y = int(self.crop_start_y * self.ratio)
            end_x = int(self.crop_end_x * self.ratio)
            end_y = int(self.crop_end_y * self.ratio)
        elif self.crop_start_x > self.crop_end_x and self.crop_start_y <= self.crop_end_y:
            start_x = int(self.crop_end_x * self.ratio)
            start_y = int(self.crop_start_y * self.ratio)
            end_x = int(self.crop_start_x * self.ratio)
            end_y = int(self.crop_end_y * self.ratio)
        elif self.crop_start_x <= self.crop_end_x and self.crop_start_y > self.crop_end_y:
            start_x = int(self.crop_start_x * self.ratio)
            start_y = int(self.crop_end_y * self.ratio)
            end_x = int(self.crop_end_x * self.ratio)
            end_y = int(self.crop_start_y * self.ratio)
        else:
            start_x = int(self.crop_end_x * self.ratio)
            start_y = int(self.crop_end_y * self.ratio)
            end_x = int(self.crop_start_x * self.ratio)
            end_y = int(self.crop_start_y * self.ratio)

        x = slice(start_x, end_x, 1)
        y = slice(start_y, end_y, 1)

        # used to check if the crop is valid
        try:
            image = cv2.cvtColor(self.master.master.processed_image[y,x], cv2.COLOR_BGR2RGB)
        except cv2.error as e:
            print(e)
            self.canvas.delete(self.rectangle_id)
            self._deactive_crop_mode(None)
            return

        self._set_crop_coordinates(self.crop_start_x, self.crop_start_y, self.crop_end_x, self.crop_end_y)

        self.master.master.processed_image = self.master.master.processed_image[y, x]

        title = "Cropped Image"
        self._insert_into_history(title)

        self.display_image(self.master.master.processed_image)

    def _perform_crop_to_image(self, img=None):
        image = img
        if self.master.master.image_properties.crop_start_x == 0 or self.master.master.image_properties.crop_start_y == 0 or self.master.master.image_properties.crop_end_x == 0 or self.master.master.image_properties.crop_end_y == 0:
            return image
        original_start_x = int(self.master.master.image_properties.crop_start_x)
        original_start_y = int(self.master.master.image_properties.crop_start_y)
        original_end_x = int(self.master.master.image_properties.crop_end_x)
        original_end_y = int(self.master.master.image_properties.crop_end_y)
        original_ratio = self.master.master.image_properties.crop_ratio

        if original_start_x <= original_end_x and original_start_y <= original_end_y:
            start_x = int(original_start_x * original_ratio)
            start_y = int(original_start_y * original_ratio)
            end_x = int(original_end_x * original_ratio)
            end_y = int(original_end_y * original_ratio)
        elif original_start_x > original_end_x and original_start_y <= original_end_y:
            start_x = int(original_end_x * original_ratio)
            start_y = int(original_start_y * original_ratio)
            end_x = int(original_start_x * original_ratio)
            end_y = int(original_end_y * original_ratio)
        elif original_start_x <= original_end_x and original_start_y > original_end_y:
            start_x = int(original_start_x * original_ratio)
            start_y = int(original_end_y * original_ratio)
            end_x = int(original_end_x * original_ratio)
            end_y = int(original_start_y * original_ratio)
        else:
            start_x = int(original_end_x * original_ratio)
            start_y = int(original_end_y * original_ratio)
            end_x = int(original_start_x * original_ratio)
            end_y = int(original_start_y * original_ratio)

        x = slice(start_x, end_x, 1)
        y = slice(start_y, end_y, 1)

        if self.master.master.original_image is not None:
            image = self.master.master.original_image[y, x]
            return image

        crop_height = original_end_y - original_start_y
        crop_width = original_end_x - original_start_x

        self.master.master.image_properties.crop_start_x = original_start_x
        self.master.master.image_properties.crop_start_y = original_start_y
        self.master.master.image_properties.crop_end_x = original_end_x
        self.master.master.image_properties.crop_end_y = original_end_y
        self.master.master.image_properties.crop_ratio = 1
        self.master.master.image_properties.altered_image_height = crop_height
        self.master.master.image_properties.altered_image_width = crop_width
        self.master.master.image_properties.resize_image_height = crop_height
        self.master.master.image_properties.resize_image_width = crop_width

    def _apply_all_edits(self):
        image = self.master.master.original_image
        if self.master.master.undo_performed:
            image = self._perform_crop_to_image(image)
        image = AllEditFunctions._apply_all_basic_edits(
            self.master.master.image_properties, image)
        image = AllEditFunctions._apply_all_advanced_edits(
            self.master.master.image_properties, image)
        self.master.master.processed_image = image
        self.display_image(self.master.master.processed_image)

    def clear_canvas(self):
        self.canvas.delete("all")

    def _set_zoom_bool(self):
        if self.scale_factor == 1.0:
            self.master.master.image_properties.is_zoomed = False
        else:
            self.master.master.image_properties.is_zoomed = True

    def _zoom(self, event):
        if event.keysym == 'KP_Add' or event.delta == 120:
            if self.scale_factor > 2.2:
                self.scale_factor = 2.2
                return
            self.scale_factor *= 1.2
            self._set_zoom_bool()
        elif event.keysym == 'minus' or event.delta == -120:
            if self.scale_factor < 0.2:
                self.scale_factor = 0.2
                return
            self.scale_factor *= 0.8
            self._set_zoom_bool()
        self._zoom_canvas_adj()
        self.display_image()
        print(f"Zoom Height: {self.master.master.image_properties.zoom_image_height}, Zoom Width: {self.master.master.image_properties.zoom_image_width}")
        print(f"Scale Factor: {self.scale_factor}")
        print(f"Canvas Height: {self.canvas.winfo_height()}, Canvas Width: {self.canvas.winfo_width()}")

    def _zoom_in(self, event):
        if self.scale_factor > 2.2:
            self.scale_factor = 2.2
            return
        self.scale_factor *= 1.2
        self._set_zoom_bool()
        self._zoom_canvas_adj()
        self.display_image()

    def _zoom_out(self, event):
        if self.scale_factor < 0.2:
            self.scale_factor = 0.2
            return
        self.scale_factor *= 0.8
        self._set_zoom_bool()
        self._zoom_canvas_adj()
        self.display_image()

    def _zoom_canvas_adj(self):
        if self.scale_factor <= 1.0:
            return
        self.canvas_width = self.original_canvas_width * self.scale_factor
        self.canvas_height = self.original_canvas_height * self.scale_factor
        self.canvas.config(width=self.canvas_width, height=self.canvas_height)

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
            crop_ratio=self.master.master.image_properties.crop_ratio,
            crop_rectangle_height=self.master.master.image_properties.crop_rectangle_height,
            crop_rectangle_width=self.master.master.image_properties.crop_rectangle_width,
        )
        return edit_instance