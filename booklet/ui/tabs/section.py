from booklet.ui.tabs import *
from booklet.ui import HPFrame, HPLabelFrame



class Section(HPFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

class Standard(HPLabelFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

        # Variables
        self.custom_format_onoff = BooleanVar(value = False)
        self.custom_format_width = DoubleVar(value = 0.0)
        self.custom_format_height = DoubleVar(value = 0.0)
        self.page_range = StringVar(value = "")
        self.riffle_direction = BooleanVar(value = False)
        

class Custom(HPLabelFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)