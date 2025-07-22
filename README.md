# Py2exe Framework

> **Language**: [English](README.md) | [中文](README.zh.md)

![Python](https://img.shields.io/badge/python-3.9.12-blue.svg)
![PyInstaller](https://img.shields.io/badge/PyInstaller-6.14.1-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

A framework that helps you quickly package your Python projects into standalone `.exe` executable files using PyInstaller. Supports both GUI interface version and background running version.

<br>

## 📚 Table of Contents

- [Framework Features](#-framework-features)
- [Project Structure](#-project-structure)
- [Quick Start](#-quick-start)
- [Integrating Your Own Code](#%EF%B8%8F-integrating-your-own-code)
- [Package Code to EXE](#-package-code-to-exe)
- [Common Issues](#-common-issues)
- [License](#-license)

<br>

## ✨ Framework Features

- 🖥️ **GUI Interface Support**: Provides a user-friendly graphical interface that supports parameter modification, configuration saving, and real-time log output
- 🔧 **Background Running Mode**: Silent background execution with JSON file configuration, popup notification when completed
- 📝 **Comprehensive Logging System**: Integrated logging module for easy debugging and troubleshooting
- 🎨 **Custom Fonts**: Support for loading custom font files to enhance interface aesthetics
- 🛡️ **Exception Handling**: Comprehensive exception handling and process management

<br>

## 📁 Project Structure

```
py2exe-framework/
├── src/                         # Source code folder
│   ├── gui/                     # GUI interface version
│   │   ├── main.py              # Your main business logic code
│   │   ├── run_gui.py           # GUI interface entry point
│   │   ├── my_logger.py         # Logging module
│   │   ├── config.json          # Configuration file
│   │   ├── icon.ico             # Application icon
│   │   └── generate_exe.sh      # GUI version packaging script
│   └── background/              # Background running version
│       ├── main.py              # Your main business logic code
│       ├── run_background.py    # Background running entry point
│       ├── my_logger.py         # Logging module
│       ├── config.json          # Configuration file
│       ├── icon.ico             # Application icon
│       └── generate_exe.sh      # Background version packaging script
├── fonts/                       # Font folder
│   ├── README.md                # Font usage instructions
│   └── SarasaMonoSC-Regular.ttf # Example font file
├── examples/                    # Test data folder
│   └── sample_data.csv          # Test data file
└── LICENSE                      # License file
```

<br>

## 🚀 Quick Start

### 1. Environment Setup

```bash
# Ensure Python is installed (recommended 3.9 or higher)
python --version

# Install PyInstaller
pip install pyinstaller

# Install other dependencies (based on your code requirements, only pandas is needed for direct use of test cases)
pip install pandas
```

### 2. Download Repository

```bash
git clone <repo-url>
cd py2exe-framework
```

### 3. Quick Test
**(1) <u>GUI Interface Version</u>**
- Features: Graphical interface operation, user-friendly
- Functions: Directly modify parameters, save configurations, and view real-time log output in the interface
```bash
cd src/gui
python run_gui.py
```
- After startup, a graphical interface will open
- You can modify parameters and save them in the interface
- Click the run button to view real-time output

**(2) <u>Background Running Version</u>**
- Features: Silent background execution, no interface interference
- Functions: Set parameters by modifying JSON configuration files, popup notification when execution is complete
```bash
cd src/background
python run_background.py
```
- The program will run silently in the background
- Popup notification when execution is complete
- Check log files for detailed execution information

<br>

## 🛠️ Integrating Your Own Code
Choose the mode you want to use:
- GUI interface version, enter the `src/gui` folder
- Background running version, enter the `src/background` folder

### 1. Configure Parameters

Modify the `config.json` file: The current content is only an example, you can set parameters according to actual conditions.

```json
{
  "logs_folder": "",
  "custom_param_1": "...",
  "custom_param_2": "...",
  "custom_param_3": "..."
}
```

**Note:**
- Please fill in all parameters that need user configuration. If no default value is provided, you can fill in empty string placeholders first.
- Supports basic data types such as strings, numbers, and boolean values; for Windows paths, use double backslashes `\\` or forward slashes `/`.
- `logs_folder` is a fixed parameter:
  - If you don't need log files, you can delete this parameter, and the program will still run normally;
  - If you want to generate log files, keep this parameter, and log files will be saved to the specified folder with filename format: `logger_YYYYMMDD_HHMMSS.log`. Usage example in code:

    ```python
    from my_logger import logger

    def some_function():
        logger.info("Program started")
        logger.warning("This is a warning")
        logger.error("This is an error")
        logger.debug("Debug information")
    ```

### 2. Put Your Code in the Folder
Put your own code in the folder (`src/gui` or `src/background`). If there are hierarchical relationships, they can be retained, as long as `main.py` is guaranteed to be the main entry point. Edit the `main_process` function to ensure that this function calls the main process of your code.

**Note:** All parameters set in `config.json` or filled in by users in the GUI interface will be passed to the `main_process` function in `dict` format.

```python
def main_process(args_dict: dict) -> None:
    """
    Your main business logic function
    """    
```

### 3. Interface Customization (GUI Interface Version Only)

- Customize application name

    Modify in `src/gui/run_gui.py`:

    ```python
    application_name = "Your Application Name"  # Modify here
    ```

- Add custom fonts
  - Put font files (`.ttf` or `.otf`) in the `fonts/` folder
  - Use in the `preferred_fonts` configuration in `run_gui.py`:

    ```python
    preferred_fonts = {
        'default': [
            ("Your Font Name", 10),
            ("Microsoft YaHei", 10)  # Backup font
        ],
    }
    ```

### 4. Running
**(1) <u>GUI Interface Version</u>**
```bash
python run_gui.py
```
After starting the GUI interface, you will see:

- **Configuration Parameter Area**: Displays all parameters in the current `config.json`
   - You can directly modify parameter values in the interface
   
- **Operation Buttons**:
   - `Load Config`: Load configuration parameters from `config.json` file again
   - `Save Config`: Save current interface parameters to `config.json` file
   - `Run Program`: Execute main program logic

- **Program Output Area**: Real-time display of program execution process
   - Display log information (info, warning, error, etc.)
   - Display program print output
   - Support scrolling to view historical output

**(2) <u>Background Running Version</u>**
```bash
python run_background.py
```
- After program startup, it will read the `config.json` configuration file
- Silently execute the business logic in the `main_process` function
- A prompt window will pop up to inform the execution result after program completion
- **Note**: Manually edit the `src/background/config.json` file before running, modify the required parameter values, save the file and then run the program

<br>

## 📦 Package Code to EXE

### 1. Preparation

- Ensure the program runs normally
- Check if all dependencies are installed
- Confirm configuration file paths are correct

### 2. Windows System Packaging

**(1) <u>GUI Interface Version</u>**

```bash
cd src/gui

# Method 1: Use provided script
generate_exe.sh

# Method 2: Manual execution
pyinstaller --onefile --noconsole --icon=icon.ico run_gui.py
```

**(2) <u>Background Running Version</u>**

```bash
cd src/background

# Method 1: Use provided script
generate_exe.sh

# Method 2: Manual execution
pyinstaller --onefile --noconsole --icon=icon.ico run_background.py
```

**(3) Packaging Parameter Description**

- `--onefile`: Package into a single exe file
- `--noconsole`: Don't display console window (suitable for GUI version and background silent running)
- `--icon=icon.ico`: Set exe file icon

**(4) Post-packaging Processing**

- After packaging is complete, find the generated `.exe` file in the `dist/` folder
- Copy the `.exe` file to the target location
  - **GUI version**: Copy `config.json` to the same directory as exe (users can modify parameters in the interface)
  - **Background version**: Ensure `config.json` is configured correctly and then copy to the same directory as exe
- Delete unnecessary `build/` and `dist/` folders and `.spec` files

### 3. Linux System Packaging (Testing)

- If you need to package Windows exe on Linux:

    ```bash
    # Install wine
    sudo apt update
    sudo apt install wine

    # Use wine to run PyInstaller
    wine C:/Python38/Scripts/pyinstaller.exe run_background.py --icon="icon.ico" --onefile
    ```
- `.spec` file
    ```
    a = Analysis(
        ['objdictedit.py'],    # List of main programs or script files. Only one file 'objdictedit.py' here.
        pathex=[],             # Specify Python interpreter search paths. Empty list here means using default search paths.
        binaries=[],           # List of binary files included in the package. No binary files specified here.
        datas=[
        ('config/DS-302.prf', 'config'),
        ('config/DS-401.prf', 'config'),
        ],
        hiddenimports=[],      # List of hidden import modules that need to be explicitly specified. No hidden import modules specified here.
        hookspath=[],          # List of hook file paths for handling specific module import issues. Empty list here means no additional hook paths.
        hooksconfig={},        # Dictionary of hook configuration options for customizing import hook behavior. Empty dictionary here means no specific hook configuration.
        runtime_hooks=[],      # List of runtime hooks that modify import behavior at runtime. Empty list here means no runtime hooks.
        excludes=[],           # List of modules excluded from packaging. Empty list here means no modules to exclude.
        noarchive=False,       # Controls whether to package Python source code into archives. Set to False here means allowing Python source code to be packaged into archives.
        optimize=0,            # Optimization level, controls the optimization level of generated bytecode. Set to 0 here means no optimization.
    )
    ```

<br>

## 🐛 Common Issues

### 1. Exe cannot run after packaging

**Solution**:
- Check if dependency files are missing
- Ensure all paths use absolute paths
- Ensure Python can run the program smoothly

### 2. Cannot find configuration file

**Solution**:
- Ensure `config.json` is in the same directory as the exe file
  - GUI version: Can reload configuration file in the interface
  - Background version: Must be in the same directory as the exe file

### 3. Background version doesn't show popup after running

**Solution**:
- Check if the program completed execution normally
- Check log files to confirm program status
- Ensure the program is not stuck at some step

### 4. Program crashes

**Solution**:
- Ensure the main entry has comprehensive exception handling:
```python
if __name__ == '__main__':
    try:
        # Your code
        pass
    except Exception as e:
        logger.error(f"Program exception: {e}")
        input("Press Enter to exit...")
```

### 5. Other Notes
- Don't have `__init__.py` in the folder where `main.py` is located, otherwise there will be path issues

<br>

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
