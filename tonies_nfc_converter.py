"""
This module provides functionality for converting old nfc tonies files from the flipper zero
to the current version 4 of the NFC files for SLIX Tags

"""

import os
import sys
from tkinter import Tk
from tkinter.filedialog import askdirectory, askopenfilename
from pathlib import Path
import jinja2

script_path = Path(sys.argv[0]).absolute()
currdir = script_path.parents[0]

def extract_uid_and_data_content(file_path):
    uid = None
    data_content = None

    with open(file_path, 'r', encoding='UTF-8') as nfc_file:
        for line in nfc_file:
            if line.startswith("#") or not line.strip():
                continue
            # Strip newline characters and split the line into key and value
            parts = line.strip().split(': ')
            if len(parts) != 2:
                continue
            key, value = parts
            # Check if the line contains the UID or DataContent
            if key == 'UID':
                uid = value
            elif key == 'Data Content':
                data_content = value
            
        if uid and data_content:
            file_content = {'uid': uid, 'data': data_content}
        else:
            file_content = {}

    return file_content

filetypes = [
    ("jinja2 template files", "*.jinja2")
]

root = Tk()
root.withdraw() # use to hide tkinter window
template_file = askopenfilename(parent=root, initialdir=currdir, title='Select Template File', filetypes=filetypes)
tonie_file_dir = askdirectory(parent=root, initialdir=currdir, title='Select Tonies Folder')

with open(template_file, encoding='UTF-8') as file_:
    template = jinja2.Template(file_.read(), line_comment_prefix='{=', comment_start_string='{=', comment_end_string='=}')
    abs_count = 0
    for root, dirs, files in os.walk(tonie_file_dir):
        count = 0
        for file in files:
            if file.endswith(".nfc"):
                file_name = os.path.join(root, file)
                file_content = extract_uid_and_data_content(file_name)
                if file_content:
                    count += 1
                    rendered_string = template.render(file_content)
                    new_file = open(file_name, 'w', encoding='UTF-8')
                    new_file.write(rendered_string)
                    new_file.close()
                else:
                    print(f'{file_name} could not be converted uid or data content missing')
        abs_count += count
    print(f"Done converting {abs_count} files")
