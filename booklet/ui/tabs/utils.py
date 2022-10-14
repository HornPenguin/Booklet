from booklet.ui.tabs import *
from booklet.ui import HPFrame, HPLabelFrame


class Utils(HPFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)


class ToImage(HPLabelFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

        # Variables
        self.toimage_onoff = BooleanVar(value = False)


class Duplex(HPLabelFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        # Variables
        self.duplex_onoff = BooleanVar(value = False)
        self.translation_x = DoubleVar(value=0.)
        self.translation_y = DoubleVar(value=0.)
        self.rotation = DoubleVar(value = 0.)
        self.preserve_dimension = BooleanVar(value = False)

        # Functional Variables
        self.translation_onoff = BooleanVar(value = False)
        self.rotation_onoff = BooleanVar(value = False)

class Note(HPLabelFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        # Variables
        self.Note_onoff = BooleanVar(value = False)

