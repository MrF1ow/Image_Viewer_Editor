import os
from tkinter import filedialog


class FileManager:
    def __init__(self):
        self.file = None

    def get_file(self):

        valid_file_types = [("Image files", "*.png *.jpeg *.gif *.bmp *.tiff")]

        file_path = filedialog.askopenfilename(filetypes=valid_file_types)  # Prompt user to select image

        if file_path:
            self.file = file_path  # Update file attribute with path of file selected

    def save_file(self, content):
        if self.file:
            content.save(self.file)  # Overwrites existing file with new edits

    @staticmethod
    def save_as_file(content):

        valid_file_types = [
            ("PNG files", "*.png"),
            ("JPEG files", " *.jpeg"),
            ("GIF files", "*.gif"),
            ("BMP files", "*.bmp"),
            ("TIFF files", "*.tiff")
        ]

        # Prompts user to save the file under the desired name and file format
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=valid_file_types)

        if file_path:
            content.save(file_path)  # Saves the file in that destination

    def delete_file(self):
        if self.file:
            try:
                os.remove(self.file)  # Removes file from system
                self.file = None  # Clear the file attribute
            except OSError:
                print(f"Error: {OSError}")



