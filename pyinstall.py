import PyInstaller.__main__
import sys
import platform

build_option = []

FILE_NAME = 'main.py'
PROGRAM_NAME = 'Booklet'
WORK_PATH = 'install_build'
ICON_NAME = 'resource\\hp_booklet.ico'
SPLASH_IMAGE = 'splash.png'

build_option += [
    '--noupx',
    '--log-level=DEBUG',
    f'--workpath={WORK_PATH}', 
    f'--name={PROGRAM_NAME}',
    f'--icon={ICON_NAME}'
]

argv = sys.argv[1:]

build_option += argv            

PLATFORM = platform.system()
Platform_spec = { #No terminal or console windows for gui application.
    'Darwin': ['--noconsole'],
    'Linux' : [''],
    'Windows': ['--noconsole']
}
build_option += Platform_spec[PLATFORM]

path_sep = ';' if PLATFORM == 'Windows' else ':'

datas = {'resource':'resource'}
binaries = []
data_list = [f'--add-data={key}{path_sep}{datas[key]}' for key in datas.keys()]
binary_list = []

build_option += data_list

build_option.append(FILE_NAME)
print('Build-options')
print(build_option)
PyInstaller.__main__.run(build_option)