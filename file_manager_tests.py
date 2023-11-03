from file_manager import FileManager
from PIL import Image

# Example of functions
fm = FileManager()

fm.get_file()  # Retrieves file

if fm.file:
    print("Selected file: ", fm.file)
    image = Image.open(fm.file)  # Opens the image

    fm.save_as_file(image)  # Make a copy
    print("Success")
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

if fm.file:
    print("Selected file: ", fm.file)
    image = Image.open(fm.file)  # Opens the image

    fm.save_as_file(image)  # Make a copy with the edit
    print("Success")
else:
    print("Error")

fm.delete_file()  # Delete the original file
