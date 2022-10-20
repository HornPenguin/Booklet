from booklet.ui import HPFrame, HPLabelFrame
from booklet.ui.tabs import *
class Imposition(HPFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid_anchor(CENTER)

        self.sub_frames.append(
            Book(
                self,
                self.ui_texts["frames"]["book"],
                self.resources["book"],
                width = int(0.5*self.width),
                height = self.height
            )
        )
        self.sub_frames.append(
            Repetition(
                self,
                self.ui_texts["frames"]["repetition"],
                self.resources["repetition"],
                width = int(0.5*self.width),
                height = self.height
            )
        )

        self.sub_frames[0].grid(row=0, column=0, padx=(10, 10), pady=4)
        self.sub_frames[1].grid(row=0, column=1, padx=(10, 10), pady=4)


class Book(HPLabelFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid_anchor(CENTER)


        # UI string setting
        self.string_vars

class Repetition(HPLabelFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid_anchor(CENTER)