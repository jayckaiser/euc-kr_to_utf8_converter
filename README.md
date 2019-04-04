# euc-kr_to_utf8_converter
This is just a little script I wrote to convert a directory of EUC-KR files to UTF8.
The KAIST corpus comes in a mix of EUC-KR and UTF8 files, so I needed to convert them to UTF8 for easy processing.

Use `python euckr_to_utf8.py SOURCE_FOLDERPATH OUTPUT_FOLDERNAME` to convert them.
OUTPUT_FOLDERNAME is optional and will be written to the same directory as the source folder is found.
Defaults to source_folder + "_utf8" if no OUTPUT_FOLDERNAME is provided.
