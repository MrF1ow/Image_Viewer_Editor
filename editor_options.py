import numpy as np
from tkinter import Frame, Button, TOP, LEFT, RIGHT, BOTTOM, Toplevel
from PIL import Image, ImageTk
from image_properties import ImageProperties
from advanced_editor_tools import AdvancedEditorTools


class EditorOptions(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master=master)

        # creates the button
        self.advanced_edits_button = Button(self, text="Advanced Edits")
        # binds the button to the function
        self.advanced_edits_button.bind("<ButtonRelease>", self._open_advanced_edits)
        # this puts it on the top left
        self.advanced_edits_button.grid(row=0, column=0, sticky="w")

        self.horz_flip_button = Button(self, text="Horz Flip")
        self.horz_flip_button.bind(
            "<ButtonRelease>", self.horizontal_flip_image)
        self.horz_flip_button.grid(row=0, column=1, sticky="e")

        self.vert_flip_button = Button(self, text="Vert Flip")
        self.vert_flip_button.bind("<ButtonRelease>", self.vertical_flip_image)
        self.vert_flip_button.grid(row=1, column=0, sticky="sw", columnspan=2)

        self.rotate_button = Button(self, text="Rotate")
        self.rotate_button.bind("<ButtonRelease>", self.rotate_image)
        self.rotate_button.grid(row=1, column=1, sticky="se", columnspan=2)

    # this function opens the place where we are going to have all the sliders for our advanced editor tools
    def _open_advanced_edits(self, event):
        self.master.master.advanced_tools = AdvancedEditorTools(master=self.master)
        self.master.master.advanced_tools.grab_set()


    def horizontal_flip_image(self, event):
        # Get the processed image from the master
        image = self.master.master.processed_image
        # Convert the numpy array of pixels to a Pillow image
        image = Image.fromarray(image)

        # Check if the image is already horizontally flipped
        if ImageProperties.is_flipped_horz:
            # If it's flipped, revert back to the original
            ImageProperties.is_flipped_horz = False
            flipped_image = image
        else:
            # If it's not flipped, flip it horizontally
            ImageProperties.is_flipped_horz = True
            flipped_image = image.transpose(method=Image.FLIP_LEFT_RIGHT)

        # Convert the flipped image back to a numpy array
        numpy_image = np.array(flipped_image)
        # Update the processed image in the master
        self.master.master.processed_image = numpy_image
        # Display the flipped image in the image viewer
        self.master.master.image_viewer.display_image(numpy_image)


    def vertical_flip_image(self, event):
        # Get the processed image from the master
        image = self.master.master.processed_image
        # Convert the numpy array of pixels to a Pillow image
        image = Image.fromarray(image)

        # Check if the image is already vertically flipped
        if ImageProperties.is_flipped_vert:
            # If it's flipped, revert back to the original
            ImageProperties.is_flipped_vert = False
            flipped_image = image
        else:
            # If it's not flipped, flip it vertically
            ImageProperties.is_flipped_vert = True
            flipped_image = image.transpose(method=Image.FLIP_TOP_BOTTOM)

        # Convert the flipped image back to a numpy array
        numpy_image = np.array(flipped_image)
        # Update the processed image in the master
        self.master.master.processed_image = numpy_image
        # Display the flipped image in the image viewer
        self.master.master.image_viewer.display_image(numpy_image)


    def rotate_image(self, event):
        # Get the processed image from the master
        image = self.master.master.processed_image
        # Convert the numpy array of pixels to a Pillow image
        image = Image.fromarray(image)

        # Rotate the image 90 degrees clockwise
        rotated_image = image.rotate(90, resample=Image.NEAREST, expand=True)
        # Convert the rotated image back to a numpy array
        numpy_image = np.array(rotated_image)

        # Update the processed image in the master
        self.master.master.processed_image = numpy_image
        # Display the rotated image in the image viewer
        self.master.master.image_viewer.display_image(numpy_image)
