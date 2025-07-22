from __future__ import annotations

import json
import os
import sys
import tkinter
import warnings
from tkinter import messagebox

import psutil
from main import main_process

warnings.filterwarnings('ignore')


def show_message(message: str) -> None:
    root = tkinter.Tk()
    root.withdraw()
    messagebox.showinfo('Notification', message)
    root.destroy()


def check_num_of_instances(threshold: int = 3) -> None:
    """
    check the number of running instances of this script
    
    :param threshold: the maximum number of allowed instances, default is 3
    :return: None
    """

    current_pid = os.getpid()
    current_name = os.path.basename(sys.executable if getattr(sys, 'frozen', False) else __file__)

    count = 0
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if current_name in str(proc.info['cmdline']) and proc.info['pid'] != current_pid:
                count += 1
                if count > threshold:
                    show_message(f"Multiple instances detected: current PID: {current_pid}, other PID: {proc.info['pid']}")
                    os.kill(proc.info['pid'], 9)
                    os._exit(1)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass


if __name__ == '__main__':
    try:
        if getattr(sys, 'frozen', False):
            root_path = str(os.path.dirname(sys.executable))
        else:
            root_path = str(os.path.dirname(os.path.abspath(__file__)))

        # check if the logs directory exists
        config_file = os.path.join(root_path, 'config.json')

        if os.path.exists(config_file):
            with open(config_file, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
        else:
            raise FileNotFoundError(f"Configuration file not found: {config_file}")

        # avoid multiple instances
        check_num_of_instances()

        # run the main function
        main_process(args_dict=config_data)

        show_message('Process completed successfully!')
        os._exit(1)

    except Exception as e:

        show_message(f"Error occurred: {e}")
        os._exit(1)
