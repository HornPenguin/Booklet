from booklet.data import *

# Types of data
# 1. images
# 2. urls
# 3. treeviews
# 4. texts
# 5. media
# 6. misc <- binary or something else
resources ={
    "main": {},
    "menubar" : {
        "help": {
            "urls":{
                "repository": git_repository
            },
            "texts":{
                "about": about_text,
                "license": license
            }
        },
        "reference":{
            "urls":{
                "tutorial": tutorial
            },
            "treeviews":{
                "paper_format": [format_head, format_table],
            },
            "images": {
                "paper_fold": []
            },
            "texts": { 
                "paper_fold": []
            }
        },
        "settings": {}
    },
    "tabs" : {
        "files":{
            "manuscript":{
                "images": {
                    "button": button_icons
                }
            }
        },
        "section":{
            "standard":{},
            "custom": {
                "layout":{},
                "fcode": {
                    "misc":{
                        "start_axis": ["x", "y"]
                    }
                }
            }
        },
        "imposition":{
            "bookbrochures": {},
            "repetition": {}
        },
        "printingmarks":{
            "printingmarks":{
                "texts":{
                    "crop_line": "",
                    "trim_line": "",
                    "registration_mark": "",
                    "cmyk": "",
                    "direction_mark": "",
                    "angle_mark": "",
                    "duplex_measure": ""
                }
            } 
        },
        "utils":{
            "toimage":{},
            "duplex": {},
            "note": {
                "numbering": {
                    "misc":{
                        "count":["test"],
                        "mark_on":["test"],
                        "location":["test"],
                        "align":["test"],
                        "font":["test"],
                        "size":["test"],
                    }
                }
            }
        }
    },
}