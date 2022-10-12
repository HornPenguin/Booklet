import tkinter as tk
from tkinter import Toplevel, ttk

from tkinter import filedialog
from tkinter.colorchooser import askcolor

import platform
if platform.system().startswith != "Darwin":
    from tkinter import Label, Button
else:
    from tkmacosx import Label, Button

from tkinter import StringVar, IntVar, DoubleVar

from tkinter import Menu, LabelFrame
from tkinter.ttk import Notebook, Frame
from tkinter.font import Font

from typing import Dict
from collections.abc import Iterable

class HPMenu(Menu):
    # YAML format:
    #   MenuName:
    #       name: "menu name"
    #       subentries:
    #           SubMenu001:
    #                name: "submenu name001"
    #                subentries:
    #                       .
    #                       .
    #                       .
    #           command001: "command001"
    #           command002: "command002"
    #           SubMenu002:
    #                name: "submenu name002"
    #                subentries:
    #                       .
    #                       .
    #                       .  
    
    def __init__(self, parent, main_app, ui_texts, resources, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.main_app = main_app

        self.ui_texts = ui_texts
        self.resources = resources

        self.sub_entries = []

    def update_ui_texts(self, ui_texts):
        self.ui_texts = ui_texts
        if "subentries" in self.ui_texts.keys():
            if type(self.ui_texts["subentries"]) == list:
                for i in range(0, len(self.ui_texts["subentries"])):
                    self.entryconfigure(i, label = self.ui_texts["subentries"][i])
            else:
                for i, key in enumerate(self.ui_texts["subentries"].keys()):
                    if isinstance(self.ui_texts["subentries"][key], Iterable) and type(self.ui_texts["subentries"][key]) != str:
                        print("iterable")
                        self.sub_entries[i].update_ui_texts(self.ui_texts["subentries"][key])
                    else: self.entryconfigure(i, label = self.ui_texts["subentries"][key])
        else: 
            for i, key in enumerate(self.ui_texts.keys()):
                if isinstance(self.ui_texts[key], Iterable) and type(self.ui_texts[key]) != str:
                    self.entryconfigure(i, label = self.ui_texts[key]["name"])
                    value = self.ui_texts[key]
                    self.sub_entries[i].update_ui_texts(value)
                elif type(self.ui_texts[key]) == str:
                    self.entryconfigure(i, label = self.ui_texts[key])

class HPLabelFrame(LabelFrame):
    def __init__(self, parent, ui_texts, resources, *args, **kwargs):
        
        self.width = kwargs["width"] if "width" in kwargs.keys() else 0
        self.height = kwargs["height"] if "height" in kwargs.keys() else 0

        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.ui_texts = ui_texts
        self.resources = resources

        super().config(text = self.ui_texts["name"])

        self.sub_frames = []
        self.string_vars = {} # tkinter StringVar to be convert with ui_text update
        
    def update_ui_texts(self, ui_texts):
        label_strings = ui_texts["strings"] if "strings" in ui_texts.keys() else None
        subframe_strings = list(ui_texts["frames"].values()) if "frames" in ui_texts.keys() else None
        if subframe_strings is not None:
            for i, subframe in enumerate(self.sub_frames):
                subframe.update_ui_texts(subframe_strings[i])
        if label_strings is not None:
            keys = list(self.ui_texts["strings"].keys())
            for i, label_string_var in enumerate(self.string_vars.values()):
                key = keys[i]
                try:
                    label_string_var.set(label_strings[key])
                except:
                    print(label_strings)
        self.ui_texts = ui_texts

class HPFrame(Frame):
    def __init__(self, parent, *args, ui_texts=None, resources=None,**kwargs):
        
        super().__init__(parent, *args, **kwargs)
        self.parent = parent

        self.ui_texts = ui_texts
        self.resources = resources

        self.sub_frames = []
        self.string_vars = {} # tkinter StringVar

    def update_ui_texts(self, ui_texts):
        print(ui_texts.keys())
        if self.ui_texts is not None: # Directly have ones
            self.ui_texts = ui_texts
            label_strings = self.ui_texts["strings"] if "strings" in self.ui_texts.keys() else None
            subframe_strings = list(self.ui_texts["frames"].values()) if "frames" in self.ui_texts.keys() else None

            if subframe_strings is not None:
                for i, subframe in enumerate(self.sub_frames):
                    subframe.update_ui_texts(subframe_strings[i])
            if label_strings is not None:
                for i, label_string_var in enumerate(self.string_vars.values()):
                    label_string_var.set(label_strings[i])
        elif len(self.sub_frames) != 0 and ui_texts is not None:
            label_strings = ui_texts["strings"]
            subframe_strings = list(ui_texts["subframes"].values())

            for i, subframe in enumerate(self.sub_frames):
                subframe.update_ui_texts(subframe_strings[i])
            for i, label_string_var in enumerate(self.string_vars):
                label_string_var.set(label_strings[i])

class HPNoteBook(Notebook):
    def __init__(self, parent, ui_texts, resources, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.ui_texts = ui_texts
        self.resources = resources


    def update_ui_texts(self, ui_texts):
        self.ui_texts = ui_texts
        for i, tab in enumerate(self.children.values()):
            sub_lang_pack = list(self.ui_texts.values())[i]
            print(sub_lang_pack["name"])
            self.tab(i, text = sub_lang_pack["name"])
            tab.update_ui_texts(sub_lang_pack)




class PopUp(Toplevel):
    def __init__(
        self, 
        parent, 
        ui_texts, 
        resources, 
        *args, 
        **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = parent

        self.ui_texts = ui_texts
        self.resources = resources
