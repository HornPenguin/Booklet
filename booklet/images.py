from .utils import resources_path
import platform

PLATFORM = platform.system()

icon_name = "hp_booklet"

if PLATFORM == "Linux":
    icon_name = "@" + icon_name + ".xbm"
    # icon_name = icon_name+'.xbm'
else:
    icon_name = icon_name + ".ico"

icon_path = resources_path(icon_name, "resources")
