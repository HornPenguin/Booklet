
from booklet.data import PATH_IMAGE
from pathlib import Path

from PIL import Image

image_path = PATH_IMAGE/"printing_marks"

routine_images = {file.stem: Image.open(image_path/file) for file in image_path.iterdir()}

