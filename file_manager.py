import os
from tkinter import filedialog  # pip install tk
import cv2 as cv
import tempfile


class FileManager:
    def __init__(self):
        self.file = None

    def get_file(self):
        valid_file_types = [
            ("Image Files", "*.png *.jpeg *.jpg *.gif *.bmp *.tiff"),
            ("PNG files", "*.png"),
            ("JPEG files", "*.jpeg *.jpg"),
            ("GIF files", "*.gif"),
            ("BMP files", "*.bmp"),
            ("TIFF files", "*.tiff")
        ]

        file_path = filedialog.askopenfilename(
            filetypes=valid_file_types)  # Prompt user to select image

        if file_path:
            if file_path.endswith(".gif"):

                # Gets the first frame from the gif
                cap = cv.VideoCapture(file_path)
                ret, first_frame = cap.read()
                cap.release()

                if ret:
                    # Puts the frame into a temporary directory
                    temp_dir = tempfile.mkdtemp()
                    temp_file_path = os.path.join(temp_dir, "first_frame.png")
                    cv.imwrite(temp_file_path, first_frame)
                    file_path = temp_file_path
                else:
                    print("Error: Could not read first frame from GIF")

            self.file = file_path  # Update file attribute with path of file selected

    def find_file(self, path):
        file_path = path
        if file_path:
            self.file = file_path

    # this should be an option
    def save_file(self, content):
        if self.file:
            # Overwrites existing file with new edits
            cv.imwrite(self.file, content)

    @staticmethod
    def save_as_file(content):

        valid_file_types = [
            ("PNG files", "*.png"),
            ("JPEG files", "*.jpg"),
            ("GIF files", "*.gif"),
            ("BMP files", "*.bmp"),
            ("TIFF files", "*.tiff")
        ]

        # Prompts user to save the file under the desired name and file format
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png", filetypes=valid_file_types)

        if file_path:
            # Saves the file in that destination
            cv.imwrite(file_path, content)

    def delete_file(self):
        if self.file:
            try:
                os.remove(self.file)  # Removes file from system
                self.file = None  # Clear the file attribute
            except OSError:
                print(f"Error: {OSError}")
