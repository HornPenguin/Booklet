import tkinter as tk
from tkinter import ttk

from tkinter import filedialog
from tkinter.colorchooser import askcolor

if platform.system() != "Darwin":
    from tkinter import Label, Button
else:
    from tkmacosx import Label, Button

from tkinter import StringVar, IntVar, DoubleVar

from tkinter import Menu, LabelFrame
from tkinter.ttk import Notebook, Frame
from tkinter.font import Font

from typing import Dict

class HPMenu(Menu):
    # TAML format:
    #   MenuName:
    #       name: "menu name"
    #       submenu:
    #           SubMenu001:
    #                name: "submenu name001"
    #       command: 
    #           command001: "command001"
    def __init__(self, parent, lanugage_pack:Dict, font:Font, resources, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent

        self.ui_texts = lanugage_pack
        self.resources = resources
        self.font = None
        if isinstance(font, Font):
            self.font = font

        self.submenus = []
        self.commands = []


        self.__append_sub_menus()

        for menu, label in zip(self.menus, self.ui_texts.keys()):
            self.add_cascade(label=self.ui_texts[label]["name"], menu=menu)

        def __append_sub_menus():
            for menu, label in zip(self.submenus, self.ui_texts.keys()):
                self.add_cascade(label=self.ui_texts[label]["name"], menu=menu)
class HPLabelFrame(LabelFrame):
    def __init__(self, parent, language_pack, font, resources, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        
        self.ui_texts = language_pack
        self.font = font
        self.resources = resources

        super().config(text = self.ui_texts["name"])

        self.ui_texts_variables = {}
        self.variables = {}

        self.sub_frames = {}
        

        self.__layout()
    
    def __layout(self):
        raise NotImplementedError("Children class must overlapping this method.")
class HPFrame(Frame):
    def __init__(self):
        pass
class HPNoteBook(Notebook):
    def __init__(self):
        pass