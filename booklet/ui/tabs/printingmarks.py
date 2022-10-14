from booklet.ui.tabs import *
from booklet.ui import HPFrame, HPLabelFrame


class PrintingMarks(HPFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

        # Variables
        self.margin_onoff = DoubleVar(value = 0.)
        self.crop_onoff = BooleanVar(value = False)
        self.trim_onoff = BooleanVar(value = False)
        self.registration_onoff = BooleanVar(value = False)
        self.cmyk_onoff = BooleanVar(value = False)
        self.direction_onoff = BooleanVar(value = False)
        self.angle_onoff = BooleanVar(value = False)
        self.duplex_onoff = BooleanVar(value = False)

        # Functional variables
