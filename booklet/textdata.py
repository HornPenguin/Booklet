from booklet.utils import resources_path

about_text_path = resources_path("about", "resources/text")
license_text_path = resources_path("license", "resources/text")
url_text_path = resources_path("urls", "resources/text")

# resourcess image names
imposition_icon_names = ["imposition", "split"]
printing_icon_names = ["proof", "cmyk", "registration", "trim"]

re_get_ranges = r"([ ]{0,}\d+[ ]{0,}-{1,1}[ ]{0,}\d+[ ]{0,}|[ ]{0,}\d+[ ]{0,}[^,-])"
re_check_permited_character = r"([^-,\d\s])+?"

with open(url_text_path, "r") as f:
    git_repository = f.readline()
    homepage = f.readline()
    tutorial = f.readline()

about_text = []
with open(about_text_path, "r") as f:
    about_list = f.readlines()
    rlist = list(filter(lambda x: x != "" and x != "\n", about_list))
    about_text += rlist

license = []

with open(license_text_path, "r") as f:
    license_list = f.readlines()
    rlist = list(filter(lambda x: x != "" and x != "\n", license_list))
    license += rlist


format_head = ["Format", "width(mm)", "height(mm)"]
format_table = [
    ("A3", 297, 420),
    ("A4", 210, 297),
    ("A5", 148, 210),
    ("B3", 353, 500),
    ("B4", 250, 353),
    ("B5", 176, 250),
    ("B6", 125, 176),
    ("JIS B3", 364, 515),
    ("JIS B4", 257, 364),
    ("JIS B5", 182, 257),
    ("JIS B6", 128, 182),
    ("Letter", 216, 279),
    ("Legal", 216, 356),
    ("Tabloid", 279, 432),
    ("GOV Letter", 203, 267),
    ("GOV Legal", 216, 279),
    ("ANSI A", 216, 279),
    ("ANSI B", 279, 432),
    ("ARCH A", 229, 305),
    ("ARCH B", 305, 457),
]

PaperFormat = {"Default": "0x0"}
for format in format_table:
    PaperFormat[format[0]] = f"{format[1]}x{format[2]}"
