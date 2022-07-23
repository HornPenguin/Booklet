from setuptools import setup, find_packages

setup_requires = []

install_requires = [
    'PyPDF2',
    "reportlab",
    "Pillow",
    "simpleaudio"
]


setup(
    name = "HornPenguin Booklet",
    version = "0.0.1",
    description="PDF modulator for press and printing"
    author = "Hyunseong Kim",
    author_email="hyunseong@hornpenguin.com"
    packages = find_packages(),
    install_requires = install_requires,
    setup_requires = setup_requires
) 