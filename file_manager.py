import os
from tkinter import filedialog, simpledialog  # pip install tk
import cv2 as cv
import imageio # pip install imageio


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
                    directory, file_name = os.path.split(file_path)
                    name, ext = os.path.splitext(file_name)
                    new_file_path = os.path.join(directory, f'{name}_first_frame.png')

                    # Prompt confirmation to user to create new image from GIF.
                    result = simpledialog.messagebox.askokcancel("Importing GIF", f"Creating PNG of first frame from select GIF to {new_file_path}")
                    if not result:
                        return
                    
                    cv.imwrite(new_file_path, first_frame)
                    file_path = new_file_path
                else:
                    print("Error: Could not read first frame from GIF")

            self.file = file_path  # Update file attribute with path of file selected

    def find_file(self, path):
        # Get a file that already exists
        file_path = path
        if file_path:
            self.file = file_path

    def save_file(self, content):
        if self.file:
            # Overwrites existing file with new edits
            cv.imwrite(self.file, content)

    @staticmethod
    def save_as_file(content):

        valid_file_types = [
            ("Image Files", "*.png *.jpeg *.jpg *.gif *.bmp *.tiff"),
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
            if file_path.endswith("gif"):
                # Opencv cant sasve images as GIF. Imageio is used to save.
                imageio.mimsave(file_path, [content])

                # Change color values from RBG to BGR
                image_rgb = imageio.imread(file_path)
                image_bgr = cv.cvtColor(image_rgb, cv.COLOR_RGB2BGR)
                imageio.mimsave(file_path, [image_bgr]) # Save the image again with correct colors.

            else:
                # Saves the file in that destination
                cv.imwrite(file_path, content)

    def delete_file(self):
        if self.file:
            try:
                os.remove(self.file)  # Removes file from system
                self.file = None  # Clear the file attribute
            except OSError:
                print(f"Error: {OSError}")
