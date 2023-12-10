from dataclasses import dataclass

@dataclass
class ImageProperties:
    title: str=""
    time: str=""

    is_flipped_horz: bool=False
    is_flipped_vert: bool=False
    is_grayscaled: bool=False
    is_sepia: bool=False
    is_cropped: bool=False
    is_rotated: bool=False
    is_zoomed: bool=False

    original_image_width: int=0
    original_image_height: int=0

    altered_image_width: int=0
    altered_image_height: int=0

    resize_image_width: int=0
    resize_image_height: int=0

    zoom_scale_factor: float=0.0

    rotation: int=0

    brightness: int=50
    contrast: int=50
    saturation: float=0
    blur: int=0
    hue: float=0

    crop_start_x: float = 0
    crop_start_y: float = 0
    crop_end_x: float = 0
    crop_end_y: float = 0
    crop_ratio: float = 0.0
    crop_rectangle_width: float = 0
    crop_rectangle_height: float = 0

    at_time_canvas_width: float = 0
    at_time_canvas_height: float = 0

    pan_start_x: float = 0
    pan_start_y: float = 0
    pan_coord_x: float = 0
    pan_coord_y: float = 0