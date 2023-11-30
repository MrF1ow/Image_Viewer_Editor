from tkinter import Frame, Canvas, CENTER
from PIL import Image, ImageTk
import cv2
import math
from tkinter import Frame, Button, Toplevel, Label, Button, Entry


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

        # inside of the frame, make a canvas for image using the 'Canvas' widget (look it up)
        self.canvas = Canvas(self, bg="black",  width=self.canvas_width, height=self.canvas_height, highlightthickness=0)

        # center the image
        self.canvas.place(relx=0.5, rely=0.5, anchor="center")
        self.canvas.config(scrollregion=(0, 0, self.canvas_width, self.canvas_height))

        # Starting coordinates for panning
        self.start_x = 0
        self.start_y = 0
        self.coord_x = 0
        self.coord_y = 0

        #Binding for panning
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

    def display_image(self, img=None, zoom=False):
        self.clear_canvas()
        if img is None:
            # this uses the processed image if none is given
            image = self.master.master.processed_image.copy()
        else:
            image = img

        # use openCV to convert the image from BGR to RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        height, width = image.shape[:2]
        ratio = height / width

        self.master.master.image_properties.altered_image_height = height
        self.master.master.image_properties.altered_image_width = width

        new_height = height
        new_width = width

        # need to check if the image size is bigger than the frame
        if height > self.winfo_height() or width > self.winfo_width():
            if ratio < 1:
                new_width = self.winfo_width()
                new_ratio = new_width / width
                new_height = int(new_height * new_ratio)
            else:
                new_height = self.winfo_height()
                new_width = int(math.floor(new_height * (width / height)))

        # For zoom functionality
        if zoom:
            size = int(new_width * self.scale_factor), int(new_height * self.scale_factor)
            self.current_image = cv2.resize(image, size)
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

        self.canvas.create_image(image_center_x, image_center_y, anchor="nw", image=self.current_image)

        # Moves the image back to pan location when edits are applied
        center_x, center_y = self.canvas.coords("all")

        self.canvas.move("all", self.master.master.image_properties.pan_coord_x, self.master.master.image_properties.pan_coord_y)

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

        bbox = self.canvas.bbox("all")  # Get the bounding box of all elements on the canvas
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        # Calculate the current position
        current_x, current_y = self.canvas.coords("all")

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
            self.master.master.image_properties.pan_coord_x -= (self.canvas.winfo_width()*.1)
        if current_x-(self.canvas.winfo_width()*.1) < 0:
            self.canvas.move("all", -current_x, 0)
            self.start_x -= current_x
            self.master.master.image_properties.pan_coord_x -= current_x

    def _pan_right(self, event):
        bbox = self.canvas.bbox("all")  # Get the bounding box of all elements on the canvas
        if bbox[2]+(self.canvas.winfo_width()*.1) <= self.canvas.winfo_width():
            self.canvas.move("all", +(self.canvas.winfo_width()*.1), 0)
            self.start_x += (self.canvas.winfo_width()*.1)
            self.master.master.image_properties.pan_coord_x += (self.canvas.winfo_width()*.1)
        if bbox[2]+(self.canvas.winfo_width()*.1) > self.canvas.winfo_width():
            self.canvas.move("all", self.canvas.winfo_width()-bbox[2], 0)
            self.start_x += self.canvas.winfo_width()-bbox[2]
            self.master.master.image_properties.pan_coord_x += self.canvas.winfo_width()-bbox[2]

    def _pan_down(self, event):
        bbox = self.canvas.bbox("all")  # Get the bounding box of all elements on the canvas
        if bbox[3]+(self.canvas.winfo_height()*.1) <= self.canvas.winfo_height():
            self.canvas.move("all", 0, +(self.canvas.winfo_height()*.1))
            self.start_y += (self.canvas.winfo_height()*.1)
            self.master.master.image_properties.pan_coord_y += (self.canvas.winfo_height()*.1)
        if bbox[3]+(self.canvas.winfo_height()*.1) > self.canvas.winfo_height():
            self.canvas.move("all", 0, self.canvas.winfo_height()-bbox[3])
            self.start_y += self.canvas.winfo_height()-bbox[3]
            self.master.master.image_properties.pan_coord_y += self.canvas.winfo_height()-bbox[3]

    def _pan_up(self, event):
        current_x, current_y = self.canvas.coords("all")
        if current_y-(self.canvas.winfo_height()*.1) >= 0:
            self.canvas.move("all", 0, -(self.canvas.winfo_height()*.1))
            self.start_y -= (self.canvas.winfo_height()*.1)
            self.master.master.image_properties.pan_coord_y -= (self.canvas.winfo_height()*.1)
        if current_y-(self.canvas.winfo_height()*.1) < 0:
            self.canvas.move("all", 0, -current_y)
            self.start_y -= current_y
            self.master.master.image_properties.pan_coord_y -= current_y

    #Resets the pan coordinates
    def _reset(self):
        self.canvas.move("all", -self.master.master.image_properties.pan_coord_x, -self.master.master.image_properties.pan_coord_y)
        self.master.master.image_properties.pan_coord_x = 0
        self.master.master.image_properties.pan_coord_y = 0
        self.start_x = 0
        self.start_y = 0

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
                                                         self.crop_end_x, self.crop_end_y, width=3, outline="red")

    def _set_crop_coordinates(self, start_x, start_y, end_x, end_y):
        self.master.master.image_properties.is_cropped = True
        self.master.master.image_properties.crop_start_x = start_x
        self.master.master.image_properties.crop_start_y = start_y
        self.master.master.image_properties.crop_end_x = end_x
        self.master.master.image_properties.crop_end_y = end_y
        self.master.master.image_properties.crop_ratio = self.ratio

    def _end_crop(self, event):
        self._set_crop_coordinates(
            self.crop_start_x, self.crop_start_y, self.crop_end_x, self.crop_end_y)
        if self.master.master.image_properties.crop_start_x <= self.master.master.image_properties.crop_end_x and self.master.master.image_properties.crop_start_y <= self.master.master.image_properties.crop_end_y:
            start_x = int(self.master.master.image_properties.crop_start_x *
                          self.master.master.image_properties.crop_ratio)
            start_y = int(self.master.master.image_properties.crop_start_y *
                          self.master.master.image_properties.crop_ratio)
            end_x = int(self.master.master.image_properties.crop_end_x *
                        self.master.master.image_properties.crop_ratio)
            end_y = int(self.master.master.image_properties.crop_end_y *
                        self.master.master.image_properties.crop_ratio)
        elif self.master.master.image_properties.crop_start_x > self.master.master.image_properties.crop_end_x and self.master.master.image_properties.crop_start_y <= self.master.master.image_properties.crop_end_y:
            start_x = int(self.master.master.image_properties.crop_end_x *
                          self.master.master.image_properties.crop_ratio)
            start_y = int(self.master.master.image_properties.crop_start_y *
                          self.master.master.image_properties.crop_ratio)
            end_x = int(self.master.master.image_properties.crop_start_x *
                        self.master.master.image_properties.crop_ratio)
            end_y = int(self.master.master.image_properties.crop_end_y *
                        self.master.master.image_properties.crop_ratio)
        elif self.master.master.image_properties.crop_start_x <= self.master.master.image_properties.crop_end_x and self.master.master.image_properties.crop_start_y > self.master.master.image_properties.crop_end_y:
            start_x = int(self.master.master.image_properties.crop_start_x *
                          self.master.master.image_properties.crop_ratio)
            start_y = int(self.master.master.image_properties.crop_end_y *
                          self.master.master.image_properties.crop_ratio)
            end_x = int(self.master.master.image_properties.crop_end_x *
                        self.master.master.image_properties.crop_ratio)
            end_y = int(self.master.master.image_properties.crop_start_y *
                        self.master.master.image_properties.crop_ratio)
        else:
            start_x = int(self.master.master.image_properties.crop_end_x *
                          self.master.master.image_properties.crop_ratio)
            start_y = int(self.master.master.image_properties.crop_end_y *
                          self.master.master.image_properties.crop_ratio)
            end_x = int(self.master.master.image_properties.crop_start_x *
                        self.master.master.image_properties.crop_ratio)
            end_y = int(self.master.master.image_properties.crop_start_y *
                        self.master.master.image_properties.crop_ratio)

        x = slice(start_x, end_x, 1)
        y = slice(start_y, end_y, 1)

        # return image[y, x]

        self.master.master.processed_image = self.master.master.processed_image[y, x]
        self.display_image(self.master.master.processed_image)

    def _finalize_crop(self, img=None, start_x=None, start_y=None, end_x=None, end_y=None):
        image = img
        x = slice(start_x, end_x, 1)
        y = slice(start_y, end_y, 1)
        return image[y, x]

    # gotta figure this one

    def _revert_crop_coordinates(self):
        original_start_x = int(self.master.master.image_properties.crop_start_x /
                               self.master.master.image_properties.crop_ratio)
        original_start_y = int(self.master.master.image_properties.crop_start_y /
                               self.master.master.image_properties.crop_ratio)
        original_end_x = int(self.master.master.image_properties.crop_end_x /
                             self.master.master.image_properties.crop_ratio)
        original_end_y = int(self.master.master.image_properties.crop_end_y /
                             self.master.master.image_properties.crop_ratio)

        x = slice(original_start_x, original_end_x, 1)
        y = slice(original_start_y, original_end_y, 1)

        self.master.master.image_properties.crop_start_x = original_start_x
        self.master.master.image_properties.crop_start_y = original_start_y
        self.master.master.image_properties.crop_end_x = original_end_x
        self.master.master.image_properties.crop_end_y = original_end_y
        self.master.master.image_properties.crop_ratio = 1

        if self.master.master.original_image is not None:
            self.master.master.processed_image = self.master.master.original_image[y, x]
            self.display_image(self.master.master.processed_image)

    def _apply_all_edits(self):
        image = self.master.master.original_image
        if self.master.master.advanced_tools is not None:
            image = self.master.master.advanced_tools._apply_all_advanced_edits(
                image)
        # self._end_crop()
        image = self.master.master.editor_options._apply_all_basic_edits(image)
        self.master.master.processed_image = image
        self.display_image(self.master.master.processed_image)

    def clear_canvas(self):
        self.canvas.delete("all")

    def _zoom(self, event):
        if event.keysym == 'KP_Add' or event.delta == 120:
            if self.scale_factor > 2.2:
                return
            self.scale_factor *= 1.2
        elif event.keysym == 'minus' or event.delta == -120:
            if self.scale_factor < 0.2:
                return
            self.scale_factor *= 0.8
        self.display_image(zoom=True)

    def _zoom_in(self, event):
        if self.scale_factor > 2.2:
            return
        self.scale_factor *= 1.2
        self.display_image(zoom=True)

    def _zoom_out(self, event):
        if self.scale_factor < 0.2:
            return
        self.scale_factor *= 0.8
        self.display_image(zoom=True)