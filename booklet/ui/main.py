import sys
from collections.abc import Iterable

import tkinter as tk
from tkinter.ttk import Button, Label
if sys.platform.startswith("darwin"):
    from tkmacosx import Button
from tkinter import StringVar, IntVar, DoubleVar
from tkinter import filedialog
from tkinter.colorchooser import askcolor

from PIL import Image, ImageTk
import simpleaudio
import PyPDF2 as pypdf
import yaml

# Project

import booklet.data as data
from booklet.meta import APP_NAME
from booklet.utils.misc import *
from booklet.utils.conversion import mm2pts, pts2mm
from booklet.utils.color import hex2cmyk, cmyk2rgb, rgb2hex
from booklet.utils.matrix import exchange

from booklet.ui import HPMenu, HPLabelFrame, HPFrame, HPNoteBook
from booklet.ui.menubar import HelpMenu, ReferMenu, SettingMenu, LanguageMenu
from booklet.ui.tabs.file import FileIO
from booklet.ui.tabs.section import Section
from booklet.ui.tabs.imposition import Imposiiton
from booklet.ui.tabs.printingmarks import PrintingMarks
from booklet.ui.tabs.utils import Utils


from booklet.ui.resources import resources

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
        
        tabs = [
            FileIO(self, self.ui_texts["files"], self.resources["files"], width=self.width, height=self.height)
        ]
        for tab in tabs:
            self.add(tab, text=tab.ui_texts["name"])


# Progress bar
class HPBooklet_ProgressBar(HPFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



# Root UI
class HPBooklet(tk.Tk):
    def __init__(
            self, 
            *args,
            lang_code = "en",
            resources = None,
            **kwargs
        ):
        self.width = 0
        self.height = 0
        if "width" in kwargs.keys():
            self.width = kwargs["width"]
            del(kwargs["width"])
        if "height" in kwargs.keys():
            self.height = kwargs["height"]
            del(kwargs["height"])
        super().__init__(*args, **kwargs)
        self.language_code = lang_code
        self.resources = resources

        self.call("source", resources_path(data.TK_THEME, data.PATH_RESOURCE))
        self.call("set_theme", "light")
        self.title(APP_NAME)

        self.ui_texts = self.__load_ui_texts()

        self.sub_elements ={} # Each keys must be same with language setting file key
        self.sub_elemnts_direct = {} # Switching can be acheive by direct modification of tk.StringVar.
        self.string_vars = {
            "generate": tk.StringVar(value="")
        }

        self.sub_elements["menubar"] = HPBooklet_Menu(
                                                self, 
                                                self,
                                                self.ui_texts["menubar"], 
                                                self.resources["menubar"]
                                                )
        super().configure(menu=self.sub_elements["menubar"])
        self.sub_elements["tabs"] = HPBooklet_Tabs(
                                            self, 
                                            self.ui_texts["tabs"], 
                                            self.resources["tabs"],
                                            width=self.width, 
                                            height=int(self.height*0.7)
                                            )

        self.sub_elements["progress"] = HPBooklet_ProgressBar(
                                                self
                                            )
        #   Buttons, Labels
        self.sub_elemnts_direct["generate"] = Button(self, textvariable=self.string_vars["generate"])

        self.string_vars["generate"].set(self.ui_texts["generate"])
        
        # Locating
        self.sub_elements["tabs"].grid(row=0, column=0)
        self.sub_elements["progress"].grid(row=1, column=0)
        self.sub_elemnts_direct["generate"].grid(row=2, column=0)
        
    
    def __load_ui_texts(self):
        lang_path =resources_path(self.language_code+".yaml", data.PATH_LANGUAGE)
        with open(lang_path, "r", encoding="utf-8") as lang:
            return yaml.load(lang, yaml.FullLoader)

    def update_ui_texts(self, lang_code):
        self.language_code = lang_code
        self.ui_texts = self.__load_ui_texts()
        keys = list(self.ui_texts.keys())[2:] # 0: language, 1: font settings
        for i, key in enumerate(keys):
            if isinstance(self.ui_texts[key], Iterable) and type(self.ui_texts[key]) != str:
                self.sub_elements[key].update_ui_texts(self.ui_texts[key])
            else:
                self.string_vars[key].set(self.ui_texts[key])
    
    @property
    def requirements(self):
        pass
    @requirements.setter
    def requirements(self, **kwargs):
        pass

    def save_requirements(self):
        file = filedialog.asksaveasfile(
            initialdir="~",
            initialfile = "requirements.yaml",
            filetypes=[("Yaml", "*.yaml")]
        )
    def load_requirements(self):
        file = filedialog.askopenfile(
            initialdir="~", 
            title="Select Requrements file", 
            filetypes=(("Yaml", "*.yaml"),)
        )

        requirements = self.__vaildate_requirements(file)

        if type(requirements) == str:
            # Raise Popup windows
            pass
        elif requirements:
            self.requirements = requirements
    
    def __vaildate_requirements(self, file):
        # Check the format of requirements 
        # Fill omitted field with {None} variables
        pass