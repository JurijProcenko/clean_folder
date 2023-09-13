""" Garbadge sorter
Take one argument - folder for sorting.
He's sorting and moving files to folders:
images, documents, video, audio, archives

"""

from sys import argv
import os
from pathlib import Path
import string
import shutil


# Rename file name from cyrillic to latin
def normalize(cyrillic_name: str, cyr_lat: dict) -> str:
    ext = cyrillic_name[cyrillic_name.rfind(".") :]
    cyrillic_name = cyrillic_name[: cyrillic_name.rfind(".")]
    name_out = ""
    # Convert cyrilic letters to latin, latin letters and
    # numbers remain as they are, other characters are replaced by the _ character
    for c in cyrillic_name:
        if c in string.ascii_letters or c in string.digits:
            name_out += c
        elif c in cyr_lat.keys() or c.lower() in cyr_lat.keys():
            if c.isupper():
                name_out += cyr_lat[c.lower()].upper()
            else:
                name_out += cyr_lat[c]
        else:
            name_out += "_"
    return name_out + ext


# def rename_all_files():
#     dest_folders.pop("unknown")
#     for key in dest_folders:
#         os.chdir(dest_folders[key])
#         for next_file in Path.cwd().glob("*.*"):
#             name = str(next_file.name)
#             next_file.replace(normalize(name))


def make_dir(dest_folders):
    for key in dest_folders:
        try:
            os.mkdir(dest_folders[key])
        except:
            pass


def confirm_replace(source_file: Path, dest: Path, new_dest: Path = None):
    add_sym = " Copy"
    if not new_dest:
        name = str(source_file.name)
    else:
        name = str(new_dest.name)
    ext = name[name.rfind(".") :]
    new_name = name[: name.rfind(".")]
    new_name = new_name + add_sym + ext
    new_dest = dest.with_name(new_name)
    try:
        os.rename(source_file, new_dest)
    except:
        confirm_replace(source_file, dest, new_dest)


def make_heap(home: Path, dest_folders: dict, cyr_lat: dict):
    try:
        os.mkdir(dest_folders["unknown"])
    except:
        pass
    for next_file in home.rglob("*"):
        if next_file.is_file():
            name = normalize(str(next_file.name), cyr_lat)
            try:
                os.rename(next_file, dest_folders["unknown"].joinpath(name))
            except:
                confirm_replace(next_file, dest_folders["unknown"].joinpath(name))


def move_files(home: Path, dest_folders: dict, extentions: dict, known_ext: set) -> set:
    for key in extentions:
        for ext in extentions[key]:
            for next_file in home.glob(f"**/*.{ext}"):
                name = next_file.name
                known_ext.add(str(next_file)[str(next_file).rfind(".") + 1 :].lower())
                try:
                    os.rename(next_file, dest_folders[key].joinpath(name))
                except:
                    confirm_replace(next_file, dest_folders[key].joinpath(name))
    return known_ext


def find_unknown_ext(dest_folders: dict, known_ext: set, unknown_ext: set) -> set:
    # Собираем неизвестные расширения в множество
    for next_file in Path(dest_folders["unknown"]).glob("*.*"):
        name = next_file.name
        ext = next_file.suffix
        next_file = str(next_file)
        if ext not in known_ext:
            unknown_ext.add(next_file[next_file.rfind(".") + 1 :].lower())
    return unknown_ext


def remove_empty_folders(source_folder):
    for root, dirs, files in os.walk(source_folder, topdown=False):
        for d in dirs:
            curpath = os.path.join(root, d)
            if not os.listdir(curpath):
                os.rmdir(curpath)


def unpack_archives(dest_folders: dict):
    for next_file in Path(dest_folders["archives"]).glob("*.*"):
        name = str(next_file)
        dest = name[: name.rfind(".")] + "\\"
        os.mkdir(dest)
        zip_command = f"tar -C {dest} -xf {name}"
        try:
            os.system(zip_command)
        except:
            print(f"Something wrong with file {name}")
    for next_file in Path(dest_folders["archives"]).glob("*.*"):
        if next_file.is_file():
            next_file.unlink()


def main():
    # Taking an argument from command line
    try:
        source_folder = argv[1]
    except:
        print("Please, give me path and source folder's name")
        source_folder = input(">>> ")
        if not source_folder:
            print("Можливо наступного разу?")
            exit()
    home = Path(source_folder)
    # Destination folders
    dest_folders = {
        "image": home.joinpath("images"),
        "doc": home.joinpath("documents"),
        "video": home.joinpath("video"),
        "audio": home.joinpath("audio"),
        "archives": home.joinpath("archives"),
        "unknown": home.joinpath("unknown"),
        # "doc": source_folder + "\\documents",
        # "video": source_folder + "\\video",
        # "audio": source_folder + "\\audio",
        # "archives": source_folder + "\\archives",
        # "unknown": source_folder + "\\unknown",
    }
    # Cyrillic and latin
    cyr_lat = {
        "а": "a",
        "б": "b",
        "в": "v",
        "г": "g",
        "д": "d",
        "е": "e",
        "ё": "yo",
        "ж": "zh",
        "з": "z",
        "и": "i",
        "й": "j",
        "к": "k",
        "л": "l",
        "м": "m",
        "н": "n",
        "о": "o",
        "п": "p",
        "р": "r",
        "с": "s",
        "т": "t",
        "у": "u",
        "ф": "f",
        "х": "h",
        "ц": "c",
        "ч": "ch",
        "ш": "sh",
        "щ": "shh",
        "ь": "",
        "ы": "y",
        "ъ": "",
        "э": "je",
        "ю": "ju",
        "я": "ja",
    }

    extentions = {
        "image": ["JPEG", "PNG", "JPG", "SVG"],
        "doc": ["DOC", "DOCX", "TXT", "PDF", "XLSX", "PPTX", "XLS"],
        "video": ["AVI", "MP4", "MOV", "MKV"],
        "audio": ["MP3", "OGG", "WAV", "AMR"],
        "archives": ["ZIP", "GZ", "TAR"],
    }
    extention_list = [
        "JPEG",
        "PNG",
        "JPG",
        "SVG",
        "DOC",
        "DOCX",
        "TXT",
        "PDF",
        "XLSX",
        "XLS",
        "PPTX",
        "AVI",
        "MP4",
        "MOV",
        "MKV",
        "MP3",
        "OGG",
        "WAV",
        "AMR",
        "ZIP",
        "GZ",
        "TAR",
    ]
    # Sets for known and unknown extentions
    known_ext = set()
    unknown_ext = set()

    make_heap(home, dest_folders, cyr_lat)  # перемещаем все в кучу в папку unknown
    remove_empty_folders(source_folder)  # Удаляем пустые папки
    make_dir(dest_folders)  # Создаем папки назначения
    known_ext = move_files(
        home, dest_folders, extentions, known_ext
    )  # Переносим файлы известных типов в папки назначения
    unknown_ext = find_unknown_ext(
        dest_folders, known_ext, unknown_ext
    )  # Собираем неизвестные расширения
    # rename_all_files()  # Переводим названия фалов в транслит
    unpack_archives(dest_folders)  # Распаковываем архивы
    print("Известные найденные расширения файлов: ", known_ext)
    print("Неизвестные найденные расширения файлов: ", unknown_ext)


if __name__ == "__main__":
    main()
