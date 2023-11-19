from tkinter import Frame, Canvas, CENTER
from PIL import Image, ImageTk
import cv2
import math
from image_properties import ImageProperties
from advanced_editor_tools import AdvancedEditorTools
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

        # inside of the frame, make a canvas for image using the 'Canvas' widget (look it up)
        self.canvas = Canvas(self, bg="black",  width=720, height=405)
        # center the image
        self.canvas.place(relx=0.5, rely=0.5, anchor="center")

    def display_image(self, img=None):
        self.clear_canvas()
        if img is None:
            # this uses the processed image if none is given
            image = self.master.master.processed_image.copy()
        else:
            image = img

        # use openCV to convert the image from BGR to RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # getting the height and width of image (metadata???)
        # read this to understand what channels are: https://medium.com/featurepreneur/understanding-the-concept-of-channels-in-an-image-6d59d4dafaa9
        height, width, channels = image.shape
        ratio = height / width

        ImageProperties.altered_image_height = height
        ImageProperties.altered_image_width = width

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

        self.current_image = cv2.resize(image, (new_width, new_height))
        self.current_image = ImageTk.PhotoImage(
            Image.fromarray(self.current_image))

        self.ratio = height / new_height

        self.canvas.config(width=new_width, height=new_height)
        self.canvas.create_image(
            new_width / 2, new_height / 2, anchor="center", image=self.current_image)

    def _active_crop_mode(self, event):
        self.canvas.bind("<ButtonPress>", self._start_crop)
        self.canvas.bind("<B1-Motion>", self._update_crop)
        self.canvas.bind("<ButtonRelease>", self._end_crop)
        self.master.master.in_crop_mode = True

    def _deactive_crop_mode(self, event):
        self.canvas.unbind("<ButtonPress>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease>")
        self.master.master.in_crop_mode = False

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
        ImageProperties.is_cropped = True
        ImageProperties.crop_start_x = start_x
        ImageProperties.crop_start_y = start_y
        ImageProperties.crop_end_x = end_x
        ImageProperties.crop_end_y = end_y
        ImageProperties.crop_ratio = self.ratio

    def _end_crop(self, event):
        self._set_crop_coordinates(self.crop_start_x, self.crop_start_y, self.crop_end_x, self.crop_end_y)
        if ImageProperties.crop_start_x <= ImageProperties.crop_end_x and ImageProperties.crop_start_y <= ImageProperties.crop_end_y:
            start_x = int(ImageProperties.crop_start_x * ImageProperties.crop_ratio)
            start_y = int(ImageProperties.crop_start_y * ImageProperties.crop_ratio)
            end_x = int(ImageProperties.crop_end_x * ImageProperties.crop_ratio)
            end_y = int(ImageProperties.crop_end_y * ImageProperties.crop_ratio)
        elif ImageProperties.crop_start_x > ImageProperties.crop_end_x and ImageProperties.crop_start_y <= ImageProperties.crop_end_y:
            start_x = int(ImageProperties.crop_end_x * ImageProperties.crop_ratio)
            start_y = int(ImageProperties.crop_start_y * ImageProperties.crop_ratio)
            end_x = int(ImageProperties.crop_start_x * ImageProperties.crop_ratio)
            end_y = int(ImageProperties.crop_end_y * ImageProperties.crop_ratio)
        elif ImageProperties.crop_start_x <= ImageProperties.crop_end_x and ImageProperties.crop_start_y > ImageProperties.crop_end_y:
            start_x = int(ImageProperties.crop_start_x * ImageProperties.crop_ratio)
            start_y = int(ImageProperties.crop_end_y * ImageProperties.crop_ratio)
            end_x = int(ImageProperties.crop_end_x * ImageProperties.crop_ratio)
            end_y = int(ImageProperties.crop_start_y * ImageProperties.crop_ratio)
        else:
            start_x = int(ImageProperties.crop_end_x * ImageProperties.crop_ratio)
            start_y = int(ImageProperties.crop_end_y * ImageProperties.crop_ratio)
            end_x = int(ImageProperties.crop_start_x * ImageProperties.crop_ratio)
            end_y = int(ImageProperties.crop_start_y * ImageProperties.crop_ratio)

        # x = slice(start_x, end_x, 1)
        # y = slice(start_y, end_y, 1)

        # return image[y, x]

        # self.master.master.processed_image = self.master.master.processed_image[y, x]
        # self.display_image(self.master.master.processed_image)

    def _finalize_crop(self, img=None, start_x=None, start_y=None, end_x=None, end_y=None):
        image = img
        x = slice(start_x, end_x, 1)
        y = slice(start_y, end_y, 1)
        return image[y, x]


    # gotta figure this one
    def _revert_crop_coordinates(self):
        original_start_x = int(ImageProperties.crop_start_x / ImageProperties.crop_ratio)
        original_start_y = int(ImageProperties.crop_start_y / ImageProperties.crop_ratio)
        original_end_x = int(ImageProperties.crop_end_x / ImageProperties.crop_ratio)
        original_end_y = int(ImageProperties.crop_end_y / ImageProperties.crop_ratio)

        x = slice(original_start_x, original_end_x, 1)
        y = slice(original_start_y, original_end_y, 1)

        ImageProperties.crop_start_x = original_start_x
        ImageProperties.crop_start_y = original_start_y
        ImageProperties.crop_end_x = original_end_x
        ImageProperties.crop_end_y = original_end_y
        ImageProperties.crop_ratio = 1

        if self.master.master.original_image is not None:
            self.master.master.processed_image = self.master.master.original_image[y, x]
            self.display_image(self.master.master.processed_image)

    def _apply_all_edits(self):
        image = self.master.master.original_image
        image = self.master.master.editor_options._apply_all_basic_edits(image)
        if self.master.master.advanced_tools is not None:
            image = self.master.master.advanced_tools._apply_all_advanced_edits(image)
        self._end_crop(event=None, img=image)
        self.master.master.processed_image = image
        self.display_image(self.master.master.processed_image)

    def clear_canvas(self):
        self.canvas.delete("all")


