import cv2 as cv

class AdvancedEditorTools():
    def init(self, file):
        self.file = file


    def set_brightness(self, desired_brightness: int):
        if 0 <= desired_brightness <= 100:
            self.image_properties.brightness(desired_brightness)