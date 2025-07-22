import json
import os
import sys
import threading
import tkinter as tk
import tkinter.font as tkFont
from tkinter import filedialog, messagebox, scrolledtext, ttk

from main import main_process
from my_logger import setup_logger

try:
    import ctypes
    HAS_FONT_LOADING = True
except ImportError:
    HAS_FONT_LOADING = False

application_name = "Your Application Name"  # TODO: Replace with your application name


class ConfigGUI:

    def __init__(self, root_path: str):

        self.root_path = root_path
        self.config_file = os.path.join(root_path, 'config.json')

        # Create main window
        self.root = tk.Tk()
        self.root.title(application_name)
        self.root.geometry("800x600")
        self.root.resizable(True, True)

        # Load local font files
        self._load_local_fonts()

        # Font settings - you can modify fonts here
        # First font is preferred, others are fallback fonts
        # Note: local font files in fonts/ folder will be loaded automatically
        preferred_fonts = {
            'default': [
                ("Sarasa Mono SC", 10),  # If you put SarasaMonoSC.ttf in fonts/ folder
                ("Microsoft YaHei", 10)  # System font fallback
                ],
            'title': [("Sarasa Mono SC", 16, "bold"), ("Microsoft YaHei", 16, "bold"), ],
            'button': [("Sarasa Mono SC", 9), ("Microsoft YaHei", 9), ],
            'log': [("Sarasa Mono SC", 9), ("Microsoft YaHei", 9), ]
            }

        # Auto-select available fonts
        self.default_font = self._get_available_font(preferred_fonts['default'])
        self.title_font = self._get_available_font(preferred_fonts['title'])
        self.button_font = self._get_available_font(preferred_fonts['button'])
        self.log_font = self._get_available_font(preferred_fonts['log'])

        # Configuration data
        self.config_data = {}
        self.config_vars = {}

        # Create interface
        self.create_widgets()

        # Load configuration
        self.load_config()

    def _load_local_fonts(self):
        """
        Load font files from project folder
        Supported font formats: .ttf, .otf
        """
        if not HAS_FONT_LOADING:
            return

        # Font files folder path
        fonts_dir = os.path.join(self.root_path, 'fonts')

        if not os.path.exists(fonts_dir):
            return

        # Supported font formats
        font_extensions = ['.ttf', '.otf', '.TTF', '.OTF']

        # Iterate through font folder
        for filename in os.listdir(fonts_dir):
            if any(filename.endswith(ext) for ext in font_extensions):
                font_path = os.path.join(fonts_dir, filename)
                try:
                    # Use Windows API to load font file
                    gdi32 = ctypes.windll.gdi32
                    result = gdi32.AddFontResourceW(font_path)
                    if result:
                        print(f"Successfully loaded font: {filename}")
                    else:
                        print(f"Failed to load font: {filename}")
                except Exception as e:
                    print(f"Error loading font {filename}: {e}")

        # Refresh font cache
        try:
            ctypes.windll.user32.PostMessageW(0xFFFF, 0x001D, 0, 0)  # WM_FONTCHANGE
        except:
            pass

    def _get_available_font(self, font_list):
        """
        Select the first available font from font list
        
        :param font_list: Font list, each element is (font_name, size) or (font_name, size, style)
        :return: First available font tuple
        """
        available_fonts = tkFont.families()

        for font in font_list:
            font_name = font[0]
            if font_name in available_fonts:
                return font

        # If no font is found, return system default font
        return font_list[-1] if font_list else ("TkDefaultFont", 10)

    def create_widgets(self):
        """Create GUI components"""

        # Configure custom styles
        style = ttk.Style()

        # Configure button fonts
        style.configure('Custom.TButton', font=self.button_font)
        style.configure('Accent.TButton', font=self.button_font)

        # Configure label frame fonts
        style.configure('Custom.TLabelframe.Label', font=self.default_font)

        # Configure entry fonts
        style.configure('Custom.TEntry', font=self.default_font)

        # Create main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.columnconfigure(2, weight=1)

        # Title
        title_label = ttk.Label(main_frame, text=application_name, font=self.title_font, anchor="center")
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20), sticky=(tk.W, tk.E))

        # Configuration parameters area
        config_frame = ttk.LabelFrame(main_frame, text="Configuration Parameters", padding="10", style='Custom.TLabelframe')
        config_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        config_frame.columnconfigure(1, weight=1)

        # Store configuration frame reference
        self.config_frame = config_frame

        # Button area
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))

        # Buttons
        load_btn = ttk.Button(button_frame, text="Load Config", command=self.load_config)
        load_btn.configure(style='Custom.TButton')
        load_btn.pack(side=tk.LEFT, padx=(0, 5))

        save_btn = ttk.Button(button_frame, text="Save Config", command=self.save_config)
        save_btn.configure(style='Custom.TButton')
        save_btn.pack(side=tk.LEFT, padx=5)

        run_btn = ttk.Button(button_frame, text="Run Program", command=self.run_main_program)
        run_btn.configure(style='Accent.TButton')
        run_btn.pack(side=tk.RIGHT, padx=(5, 0))

        # Log output area
        log_frame = ttk.LabelFrame(main_frame, text="Program Output", padding="10", style='Custom.TLabelframe')
        log_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)

        # Log text box
        self.log_text = scrolledtext.ScrolledText(log_frame, height=10, width=70, font=self.log_font)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure main_frame row weights
        main_frame.rowconfigure(3, weight=1)

    def load_config(self):
        """Load configuration file"""
        try:
            if not os.path.exists(self.config_file):
                # Configuration file does not exist, force creation
                self._handle_missing_config()
                return

            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.config_data = json.load(f)

            # Validate configuration file content
            if not self.config_data or not isinstance(self.config_data, dict):
                raise ValueError("Invalid configuration file content")

        except Exception as e:
            self.log_message(f"Failed to load configuration: {e}")
            # Configuration loading failed, force user to handle
            self._handle_config_error(str(e))
            return

        self.update_config_widgets()
        self.log_message("Configuration loaded")

    def _handle_missing_config(self):
        """Handle missing configuration file"""
        self.log_message("Error: Configuration file does not exist!")

        result = messagebox.askyesno(
            "Configuration File Missing", f"Configuration file '{self.config_file}' does not exist.\n\n"
            "You must select an existing configuration file to continue.\n\n"
            "Click 'Yes' - Select existing configuration file\n"
            "Click 'No' - Exit program", icon='warning'
            )

        if result:  # Select existing configuration file
            self._select_config_file()
        else:  # Exit program
            self.log_message("User cancelled operation, program exits")
            self.root.destroy()

    def _handle_config_error(self, error_msg):
        """Handle configuration file loading error"""
        result = messagebox.askyesno(
            "Configuration File Error", f"Failed to load configuration file: {error_msg}\n\n"
            "You must select a valid configuration file to continue.\n\n"
            "Click 'Yes' - Select another configuration file\n"
            "Click 'No' - Exit program", icon='error'
            )

        if result:  # Select another configuration file
            self._select_config_file()
        else:  # Exit program
            self.log_message("User cancelled operation, program exits")
            self.root.destroy()

    def _select_config_file(self):
        """Select existing configuration file"""
        file_path = filedialog.askopenfilename(
            title="Select Configuration File", filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")], initialdir=self.root_path
            )

        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)

                if not isinstance(config_data, dict):
                    raise ValueError("Invalid configuration file format")

                # Update configuration file path and data
                self.config_file = file_path
                self.config_data = config_data
                self.update_config_widgets()
                self.log_message(f"Configuration file loaded: {file_path}")

            except Exception as e:
                self.log_message(f"Failed to load selected configuration file: {e}")
                messagebox.showerror("Error", f"Failed to load configuration file: {e}")
                # Recursive call, continue handling
                self._handle_missing_config()
        else:
            # User cancelled selection, exit program
            self.log_message("User cancelled configuration file selection, program exits")
            self.root.destroy()

    def update_config_widgets(self):
        """Update configuration parameter GUI components"""
        # Clear existing configuration components
        for widget in self.config_frame.winfo_children():
            if hasattr(widget, 'grid_info') and widget.grid_info():
                row = widget.grid_info()['row']
                if row > 0:  # Keep title row
                    widget.destroy()

        self.config_vars.clear()

        # Create input boxes for configuration parameters
        row = 1
        for key, value in self.config_data.items():
            # Parameter name label
            label = ttk.Label(self.config_frame, text=f"{key}:", font=self.default_font)
            label.grid(row=row, column=0, sticky=tk.W, pady=2)

            # Parameter value input box
            var = tk.StringVar(value=str(value))
            self.config_vars[key] = var
            entry = ttk.Entry(self.config_frame, textvariable=var, width=30, style='Custom.TEntry')
            entry.grid(row=row, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=2)

            row += 1

    def save_config(self):
        """Save configuration to file"""
        try:
            # Get current values from GUI
            for key, var in self.config_vars.items():
                self.config_data[key] = var.get()

            # Save to file
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config_data, f, indent=2, ensure_ascii=False)

            self.log_message("Input configuration saved to file")
            messagebox.showinfo("Success", "Configuration successfully saved to config.json")

        except Exception as e:
            self.log_message(f"Failed to save configuration: {e}")
            messagebox.showerror("Error", f"Failed to save configuration: {e}")

    def run_main_program(self):
        """Run main program function"""
        # Check if there is configuration data
        if not self.config_data:
            messagebox.showerror("Error", "No configuration data, please load configuration file first")
            return

        # Save current configuration first
        self.save_config()

        # Prepare parameters dictionary
        args_dict = self.config_data.copy()

        # Run main program function in new thread
        thread = threading.Thread(target=self._run_main_process_thread, args=(args_dict, ))
        thread.daemon = True
        thread.start()

        self.log_message("Starting main program...")
        self.log_message(f"Using parameters: {args_dict}")

    def _run_main_process_thread(self, args_dict):
        """Execute main program function in thread"""
        try:
            # Redirect output to GUI
            import io
            from contextlib import redirect_stderr, redirect_stdout

            # Create string buffers to capture output
            stdout_buffer = io.StringIO()
            stderr_buffer = io.StringIO()

            with redirect_stdout(stdout_buffer), redirect_stderr(stderr_buffer):
                # Call main program function directly
                main_process(args_dict)

            # Get output content
            stdout_content = stdout_buffer.getvalue()
            stderr_content = stderr_buffer.getvalue()

            # Display output
            if stdout_content:
                for line in stdout_content.split('\n'):
                    if line.strip():
                        self.log_message(line)

            if stderr_content:
                for line in stderr_content.split('\n'):
                    if line.strip():
                        self.log_message(f"Info: {line}")

            self.log_message("Main program execution completed")

        except Exception as e:
            self.log_message(f"Error occurred while running main program: {e}")
            import traceback
            self.log_message(f"Detailed error information: {traceback.format_exc()}")

    def log_message(self, message: str):
        """Add message to log area"""

        def update_log():
            self.log_text.insert(tk.END, f"{message}\n")
            self.log_text.see(tk.END)

        # Ensure GUI is updated in main thread
        self.root.after(0, update_log)

    def run(self):
        """Run GUI"""
        self.root.mainloop()


if __name__ == '__main__':
    try:
        # Determine root path
        if getattr(sys, 'frozen', False):
            root_path = str(os.path.dirname(sys.executable))
        else:
            root_path = str(os.path.dirname(os.path.abspath(__file__)))

        # Create and run GUI
        app = ConfigGUI(root_path)
        app.run()

    except Exception as e:
        messagebox.showerror("Error", f"Failed to start GUI: {e}")
        import traceback
        print(traceback.format_exc())
