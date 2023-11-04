from file_manager import FileManager  # pip install file_manager
from PIL import Image
import sys

# Example of functions
fm = FileManager()

fm.get_file()  # Retrieves file

if fm.file:
    print("Selected file: ", fm.file)
    image = Image.open(fm.file)  # Opens the image
    image.show()
    # fm.save_as_file(image)  # Make a copy
else:
    print("Error")

if fm.file:
    print("Selected File: ", fm.file)
    image = Image.open(fm.file)

    image = image.resize((200, 200))  # Change the size of the image

    fm.save_file(image)  # Saves the changes
    print("Success")
else:
    print("Error")

# this should be an option
fm.delete_file()  # Delete the original file

sys.exit(0) # used to stop infinite looping

