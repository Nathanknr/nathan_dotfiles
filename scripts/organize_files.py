from pathlib import Path
import shutil
import os
# Inspired by https://dev.to/gagangulyani/automating-my-workflow-with-python-1-file-organizer-40po
dirs = {
    # Images
    "jpeg": "Images",
    "jpg": "Images",
    "png": "Images",
    "gif": "Images",
    "tiff": "Images",
    "tif": "Images",
    "bmp": "Images",
    "webp": "Images",
    "svg": "Images",
    "ico": "Images",
    "heic": "Images",
    "heif": "Images",
    "raw": "Images",
    "cr2": "Images",
    "nef": "Images",
    "orf": "Images",
    "sr2": "Images",
    "psd": "Images",
    "ai": "Images",
    "eps": "Images",
    "indd": "Images",
    "xcf": "Images",
    "avif": "Images",

    # Videos
    "mp4": "Videos",
    "mkv": "Videos",
    "mov": "Videos",
    "webm": "Videos",
    "flv": "Videos",
    "avi": "Videos",
    "wmv": "Videos",
    "m4v": "Videos",
    "mpg": "Videos",
    "mpeg": "Videos",
    "3gp": "Videos",
    "ogv": "Videos",
    "vob": "Videos",
    "rm": "Videos",
    "asf": "Videos",

    # Music
    "mp3": "Music",
    "ogg": "Music",
    "wav": "Music",
    "flac": "Music",
    "aac": "Music",
    "wma": "Music",
    "m4a": "Music",
    "opus": "Music",
    "aiff": "Music",
    "alac": "Music",
    "mid": "Music",
    "midi": "Music",
    "amr": "Music",

    # Program Files
    "py": "Program Files",
    "js": "Program Files",
    "jsx": "Program Files",
    "ts": "Program Files",
    "tsx": "Program Files",
    "cpp": "Program Files",
    "cc": "Program Files",
    "cxx": "Program Files",
    "c": "Program Files",
    "h": "Program Files",
    "hpp": "Program Files",
    "html": "Program Files",
    "htm": "Program Files",
    "css": "Program Files",
    "scss": "Program Files",
    "sass": "Program Files",
    "less": "Program Files",
    "sh": "Program Files",
    "bash": "Program Files",
    "zsh": "Program Files",
    "java": "Program Files",
    "class": "Program Files",
    "jar": "Program Files",
    "kt": "Program Files",
    "go": "Program Files",
    "rs": "Program Files",
    "rb": "Program Files",
    "php": "Program Files",
    "swift": "Program Files",
    "sql": "Program Files",
    "json": "Program Files",
    "xml": "Program Files",
    "yaml": "Program Files",
    "yml": "Program Files",
    "toml": "Program Files",
    "ini": "Program Files",
    "cfg": "Program Files",
    "bat": "Program Files",
    "ps1": "Program Files",
    "lua": "Program Files",
    "r": "Program Files",
    "pl": "Program Files",
    "vb": "Program Files",
    "asm": "Program Files",
    "ipynb": "Program Files",

    # Documents
    "pdf": "Documents",
    "doc": "Documents",
    "docx": "Documents",
    "txt": "Documents",
    "rtf": "Documents",
    "odt": "Documents",
    "ppt": "Documents",
    "pptx": "Documents",
    "odp": "Documents",
    "xls": "Documents",
    "xlsx": "Documents",
    "ods": "Documents",
    "csv": "Documents",
    "tsv": "Documents",
    "md": "Documents",
    "epub": "Documents",
    "mobi": "Documents",
    "tex": "Documents",
    "log": "Documents",
    "pages": "Documents",
    "key": "Documents",
    "numbers": "Documents",

    # Miscellaneous (everything else: archives, installers, fonts, etc.)
    "zip": "Miscellaneous",
    "rar": "Miscellaneous",
    "7z": "Miscellaneous",
    "tar": "Miscellaneous",
    "gz": "Miscellaneous",
    "bz2": "Miscellaneous",
    "xz": "Miscellaneous",
    "tgz": "Miscellaneous",
    "iso": "Miscellaneous",
    "dmg": "Miscellaneous",
    "exe": "Miscellaneous",
    "msi": "Miscellaneous",
    "apk": "Miscellaneous",
    "deb": "Miscellaneous",
    "rpm": "Miscellaneous",
    "appimage": "Miscellaneous",
    "ttf": "Miscellaneous",
    "otf": "Miscellaneous",
    "woff": "Miscellaneous",
    "woff2": "Miscellaneous",
    "eot": "Miscellaneous",
    "torrent": "Miscellaneous",
    "url": "Miscellaneous",
    "lnk": "Miscellaneous",
    "bak": "Miscellaneous",
    "tmp": "Miscellaneous",
}

loc = Path("/home/nathan/Downloads")

for file in loc.iterdir():
    if file.is_file():
        extension = file.suffix[1:]
        # I get the associated doc type in dictionary
        folder = dirs.get(extension, "Miscellaneous")

        dest = loc/folder
        if not dest.exists():
                    dest.mkdir()
        try:
            shutil.move(file, loc/folder)
        except shutil.Error:
            os.remove(file)

            


