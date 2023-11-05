import tkinter as tk
from tkinter import ttk
from app_options import AppOptions # tried to make a button
from image_manager import ImageManager

# ok so here is the explanation of this lovely feature in python I learned today: pretty much since
# we are passing in the tkinter Tk class into Main, it allows Main to inherit all of the abilities of
# tkinter, but also be able to modify them. This is also the reason why you'll see Frame passed into
# the other classes
class Main(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.file_location = ""
        self.original_image = None
        self.processed_image = None

        # this just sets the title of the application
        self.title("Image Editor")

        self.app_options = AppOptions(master=self)
        separator1 = ttk.Separator(master=self, orient=tk.HORIZONTAL)
        self.image_viewer = ImageManager(master=self)

        self.app_options.pack(pady=10)
        separator1.pack(fill=tk.X, padx=10, pady=5)
        self.image_viewer.pack(fill=tk.BOTH, padx=20, pady=10, expand=1)
