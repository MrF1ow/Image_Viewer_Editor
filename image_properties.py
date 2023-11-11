from dataclasses import dataclass

@dataclass
class ImageProperties:
    is_flipped_horz: bool=False
    is_flipped_vert: bool=False
    is_grayscaled: bool=False

    image_width: int=0
    image_height: int=0

    rotation: int=0
    brightness: int=1

    blur_size: int=0

    hue: float=0
