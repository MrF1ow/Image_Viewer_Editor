from tkinter import Toplevel, Label, Entry, Button


class CropOptions(Toplevel):
    def __init__(self, master=None):
        Toplevel.__init__(self, master=master)

        #register validation commands for Entry
        self.left_check = (self.register(self.check_min_border), '%P')
        self.right_check = (self.register(self.check_right), '%P')
        self.top_check = (self.register(self.check_min_border), '%P')
        self.bottom_check = (self.register(self.check_bottom), '%P')

        # Image data
        self.original_image = self.master.master.original_image
        self.processing_image = self.master.master.processed_image

        # Window label to give image size info to user
        self.title = Label(self, text='Image size: {height} x {width}'.format(height=self.processing_image.shape[0],
                                                                              width=self.processing_image.shape[1]))
        self.title.pack()

        # Initialization of all label and entry widgets
        # Must be registered to validation commands
        self.top_label = Label(self, text="Top Border")
        self.top_entry = Entry(self)
        self.top_entry.config(validate="key", validatecommand=self.top_check)
        self.top_entry.insert(0, "0")
        self.top_label.pack()
        self.top_entry.pack()

        self.bottom_label = Label(self, text="Bottom Border")
        self.bottom_entry = Entry(self)
        self.bottom_entry.config(validate="key", validatecommand=self.bottom_check)
        self.bottom_entry.insert(0, "{}".format(self.processing_image.shape[0]))
        self.bottom_label.pack()
        self.bottom_entry.pack()

        self.left_label = Label(self, text="Left Border")
        self.left_entry = Entry(self)
        self.left_entry.config(validate="key", validatecommand=self.left_check)
        self.left_entry.insert(0, "0")
        self.left_label.pack()
        self.left_entry.pack()

        self.right_label = Label(self, text="Right Border")
        self.right_entry = Entry(self)
        self.right_entry.config(validate="key", validatecommand=self.right_check)
        # TODO for some reason the default value is no longer inserting, an outside eye would be helpful for fixing this
        self.right_entry.insert(0, "{}".format(self.processing_image.shape[1]))
        self.right_label.pack()
        self.right_entry.pack()

        self.apply_button = Button(self, text="Apply")
        self.apply_button = Button(self, text="Apply", command=self._apply_edits_to_image)
        self.apply_button.pack()

        # Organize grid for widgets
        """
        self.left_label.grid(row=0, column=0)
        self.left_entry.grid(row=1, column=0)

        self.right_entry.grid(row=1, column=1)
        self.right_label.grid(row=0, column=1)

        self.top_entry.grid(row=3, column=0)
        self.top_label.grid(row=2, column=0)

        self.bottom_entry.grid(row=3, column=1)
        self.bottom_label.grid(row=2, column=1)
        """

    def _crop_image(self, left, right, top, bot):
        # Values are validated, so we shouldn't have to worry about using int()
        self.processing_image = self.processing_image[int(top):int(bot), int(left):int(right)]

    def _apply_edits_to_image(self):
        left_border = self.left_entry.get()
        right_border = self.right_entry.get()
        top_border = self.top_entry.get()
        bottom_border = self.bottom_entry.get()

        self._crop_image(left_border, right_border, top_border, bottom_border)

        self.master.master.processed_image = self.processing_image
        self.master.master.image_viewer.display_image(img=self.processing_image)

        self.destroy()  # closes the AdvancedEditorTools (destructor pretty much)

    @staticmethod
    def check_min_border(num):
        if num.isdigit():
            if int(num) >= 0:
                return True

        return False

    def check_bottom(self, num):
        if num.isdigit():
            if int(num) <= self.processing_image.shape[0]:
                return True
        return False

    def check_right(self, num):
        if num.isdigit():
            if int(num) <= self.processing_image.shape[1]:
                return True

        return False
