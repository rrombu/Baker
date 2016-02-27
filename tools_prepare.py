from zipfile import ZipFile, ZIP_LZMA

filenames = ["ffprobe.exe",
             "mkvmerge.exe",
             "x264.exe"]

with ZipFile("baker_tools.zip", "w", compression=ZIP_LZMA) as z:
    for fpath in filenames:
        z.write(fpath)
