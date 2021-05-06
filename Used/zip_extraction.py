import sys
import subprocess
import os

# Get the current directory
if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)

# Get the path for 7zip
zip_path = str(application_path) + str(r'\7za.exe')

# Dictionary for raw string function
_dRawMap = {8: r'\b', 7: r'\a', 12: r'\f', 10: r'\n', 13: r'\r', 9: r'\t', 11: r'\v'}


def get_raw_string(s: str) -> str:
    """Takes a filepath string and turns it into a raw string"""
    return r''.join(_dRawMap.get(ord(c), c) for c in s)


def extract_files(zip_name):
    """Extracts the files using the 7zip exe"""
    system = subprocess.Popen([get_raw_string(zip_path), "x", "-y", zip_name])
    return system.communicate()


