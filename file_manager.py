import os
from tkinter import filedialog, simpledialog  # pip install tk
import cv2 as cv
import imageio  # pip install imageio
import glob

class FileManager:
    def __init__(self):
        self.file = None
        self.batch_files = None #Alternate variable for a list of batch processed files

    def get_file(self):
        valid_file_types = [
            ("Image Files", "*.png *.jpeg *.jpg *.gif *.bmp *.tiff"),
            ("PNG files", "*.png"),
            ("JPEG files", "*.jpeg"),
            ("JPEG files", "*.jpg"),
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
                    new_file_path = os.path.join(
                        directory, f'{name}_first_frame.png')

                    # Prompt confirmation to user to create new image from GIF.
                    result = simpledialog.messagebox.askokcancel(
                        "Importing GIF", f"Creating PNG of first frame from select GIF to {new_file_path}")
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
            ("JPEG files", "*.jpeg"),
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
                # Save the image again with correct colors.
                imageio.mimsave(file_path, [image_bgr])

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

    def get_files(self):
            answer = simpledialog.messagebox.askyesnocancel("Preparing to Select Folder", 
                                                      "Would you rather select files manually? \n\nNote: A PNG will be created for the first frame of each GIF file.")
            
            if answer is None:
                return

            gifFile = False

            valid_file_types = [
                ("Image Files", "*.png *.jpeg *.jpg *.gif *.bmp *.tiff"),
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpeg"),
                ("JPEG files", "*.jpg"),
                ("GIF files", "*.gif"),
                ("BMP files", "*.bmp"),
                ("TIFF files", "*.tiff")
            ]

            if answer is False:
                folder_path = filedialog.askdirectory()
                if not folder_path: return # User cancelled folder selection

                warning = simpledialog.messagebox.askokcancel("Warning",  
                                    "Batch processing is irreversible. Are you sure you want to proceed?")
                if warning is False: return # User decided to cancel the process

                file_set = []
                for file_type in valid_file_types:
                    _, file_extension = file_type
                    file_pattern = os.path.join(folder_path, file_extension)
                    matching_files = glob.glob(file_pattern) # Use glob to find files matching the pattern
                    file_set.extend(matching_files) # Add matching files to the file_set
            elif answer is True:
                file_set = filedialog.askopenfilenames(
                    filetypes=valid_file_types)  # Prompt user to select images
                if not file_set: return

                warning = simpledialog.messagebox.askokcancel("Warning",  
                                    "Batch processing is irreversible. Are you sure you want to proceed?")
                if warning is False: return # User decided to cancel the process
                
                file_set = list(file_set)
            
            for i, file_path in enumerate(file_set):
                if file_path.endswith(".gif"):

                    # Gets the first frame from the gif
                    cap = cv.VideoCapture(file_path)
                    ret, first_frame = cap.read()
                    cap.release()

                    if ret:
                        gifFile = True
                        directory, file_name = os.path.split(file_path)
                        name, ext = os.path.splitext(file_name)
                        new_file_path = os.path.join(
                            directory, f'{name}_first_frame.png')
                        
                        cv.imwrite(new_file_path, first_frame)
                        file_set[i] = new_file_path
                    else:
                        print("Error: Could not read first frame from GIF")

            if gifFile is True:
                simpledialog.messagebox.showinfo("GIF(s) Detected", "For each GIF file that was processed, another image was created of its first frame.")

            self.batch_files = file_set