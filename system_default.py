from dataclasses import dataclass
import os

@dataclass
class SystemDefaults:
    dark_mode: bool = False
    zoom_percentatge: int = 100
    autosave_allowed: bool = True
    image_resolution: str = "1280x720"
    export_format: str = ".jpeg"
    autosave_interval: int = 5
    save_file_location: str = os.path.join(os.path.expanduser("~"), "Downloads") # Settings the default value to the users Downloads folder.
    autosave_filename: str = ""
    history_size: int = 10
    