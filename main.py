import tkinter as tk
from tkinter import ttk
from app_options import AppOptions # tried to make a button
from image_manager import ImageManager
from editor_options import EditorOptions
from history_of_edits import History

class Main(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.file_location = ""
        self.original_image = None
        self.processed_image = None

        self.advanced_tools = None
        self.resize_window = None
        self.in_crop_mode = False

        self.history = []

        self.configure(bg="#6b6b6b")

        # this just sets the title of the application
        self.title("Image Editor")

        # this is used just as the frame to contain everything else
        main_frame = tk.Frame(self, bg="#6b6b6b")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # this is the file options (Save As, Save, New...etc)
        # JUST THE BUTTONS
        self.app_options = AppOptions(master=main_frame)
        self.app_options.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        separator1 = ttk.Separator(master=main_frame, orient=tk.HORIZONTAL)
        separator1.pack(fill=tk.X, padx=10, pady=5)

        # Pack EditorOptions on the left
        self.editor_options = EditorOptions(master=main_frame)
        self.editor_options.pack(side=tk.LEFT, fill=tk.Y, padx=20, pady=10)

        # Create a separator between EditorOptions and ImageViewer
        separator4 = ttk.Separator(master=main_frame, orient=tk.VERTICAL)
        separator4.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        # Display the image_viewer
        self.image_viewer = ImageManager(master=main_frame)
        self.image_viewer.pack(side=tk.LEFT, fill=tk.BOTH, padx=20, pady=10, expand=True)

        # Create a separator between ImageViewer and HistoryOfEdits
        separator5 = ttk.Separator(master=main_frame, orient=tk.VERTICAL)
        separator5.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        # Pack HistoryOfEdits on the right
        self.history_of_edits = History(master=main_frame)
        self.history_of_edits.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

