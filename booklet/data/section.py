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
    "Half-fold": 2,
    "Tri-fold": 3,
    "Z-fold": 3,
    "Gate-fold": 3,
    "Double-gate-fold": 4,
    "Double-parallel-fold": 4,
    "Arcodian-fold-4": 4,
    "Roll-fold": 4
}

blank_mode = {
    "back" : "back",
    "front" : "front",
    "both" : "both"
}