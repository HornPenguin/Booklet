from booklet.ui.tabs import *
from booklet.ui import HPFrame, HPLabelFrame


class PrintingMarks(HPFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sub_frames.append(
            Marks(
                self,
                self.ui_texts["frames"]["printingmarks"],
                self.resources["printingmarks"],
                width = self.width,
                height = self.height
            )
        )
        
        self.sub_frames[0].grid(row=0, column=0, padx = (10, 10), pady =4 , sticky = N+S+W+E)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

class Marks(HPLabelFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid_anchor(CENTER)

        # Variables
        self.margin_onoff = DoubleVar(value = 0.)
        self.crop_onoff = BooleanVar(value = False)
        self.trim_onoff = BooleanVar(value = False)
        self.registration_onoff = BooleanVar(value = False)
        self.cmyk_onoff = BooleanVar(value = False)
        self.direction_onoff = BooleanVar(value = False)
        self.angle_onoff = BooleanVar(value = False)
        self.duplex_onoff = BooleanVar(value = False)

        # Ui frames

        self.ui_frames["left"] = HPFrame(self, width = int(0.5*self.width), height = self.height)
        self.ui_frames["right"] = HPFrame(self, width = int(0.5*self.width), height = self.height)


        self.ui_frames["left"].grid(row=0, column = 0, padx = (4,4), pady=4, sticky = N+S+W+E)
        self.ui_frames["right"].grid(row=0, column = 1, padx = (4,4), pady=4, sticky = N+S+W+E)

