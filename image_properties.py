from dataclasses import dataclass

@dataclass
class ImageProperties:
    is_flipped_horz: bool=False
    is_flipped_vert: bool=False
    is_grayscaled: bool=False
    is_sepia = False

    original_image_width: int=0
    original_image_height: int=0

    altered_image_width: int=0
    altered_image_height: int=0

    rotation: int=0
    brightness: int=0
    contrast: int=1
    saturation: float=0
    blur_size: int=0
    hue: float=0
