# -*- coding: utf-8 -*-
""" A simple script to convert a file of EUC-KR files to UTF-8.

This script converts all .txt files in a provided folder from EUC-KR to UTF-8 and copies them to an output folder.
Provide the source folder and an optional output folder name to which to rewrite the files.
This output folder defaults to the provided name + "_utf8".

Created by Jay Kaiser, 2019-04-04.
Email at jayckaiser@gmail.com .
Use or modify this however you like.

"""

import logging
import os
import sys


# Prepare the logger to output messages.
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("euckr_to_utf8")


# This is a helper function for copy_as_utf8.
# The completes the actual file rewrite.
def do_the_copy(output_path, text):

    # Create the parent folder to the file (if it doesn't already exist).
    parent_folder = "/".join( output_path.split("/")[:-1] )
    os.makedirs(parent_folder, exist_ok=True)

    # Write the contents as UTF8.
    with open(output_path, 'w', encoding='UTF8') as OUTPUT_FILE:
        OUTPUT_FILE.write(text)

    return []


# Copies the file in filepath to the same path in DEST_FOLDER as UTF8 format.
# input_dir and output_dir are single folder names, NOT filepaths.
def copy_as_utf8(filepath, input_dir, output_dir):

    # Change the filepath only with the OUTPUT_DIRECTORY.
    # Replace only the last instance (just in case).
    # The strings are reversed and unreversed to replace the LAST instance of input_dir.
    output_path = filepath[::-1]
    output_path = output_path.replace(input_dir[::-1], output_dir[::-1], 1)
    output_path = output_path[::-1]

    try:
        # Open the original filepath (assuming a EUC-KR encoding.)
        with open(filepath, 'r', encoding="EUC-KR") as INPUT_FILE:
            text = INPUT_FILE.read()

        return do_the_copy(output_path, text)


    except UnicodeDecodeError:  # It must be in a different encoding...

        try:
            # Open the original filepath (assuming a UTF8 encoding.)
            with open(filepath, 'r', encoding="UTF8") as INPUT_FILE:
                text = INPUT_FILE.read()

            return do_the_copy(output_path, text)


        # This is not a proper EUC-KR or UTF8 file.
        except UnicodeDecodeError:

            # Return the failed filepath to output in a failure file.
            return [filepath]


    # Something beyond the scope of this script failed.
    except Exception as e:
        logger.error("  Something failed! Maybe the filepath is wrong? :: {}".format(e))
        sys.exit()
    


# Walk through all subdirectories and retrieve a list of .txt files.
def list_txt_files(source_folder):
    # Note: this has been copied directly from the following URL:
    # "https://www.mkyong.com/python/python-how-to-list-all-files-in-a-directory/"
    # However, I have converted it into a generator.

    # r=root, d=directories, f=files
    for r, _, f in os.walk(source_folder):
        for file in f:
            if '.txt' in file:
                yield os.path.join(r, file)



if __name__ == "__main__":

    # Read in the command line arguments.
    if len(sys.argv) == 3:  # An optional OUTPUT_DIRECTORY has been provided.
        (_, SOURCE_DIRECTORY, OUTPUT_DIRECTORY) = sys.argv
        INPUT_DIRECTORY = SOURCE_DIRECTORY.split("/")[-1]

    elif len(sys.argv) == 2: # No OUTPUT_DIRECTORY Has been provided. Use the default option.
        (_, SOURCE_DIRECTORY) = sys.argv
        INPUT_DIRECTORY = SOURCE_DIRECTORY.split("/")[-1]
        OUTPUT_DIRECTORY = INPUT_DIRECTORY + "_utf8"
    
    else:
        logger.error("  You've either provided zero or too many arguments.")
        sys.exit()


    # Check if the folder actually exists (just in case).
    if not os.path.exists(SOURCE_DIRECTORY):
        logger.error("  The input folder filepath you provided does not exist.")
        sys.exit()


    # Complete the full rewrite, keeping track of number of files parsed and files failed.
    total_files = 0
    failures = []

    # Iterate through the .txt files and attempt to rewrite them.
    for file in list_txt_files(SOURCE_DIRECTORY):
        total_files += 1
        failures += copy_as_utf8(file, INPUT_DIRECTORY, OUTPUT_DIRECTORY) 

    total_failures = len(failures)

    # Pad the failures with newlines for proper lines-writing.
    failures = [f + "\n" for f in failures]

    # Write the debug file listing the files that failed conversion.
    base_folder = "/".join( SOURCE_DIRECTORY.split("/")[:-1] )
    error_files_path = os.path.join(base_folder, "FAILED_FILES.txt")

    with open(error_files_path, "w") as ERROR_FILE:
        ERROR_FILE.writelines(failures)
    
    # Print out some statistics.
    logger.info("  Files in total: {}".format( total_files ))
    logger.info("  Failed files  : {}".format( total_failures ))
    logger.info("  Success ratio : {}".format( (total_files - total_failures) / total_files ))
    sys.exit()