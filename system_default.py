from dataclasses import dataclass

@dataclass
class SystemDefaults:
    zoom_percentatge: int = 100
    autosave: bool = True
    autosave_interval: int = 5
    autosave_location: str = ""
    autosave_filename: str = ""
    app_theme: str = "dark"
    history_size: int = 10