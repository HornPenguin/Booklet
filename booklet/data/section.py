from booklet.data import format_table


section_type = ["Book", "Brochure"]

paper_formats = {"Default": "0x0"}
for format in format_table:
    paper_formats[format[0]] = f"{format[1]}x{format[2]}"

riffle = {
    "Right": True,
    "Left": False 
}

brochure_types = {
    "half-fold": 2,
    "tri-fold": 3,
    "z-fold": 3,
    "gate-fold": 3,
    "double-gate-fold": 4,
    "double-parallel-fold": 4,
    "arcodian-fold-4": 4,
    "roll-fold": 4
}

blank_mode = {
    "back" : 1,
    "front" : 2,
    "both" : 0
}