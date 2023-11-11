from tkinter import Frame, Canvas, CENTER
from PIL import Image, ImageTk
import cv2


class ImageManager(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master=master, bg="grey",
                       width=960, height=540)

        self.current_image = None  # store currently displayed image

        # inside of the frame, make a canvas for image using the 'Canvas' widget (look it up)
        self.canvas = Canvas(self, bg="black", width=960, height=540)
        # center the image
        self.canvas.place(relx=0.5, rely=0.5, anchor=CENTER)

    def display_image(self, img=None):
        if img is None:
            image = self.master.master.processed_image.copy() #this uses the processed image if none is given
        else:
            image = img

        # use openCV to convert the image from BGR to RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # getting the height and width of image (metadata???)
        # read this to understand what channels are: https://medium.com/featurepreneur/understanding-the-concept-of-channels-in-an-image-6d59d4dafaa9
        height, width, channels = image.shape
        ratio = height / width

        new_height = height
        new_width = width

        # need to check if the image size is bigger than the frame
        # not gonna lie, chatGPT wrote this part, but it works
        if height > self.winfo_height() or width > self.winfo_width():
            if ratio < 1:
                new_width = self.winfo_width()
                new_height = int(new_height * ratio)
            else:
                new_height = self.winfo_height()
                new_width = int(new_height * (width / height))


        # need to figure out for portraits
        if new_width > 0 and new_height > 0:
            # resizes image to fit
            self.current_image = cv2.resize(image, (new_width, new_height))
            self.current_image = ImageTk.PhotoImage(Image.fromarray(self.current_image))

            self.canvas.config(width=new_width, height=new_height)
            self.canvas.create_image(new_width / 2, new_height / 2, anchor=CENTER, image=self.current_image)

