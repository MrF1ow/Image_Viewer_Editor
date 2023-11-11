import tkinter as tk
from tkinter import ttk
from app_options import AppOptions # tried to make a button
from image_manager import ImageManager
from editor_options import EditorOptions

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

        self.advanced_tools = None

        # this just sets the title of the application
        self.title("Image Editor")

        # this is used just as the frame to contain everything else
        main_frame = tk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # this is the file options (Save As, Save, New...etc)
        # JUST THE BUTTONS
        self.app_options = AppOptions(master=main_frame)
        self.app_options.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        separator1 = ttk.Separator(master=main_frame, orient=tk.HORIZONTAL)
        separator1.pack(fill=tk.X, padx=10, pady=5)

        # this is the editor options (Hue, Crop, Brighness)
        # JUST THE BUTTONS
        self.editor_options = EditorOptions(master=main_frame)
        self.editor_options.pack(side=tk.LEFT, fill=tk.Y, padx=20, pady=10)

        separator2 = ttk.Separator(master=main_frame, orient=tk.VERTICAL)
        separator2.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        # this is where the image is actually displayed
        self.image_viewer = ImageManager(master=main_frame)
        self.image_viewer.pack(fill=tk.BOTH, padx=20, pady=10, expand=1)
