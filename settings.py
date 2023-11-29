import tkinter as tk
from tkinter import ttk
from tkinter import Toplevel, filedialog, LEFT
from system_default import SystemDefaults


class Settings(Toplevel): 
    """Settings is a singleton class that only allows one instance."""
    _instance = None # Holds the single instance of the Settings class.
    _initialized = False # Checks whether the class has been initialized.

    def __new__(cls, master=None) -> bool:
        """
        Override the built-in python new initializer to ensure that the class is only created once.
        
        If the class has not been created yet, create the class. If it has, return the instance of the class.
        """
        if not cls._instance:
            cls._instance = super(Settings, cls).__new__(cls)
        return cls._instance
    
    """A class representing the settings window."""
    def __init__(self, master=None) -> None:
        if hasattr(self, "initialized"):
            return
        if not self._initialized:
            self._initialized = True
        """Initialize the Settings window."""
        Toplevel.__init__(self, master=master)
        self.title("Settings")
        self.withdraw()
        
        self.protocol("WM_DELETE_WINDOW", self.toggle_visibility)
        
        self.zoom_dropdown_options = ["25%", "50%", "75%", "100%", "125%", "150%"]

        self.image_resolution_dropdown_options = [    
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
        
        self.export_format_dropdown_options = [".png", ".jpeg", ".jpg", ".giff", ".bmp", ".tiff"]
        
        self.history_size_dropdown_options = [5, 10, 15, 20, 25, 30]

        # (Setting title, widget type, widget options)
        self.settings_title_widget_type_widget_option_and_system_default = [ 
            ("Dark Mode", "CheckbuttonType", None, SystemDefaults.dark_mode),
            ("Autosave Allowed", "CheckbuttonType", None, SystemDefaults.autosave_allowed),
            ("Default Image Resolution", "ComboboxType", self.image_resolution_dropdown_options, SystemDefaults.image_resolution),
            ("Default Export Format", "ComboboxType", self.export_format_dropdown_options, SystemDefaults.export_format),
            ("Zoom Percentage", "Int/Dropdown", self.zoom_dropdown_options, SystemDefaults.zoom_percentatge),
            ("Default File Location", "FileLocation", None, SystemDefaults.save_file_location),
            #("Save Current Filters as Defaults", "Button", None, None),  # Should presets be used instead of this button.
            ("History Size", "Int/Dropdown", self.history_size_dropdown_options, SystemDefaults.history_size),
            ("Reset Settings", "ButtonType", None, None)
        ]
        
        self.map_of_functions_to_buttons = {
            "Reset Settings": self._reset_settings
        }

        self.settings_vars = {} # Key: settings name; Value: widget
        self.create_widgets()

     
    def toggle_visibility(self) -> None:
        if self.is_settings_menu_on_screen():
            self.withdraw()
            self._set_focus_back_to_main_window()
        else:
            self.deiconify() 

        
    def is_settings_menu_on_screen(self) -> bool:
        return self.winfo_ismapped()


    def _set_focus_back_to_main_window(self) -> None:
        if self.master:
             self.master.master.focus_set()


    def create_widgets(self) -> None:
        """Create and layout widgets for the Settings window."""
        
        # Looping through settings_title_widget_type_widget_option_and_system_default array and accessing the information: name, type, option, default value to add.
        for settings_name, widget_type, widget_options, system_default_value in self.settings_title_widget_type_widget_option_and_system_default:
            widget_var = tk.StringVar()
            checkbox_var = tk.BooleanVar()
        
            
            # Checking the widget type to see how the widget will be created.
            if widget_type == "ComboboxType":
                self._create_label(settings_name=settings_name)
                self._create_combobox(widget_options=widget_options, system_default_value=system_default_value, widget_var=widget_var)
                self._add_widget_to_settings_vars(key=settings_name, value=widget_var)
                
            elif widget_type == "FileLocation": 
                self._create_label(settings_name=settings_name)
                self._create_file_location(system_default_value=system_default_value, widget_var=widget_var)
                self._add_widget_to_settings_vars(key=settings_name, value=widget_var)
            
            elif widget_type == "CheckbuttonType":
                self._create_label(settings_name=settings_name)
                self._create_checkbutton(checkbox_var=checkbox_var, system_default_value=system_default_value)
                self._add_widget_to_settings_vars(key=settings_name, value=checkbox_var)
                
            elif widget_type == "ButtonType":
                self._create_label(settings_name=settings_name)
                self._create_button(settings_name=settings_name, command=self.map_of_functions_to_buttons[settings_name])
            
            elif widget_type == "Int/Dropdown":
                self._create_label(settings_name=settings_name)
                self._create_input_combobox(widget_options=widget_options, system_default_value=system_default_value, widget_var=widget_var)
                self._add_widget_to_settings_vars(key=settings_name, value=widget_var)       
        
        self._add_blank_label_for_spacing()   
        self._create_apply_button()
        self._create_clear_button()
    
    
    def _add_widget_to_settings_vars(self, key, value) -> None:
        self.settings_vars[key] = value
        
    
    def _create_apply_button(self) -> None:
        apply_settings_button = self._initialize_button(text="Apply", command=self._apply_current_settings)
        self._insert_widget_using_grid(widget=apply_settings_button, row=len(self.settings_vars) + 1, column=0, padx=10, pady=10, sticky=tk.W)
        self._add_widget_to_settings_vars(key="Apply", value=apply_settings_button)

        
    def _create_clear_button(self) -> None:
        clear_settings_button = self._initialize_button(text="Clear", command=self._clear_current_settings)
        self._insert_widget_using_grid(widget=clear_settings_button, row=len(self.settings_vars), column=0, padx=0, pady=10, sticky=tk.E)
        self._add_widget_to_settings_vars(key="Clear", value=clear_settings_button)

    
    def _add_blank_label_for_spacing(self) -> None:
        space_label = self._create_space_label()
        self._insert_space_widget_using_grid(widget=space_label)
        self._add_widget_to_settings_vars(key="Blank Label", value=space_label)
    
    
    def _create_space_label(self) -> tk.Label:
        return tk.Label(self, text="")
    
    
    def _create_label(self, settings_name) -> None:
        widget = self._initialize_label(settings_name=settings_name)
        self._insert_widget_using_grid(widget=widget, row=len(self.settings_vars), column=0, padx=10, pady=5, sticky=tk.W)
    
       
    def _create_input_combobox(self, widget_options, system_default_value, widget_var) -> None:
        widget = self._initialize_combobox(widget_var=widget_var, widget_option=widget_options)
        self._insert_widget_using_grid(widget=widget, row=len(self.settings_vars), column=1, padx=10, pady=5, sticky=tk.W)
        self._set_value_for_widget(widget=widget, value=system_default_value)
        self._set_widget_config(widget=widget, state="normal")
    
    
    def _create_combobox(self, widget_options, system_default_value, widget_var) -> None:
        widget = self._initialize_combobox(widget_var=widget_var, widget_option=widget_options)
        self._insert_widget_using_grid(widget=widget, row=len(self.settings_vars), column=1, padx=10, pady=5, sticky=tk.W)
        self._set_value_for_widget(widget=widget, value=system_default_value)

    
    def _create_file_location(self, system_default_value, widget_var) -> None:
        widget = self._initialize_entry(widget_var)
        self._insert_widget_using_grid(widget=widget, row=len(self.settings_vars), column=1, padx=10, pady=5, sticky=tk.W + tk.E)
        self._set_value_for_widget(widget=widget_var, value=system_default_value)
        self._set_widget_config(widget=widget, state="readonly")            
        browse_button = self._initialize_button(text="Browse", command=self._browse_files)
        self._insert_widget_using_grid(widget=browse_button, row=len(self.settings_vars), column=2, padx=10, pady=5, sticky=tk.W)
        
        
    def _create_checkbutton(self, checkbox_var, system_default_value) -> None:
        self._set_value_for_widget(widget=checkbox_var, value=system_default_value)
        widget = self._initialize_checkbutton(variable=checkbox_var)  
        self._insert_widget_using_grid(widget=widget, row=len(self.settings_vars), column=1, padx=10, pady=5, sticky=tk.W) 


    def _create_button(self, settings_name, command) -> None:
        widget = self._initialize_button(text=settings_name, command=command)
        self._insert_widget_using_grid(widget=widget, row=len(self.settings_vars), column=1, padx=10, pady=5, sticky=tk.W)


    def _initialize_combobox(self, widget_var, widget_option) -> ttk.Combobox:
        return ttk.Combobox(self, textvariable=widget_var, values=widget_option, state="readonly")
    

    def _initialize_label(self, settings_name) -> tk.Label:
        return tk.Label(self, text=settings_name)
    

    def _initialize_entry(self, widget_var) -> tk.Entry:
        return tk.Entry(self, textvariable=widget_var, state="readonly")
  
    
    def _initialize_button(self, text, command) -> tk.Button:
        return tk.Button(self, text=text, command=command)
  
                
    def _initialize_checkbutton(self, variable) -> tk.Checkbutton:
        return tk.Checkbutton(self, variable=variable)   
  
                    
    def _insert_widget_using_grid(self, widget, row, column, padx, pady, sticky) -> None:
        widget.grid(row=row, column=column, padx=padx, pady=pady, sticky=sticky) 
  
   
    def _insert_space_widget_using_grid(self, widget) -> None:
        widget.grid(row=len(self.settings_vars) + 1, column=0, pady=10, columnspan=2)
      

    def _apply_current_settings(self) -> None:
        # This is the apply button that will take everything in settings and apply it (edit the config file and apply the changes).
        self.toggle_visibility()
    
    def _clear_current_settings(self) -> None:
        # Just close the window and do not save changes.
        self.toggle_visibility()
  
    
    def _browse_files(self) -> None:    
        # Open file dialog for selecting a file location
        file_path = filedialog.askdirectory()
        if file_path:
            # Update the Entry widget with the selected file path
            self.settings_vars["Default File Location"].set(file_path)        
        
    
    def _set_value_for_widget(self, widget, value) -> None:
        widget.set(value)
   
     
    def _set_widget_config(self, widget, state) -> None:
        valid_states = ["normal", "active", "disabled", "readonly"]
        if state in valid_states:
            widget.config(state=state)
    
    def _reset_settings(self):
        print("Use config manager class to pull config of default settings, update system_defaults and recreate the settings window.")
        