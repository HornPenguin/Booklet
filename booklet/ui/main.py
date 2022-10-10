import sys

import tkinter as tk
from tkinter.ttk import Button, Label
if sys.platform.startswith("darwin"):
    from tkmacosx import Button


from booklet.ui import HPMenu, HPLabelFrame, HPFrame, HPNoteBook
from booklet.ui.menubar import *


# Menu
class HPBooklet_Menu(HPMenu):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.sub_entries.append(HelpMenu(self, self.main_app, self.ui_texts["help"], self.resources["help"], tearoff=0))
        self.sub_entries.append(ReferMenu(self, self.main_app, self.ui_texts["reference"], self.resources["reference"], tearoff=0))
        self.sub_entries.append(SettingMenu(self, self.main_app, self.ui_texts["settings"], self.resources["settings"], tearoff=0))
        self.sub_entries.append(LanguageMenu(self, self.main_app, self.ui_texts["language"], {}, tearoff=0))

        for label, menu in zip(self.ui_texts.values(), self.sub_entries):
            self.add_cascade(label=label["name"] , menu=menu)

# Tabs
class HPBooklet_Tabs(HPNoteBook):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


# Progress bar
class HPBooklet_ProgressBar(HPFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



# Root UI

class HPBooklet(tk.Tk)