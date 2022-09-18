# Build script using Pyinstaller and Sphinx

import PyInstaller.__main__
import sys, os
import platform

from booklet.utils.images import icon_name

PLATFORM = platform.system()
dir_sep = "\\" if PLATFORM == "Windows" else "/"

document_directory = "documents"
project_name = "booklet"

name = "main.py"

WORK_PATH = "tem"
ICON_NAME = os.path.join("resources", icon_name)
SPLASH_IMAGE = os.path.join("resources", "splash.png")
PROGRAM_NAME = "booklet"
CONSOLE = False
argv = sys.argv[1:]

pyinstall_argv = []
sphinx_argv = []

for arg in argv:
    if "--sphinx=" in arg:
        sphinx_argv.append(arg.replace("--sphinx=", ""))
    else:
        pyinstall_argv.append(arg)
    if "--console" in arg:
        CONSOLE = True
        

FILE_NAME = os.path.join("booklet", name)

print("pyinstaller: -", pyinstall_argv)
print("sphinx:  ", sphinx_argv)
# Pyinstaller=====================================================================================
print("Build program.....................")

build_option = []


for i, arg in enumerate(pyinstall_argv):
    if "--splash" in arg:
        if "=" not in arg:
            pyinstall_argv[i] = f"--splash={SPLASH_IMAGE}"
        if "--onefile" in pyinstall_argv:
            del pyinstall_argv[i]

PROGRAM_NAME += "" if "--onefile" in pyinstall_argv else f"_{PLATFORM}"

build_option += [
    "--noupx",
    #    '--log-level=DEBUG',
    f"--workpath={WORK_PATH}",
    f"--name={PROGRAM_NAME}",
    f"--icon={ICON_NAME}",
]

build_option += pyinstall_argv

Platform_spec = {  # No terminal or console windows for gui application.
    "Darwin": [],
    "Linux": [
        "--hidden-import=PIL",
        "--hidden-import=PIL._imagingtk",
        "--hidden-import=PIL._tkinter_finder",
    ],
    "Windows": [],
}

if not CONSOLE:
    Platform_spec["Darwin"] += ["--noconsole"]
    Platform_spec["Windows"] += ["--noconsole"]

build_option += Platform_spec[PLATFORM]

path_sep = ";" if PLATFORM == "Windows" else ":"
datas = {"resources": "resources"}
binaries = []
data_list = [f"--add-data={key}{path_sep}{datas[key]}" for key in datas.keys()]
binary_list = []

build_option += data_list

build_option.append(FILE_NAME)
print("Build-options")
print(" ".join(build_option))
if __name__ == "__main__":
    PyInstaller.__main__.run(build_option)

    # Sphinx-----------------------------------
    if len(sphinx_argv) > 0:
        print("Generate documents(Sphinx)")
        os.system(f"sphinx-apidoc -o {document_directory} {project_name}")
        os.system("make " + " ".join(sphinx_argv))

import os, shutil
for filename in os.listdir(WORK_PATH):
    file_path = os.path.join(WORK_PATH, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))

print("Finished")
