from dataclasses import dataclass

@dataclass
class ImageProperties:
    is_flipped_horz: bool=False
    is_flipped_vert: bool=False

    rotation: int=0

    brightness: int=0