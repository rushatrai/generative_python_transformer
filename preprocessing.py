import os
import re
from tqdm import tqdm
from black import format_str, FileMode
from curtsies.fmtfuncs import red


paths = []

for dirpath, dirnames, filenames in os.walk("repos"):
  for f in filenames:
    path = os.path.join(dirpath, f)
    paths.append(path)

print(len(paths))  # number of .py files

MAX_CHAR_LENGTH = 512
MIN_CHAR_LENGTH = 400

NEWLINE_CHAR = "<N>"

with open("py_txt_file.txt", 'a') as py_txt_file:
  for path in tqdm(paths):
    try:
      # opens file as string
      f = open(path, 'r').read()
    except:  # in case of errors while trying to read file
      print(red(f"Error while reading file at {path}. Skipping..."))
      continue

    try:
      # converts code to standard format
      formatted_f = format_str(f, mode=FileMode())
    except:  # in case of random errors while formatting files
      print(red(f"Error while formatting file at {path}. Skipping..."))
      continue

    # removes block comments
    final_string = []
    for line in formatted_f.splitlines():
        if not line.strip().startswith("#"):
          final_string.append(line)
    formatted_f = "\n".join(final_string)

    # replaces newline delimiter (we want a single string)
    formatted_f = formatted_f.replace("\n", NEWLINE_CHAR)  

    if 100 < len(f) <= MAX_CHAR_LENGTH:  # if file is already within the character limit (and not too small)
      py_txt_file.write(formatted_f+"\n")
    else:
      split_f = formatted_f.split(f"{NEWLINE_CHAR}{NEWLINE_CHAR}")  # splits file on double newlines
      substring = ''
      for split in split_f:
        substring += split + f"{NEWLINE_CHAR}{NEWLINE_CHAR}"
        if MIN_CHAR_LENGTH <= len(substring) <= MAX_CHAR_LENGTH:  # if substring already fits requirements
          py_txt_file.write(substring+"\n")
          substring = ''
        elif len(substring) > MAX_CHAR_LENGTH:  # if substring is bigger than maxcharlength
          # calculates number of MIN_CHAR_LENGTH-sized chunks that can be formed from substring
          number_of_chunks = len(substring) // MIN_CHAR_LENGTH
          while len(substring) > MIN_CHAR_LENGTH:  # stops iteration if substring becomes smaller than required character length
            # finds closest newline character after MIN_CHAR_LENGTH
            newline_location = MIN_CHAR_LENGTH + substring[MIN_CHAR_LENGTH:].find(NEWLINE_CHAR)
            # finds where next chunk begins
            next_chunk_idx = newline_location+len(NEWLINE_CHAR)+1
            # forms chunk from MIN_CHAR_LENGTH to next closest newline character
            chunk = substring[:MIN_CHAR_LENGTH] + substring[MIN_CHAR_LENGTH:next_chunk_idx]
            # writes chunk to file
            py_txt_file.write(chunk+"\n")
            # forwards remaining part of substring to the next iteration
            substring = substring[next_chunk_idx:]
          substring = ''
