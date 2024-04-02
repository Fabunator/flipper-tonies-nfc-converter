# flipper tonies nfc converter

(Python) Tool to convert old nfc tonies files from the flipper zero
to the current version 4 of the NFC files for SLIX Tags

## Preparation

Copy all the tonies nfc files into one directory on your computer.

## Usage

```sh
pip install -r requirements.txt 
python tonies_nfc_cconverter.py
```

After the start the programm requests two inputs.

1. the location of the template file for version 4 NFC SLIX Files
2. the location of the .nfc files from the flipper zero

The program then reads the UID and Data Content from the file and inserts this information into the new version 4 file from the template.
The old file is replaced with the new version 4 file.
