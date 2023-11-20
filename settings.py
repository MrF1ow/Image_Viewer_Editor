import tkinter as tk
from tkinter import ttk
from tkinter import Toplevel, filedialog, LEFT

class Settings(Toplevel):
    def __init__(self, master=None):
        Toplevel.__init__(self, master=master)
        self.title("Settings")
        
        # Need to either declare system default or, if system defaults are already declared, need to get that variable.
        
        # Dictionary to hold references to widget variables
        self.settings_vars = {} # Key: settings name; Value: widget
        
        self.create_widgets()

    def create_widgets(self):
        zoom_options = ["25%", "50%", "75%", "100%", "125%", "150%"]
        image_resolution_options = [    
            "640x480",    # VGA
            "800x600",    # SVGA
            "1024x768",   # XGA
            "1280x720",   # HD
            "1280x800",   # WXGA
            "1366x768",   # HD
            "1440x900",   # WXGA+
            "1600x900",   # HD+
            "1680x1050",  # WSXGA+
            "1920x1080",  # Full HD
            "1920x1200",  # WUXGA
            "2560x1440",  # Quad HD
            "2560x1600",  # WQXGA
            "3840x2160"   # 4K UHD
            ]
        export_format_options = [".png", ".jpeg", ".jpg", ".giff", ".bmp", ".tiff"]
        
        # This variable allows us to avoid hand coding each new settings item. Instead, we can loop through this array.
        settings_title_and_widgets = [ 
            ("Dark Mode", "CheckbuttonType", None ),
            ("Auto Save Allowed", "CheckbuttonType", None),
            ("Default Image Resolution", "ComboboxType", image_resolution_options),
            ("Default Export Format", "ComboboxType", export_format_options),
            ("Zoom Percentage", "ComboboxType", zoom_options),
            ("Default File Location", "EntryType", None),
            ("Save Current Filters as Defaults", "CheckbuttonType", None), 
            ("Reset Settings", "CheckbuttonType", None)
        ]
        
        # Looping through settings_title_and_widgets array and accessing the information: name, type, option.
        for settings_name, widget_type, widget_options in settings_title_and_widgets:
            label = tk.Label(self, text=settings_name)
            label.grid(row=len(self.settings_vars), column=0, padx=10, pady=5, sticky=tk.W)
            
            widget_var = tk.StringVar()
            
            if widget_type == "ComboboxType":
                widget = ttk.Combobox(self, textvariable=widget_var, values=widget_options, state='readonly')
                widget.grid(row=len(self.settings_vars), column=1, padx=10, pady=5, sticky=tk.W)
            elif widget_type == "EntryType": 
                widget = tk.Entry(self, textvariable=widget_var, state='readonly')
                widget.grid(row=len(self.settings_vars), column=1, padx=10, pady=5, sticky=tk.W + tk.E)
                browse_button = tk.Button(self, text="Browse", command=self._browse_file)
                browse_button.grid(row=len(self.settings_vars), column=2, padx=10, pady=5, sticky=tk.W)
                widget.config(state='readonly')  # Disable direct editing
            elif widget_type == "CheckbuttonType":
                self.checkbox_var = tk.IntVar()
                widget = tk.Checkbutton(self, variable=self.checkbox_var)
                widget.grid(row=len(self.settings_vars), column=1, padx=10, pady=5, sticky=tk.W)
            elif widget_type == "ButtonType":
                widget = tk.Button(self, text=settings_name, command=self._apply_button(settings_name))
                widget.grid(row=len(self.settings_vars), column=2, padx=10, pady=5, sticky=tk.W)
                
            self.settings_vars[settings_name] = widget_var


        # Adding a blank label to create space.
        space_label = tk.Label(self, text="")
        space_label.grid(row=len(self.settings_vars), column=0, pady=10, columnspan=2)
    
        # Creating and formatting the "Apply" and "Cancel" buttons.
        apply_settings_button = tk.Button(self, text="Apply", command=self._apply_current_settings)
        apply_settings_button.grid(row=len(self.settings_vars) + 1, column=0, padx=10, pady=10, sticky=tk.W)
        clear_settings_button = tk.Button(self, text="Clear", command=self._clear_current_settings)
        clear_settings_button.grid(row=len(self.settings_vars) + 1, column=0, padx=0, pady=10, sticky=tk.E)
        self.settings_vars["Apply"] = apply_settings_button
        self.settings_vars["Clear"] = clear_settings_button
        
        print("SETTINGS VARS variable")
        print(self.settings_vars) # TESTING
        
    def _apply_current_settings(self):
        # This is the apply button that will tak everything in settings and apply it (edit the config file and apply the changes).
        pass
    
    def _clear_current_settings(self):
        # Just close the window and do not save changes.
        pass
    
    def _browse_file(self):    
        # Open file dialog for selecting a file location
        file_path = filedialog.askdirectory()
        if file_path:
            # Update the Entry widget with the selected file path
            self.settings_vars["Default File Location"].set(file_path)        
        
            