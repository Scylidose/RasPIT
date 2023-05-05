import os
import subprocess
import pyautogui

def open_file(file_path):
    if os.path.exists(file_path):
        if os.name == 'nt':  # Windows
            os.startfile(file_path)
        elif os.name == 'posix':  # macOS and Linux
            subprocess.call(['open', file_path])
        return True
    else:
        return False

def start_program(program_name):
    try:
        subprocess.Popen(program_name)
        return True
    except FileNotFoundError:
        return False

def execute_remote_action(action, *args, **kwargs):
    action_mapping = {
        'open_file': open_file,
        'start_program': start_program,
    }

    if action in action_mapping:
        return action_mapping[action](*args, **kwargs)
    else:
        return False
