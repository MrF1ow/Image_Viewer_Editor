from PIL import Image
import cv2
import numpy as np


class AllEditFunctions:
    @staticmethod
    def _apply_horizontal_flip_image(img_properties=None, img=None):
        image_properties = img_properties
        image = img
        image = Image.fromarray(image)

        flipped_image = image.transpose(
            method=Image.FLIP_LEFT_RIGHT) if image_properties.is_flipped_horz else image
        numpy_image = np.array(flipped_image)
        return numpy_image

    @staticmethod
    def _apply_vertical_flip_image(img_properties=None, img=None):
        image_properties = img_properties
        image = img
        image = Image.fromarray(image)

        flipped_image = image.transpose(
            method=Image.FLIP_TOP_BOTTOM) if image_properties.is_flipped_vert else image
        numpy_image = np.array(flipped_image)
        return numpy_image

    @staticmethod
    def _apply_grayscale_to_image(img_properties=None, img=None):
        image_properties = img_properties
        image = img
        grayscale_image = cv2.cvtColor(
            image, cv2.COLOR_BGR2GRAY) if image_properties.is_grayscaled else image
        return grayscale_image

    @staticmethod
    def _apply_sepia_to_image(img_properties=None, img=None):
        image_properties = img_properties
        image = img
        sepia_image = image

        if image_properties.is_sepia:
            array_image = np.array(image, dtype=np.float64)
            sepia_filter = np.array([[0.272, 0.534, 0.131],
                                     [0.349, 0.686, 0.168],
                                     [0.393, 0.769, 0.189]])
            sepia_image = np.dot(array_image, sepia_filter.T).clip(
                0, 255).astype(np.uint8)
            sepia_image = np.array(sepia_image, dtype=np.uint8)

        return sepia_image

    @staticmethod
    def _apply_rotation_to_image(img_properties=None, img=None):
        image_properties = img_properties
        image = img
        angle = image_properties.rotation
        image = Image.fromarray(image)

        rotated_image = image.rotate(
            angle=angle, resample=Image.NEAREST, expand=True)
        numpy_image = np.array(rotated_image)

        resize_height = image_properties.resize_image_height
        resize_width = image_properties.resize_image_width

        if angle == 90 or angle == 270:
            image_properties.altered_image_height = resize_width
            image_properties.altered_image_width = resize_height
        elif angle in [0, 180, 360]:
            image_properties.altered_image_height = resize_height
            image_properties.altered_image_width = resize_width

        return numpy_image

    @staticmethod
    def _apply_resize_to_image(img_properties=None, img=None):
        image_properties = img_properties
        image = img
        resized_image = cv2.resize(image, (image_properties.altered_image_width,
                                           image_properties.altered_image_height))
        return resized_image

    @staticmethod
    def _apply_all_basic_edits(img_properties=None, img=None):
        image_properties = img_properties
        resize = image_properties.is_resized
        image = img
        image = AllEditFunctions._apply_rotation_to_image(
            image_properties, image)
        if resize is True:
            image = AllEditFunctions._apply_resize_to_image(
                image_properties, image)
        image = AllEditFunctions._apply_grayscale_to_image(
            image_properties, image)
        image = AllEditFunctions._apply_horizontal_flip_image(
            image_properties, image)
        image = AllEditFunctions._apply_vertical_flip_image(
            image_properties, image)
        image = AllEditFunctions._apply_sepia_to_image(image_properties, image)

        return image

    @staticmethod
    def _convert_brightness(num):
        return num * 2.54 - 127

    @staticmethod
    def _convert_contrast(num):
        return num * 0.02

    @staticmethod
    def _convert_hue(num):
        return int(num * 1.79)

    @staticmethod
    def _apply_blur_to_image(img_properties=None, img=None):
        image_properties = img_properties
        image = img
        blur_value = image_properties.blur
        # this is how distorted each pixel will become
        kernel_size = (blur_value, blur_value)
        # the kernel size had to be a positive, ODD number
        kernel_size = tuple(size + 1 if size %
                            2 == 0 else size for size in kernel_size)
        # applies the actual blur
        image = cv2.blur(img, kernel_size)
        return image

    @staticmethod
    def _apply_hue_to_image(img_properties=None, img=None):
        image_properties = img_properties
        image = img
        hue_value = AllEditFunctions._convert_hue(image_properties.hue)
        # Convert image to HSV
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        # Change the hue channel
        # Hue values range from 0 to 179
        hsv_image[:, :, 0] = (hsv_image[:, :, 0] + hue_value) % 180

        # Convert back to BGR
        image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)
        return image

    @staticmethod
    def _apply_saturation_to_image(img_properties=None, img=None):
        image_properties = img_properties
        image = img
        saturation_value = image_properties.saturation
        saturation_factor = 1 + saturation_value
        # Convert image to HSV
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Saturation values range 0 - 255
        hsv_image[:, :, 1] = np.clip(
            hsv_image[:, :, 1] * saturation_factor, 0, 255).astype(np.uint8)

        # Convert back to BGR
        image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)
        return image

    @staticmethod
    def _apply_brightness_and_contrast_to_image(img_properties=None, img=None):
        image_properties = img_properties
        image = img
        brightness_value = image_properties.brightness
        contrast_value = image_properties.contrast

        brightness_factor = AllEditFunctions._convert_brightness(brightness_value)
        contrast_factor = AllEditFunctions._convert_contrast(contrast_value)
        # applies the actual brightness change
        image = cv2.convertScaleAbs(
            image, alpha=contrast_factor, beta=brightness_factor)
        return image

    @staticmethod
    def _apply_all_advanced_edits(img_properties=None, img=None):
        image_properties = img_properties
        image = img
        image = AllEditFunctions._apply_blur_to_image(image_properties, image)
        image = AllEditFunctions._apply_brightness_and_contrast_to_image(image_properties, image)
        if image_properties.is_grayscaled == False:
            image = AllEditFunctions._apply_hue_to_image(image_properties, image)
            image = AllEditFunctions._apply_saturation_to_image(image_properties, image)

        return image
