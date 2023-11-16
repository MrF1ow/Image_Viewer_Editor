from dataclasses import dataclass

@dataclass
class ImageProperties:
    title: str=""
    time: str=""

    is_flipped_horz: bool=False
    is_flipped_vert: bool=False
    is_grayscaled: bool=False
    is_sepia = bool=False
    is_cropped: bool=False

    original_image_width: int=0
    original_image_height: int=0

    altered_image_width: int=0
    altered_image_height: int=0

    rotation: int=0

    brightness: int=50
    contrast: int=50
    saturation: int=0
    blur: int=0
    hue: float=50

    crop_start_x: int = 0
    crop_start_y: int = 0
    crop_end_x: int = 0
    crop_end_y: int = 0
    crop_ratio: float = 0.0

