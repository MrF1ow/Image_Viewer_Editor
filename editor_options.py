from tkinter import Frame, Button, TOP, LEFT, RIGHT, BOTTOM
from advanced_editor_tools import AdvancedEditorTools

class EditorOptions(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master=master)

        # creates the button
        self.brightness_button= Button(self, text="Brightness")
        # binds the button to the function
        self.brightness_button.bind("<ButtonRelease>", self.brightness_button)
        # this puts it on the top left
        self.brightness_button.pack(side=LEFT, anchor="nw")

    def brightness_button(self, event):
        brightness_value = 20
        AdvancedEditorTools.set_brightness(brightness_value)