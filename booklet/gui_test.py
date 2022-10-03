# Copyright (c) 2022, Hyunseong Kim <qwqwhsnote@gm.gist.ac.kr>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITE D TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from __future__ import annotations

import platform, os, sys
import sys, os
sys.path.insert(0, os.path.abspath("."))
from functools import partial
import re
from math import log2
from typing import Literal

# tkinter----------------------------------
import tkinter as tk
from tkinter import filedialog

if platform.system() != "Darwin":
    from tkinter import ttk
else:
    import tkmacosx as ttk  # Mac OS specific module
from tkinter.colorchooser import askcolor

# 3rd parties----------------------------
from PIL import Image, ImageTk
import simpleaudio
import PyPDF2 as pypdf
import yaml


# Project modules-----------------------------------------------

from booklet.core.manuscript import Manuscript
from booklet.core.modifiers import *
import booklet.data as data
from booklet.meta import APP_NAME
from booklet.utils.misc import *
from booklet.utils.conversion import mm2pts, pts2mm
from booklet.utils.color import hex2cmyk, cmyk2rgb, rgb2hex

# UI--------------------------------------------------------------------------------------------

#    booklet_ui = UI()
#    booklet_ui.set_language()
#    booklet_ui.set_layout()
#    booklet_ui.execute()

class UI(tk.Tk):
    def __init__(self, language_code, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.call("source", resources_path(data.TK_THEME, data.PATH_RESOURCE))
        self.call("set_theme", "light")
        self.title(APP_NAME)

        self.tool_bar = ToolBar(self)
        super().configure(menu=self.tool_bar)
        self.language_code = language_code
        self.ui_texts = self.__load_ui_texts()
        # Tabs
        self.tab_notebook = ttk.Notebook(self)
        self.tabs = [
            Files(self.tab_notebook, self.ui_texts["tabs"]["files"]), 
            #Section(self.tab_notebook).set_ui_texts(self.ui_texts["Section"]),
            #Imposition(self.tab_notebook).set_ui_texts(self.ui_texts["Imposition"]),
            #PrintingMark(self.tab_notebook).set_ui_texts(self.ui_texts["Printing Marks"]),
            #Utils(self.tab_notebook).set_ui_texts(self.language_code)
        ]
        for tab in self.tabs:
            self.tab_notebook.add(tab , tab.ui_texts["name"])

        self.execute()
    def set_language(self, code:str='en'): # lanuage code
        self.language_code = code
    def set_resources_datas(self, urls:dict, images:dict, mics:dict, language_code:str="en"):

        self.language_code = language_code
        pass
    def locating_layout(self):
        pass
    def execute(self):
        self.mainloop()
    def __load_ui_texts(self):
        lang_path =resources_path(self.language_code+".yaml", data.PATH_LANGUAGE)
        with open(lang_path, "r") as lang:
            return yaml.load(lang, yaml.FullLoader)
    def __load_settings(self):
        pass

# ToolBar
class ToolBar(tk.Menu):
    def __init__(self, parent, language_pack, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = parent

# Frame in Tabs
# essential routine: localization
#   All frame must provide 'set' and 'update' routine of its ui texts with the given lanugage arguments.
class Files(tk.Frame):
    name = "File"
    def __init__(self, parent, language_pack, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.width = 0
        self.height = 0
        self.ui_texts = language_pack
        if "width" in kwargs.keys():
            self.width = kwargs["width"]
        if "height" in kwargs.keys():
            self.height = kwargs["height"]

        self.frames = [
            Manuscript(self, self.ui_texts["manuscript"]),
            FileInfo(self, self.ui_texts["file_info"]),
            Output(self, self.ui_texts["output"])
        ]

        self.frames[0].grid(row=0, column=0, rowspan=2)
        self.frames[1].grid(row=0, column=1)
        self.frames[2].grid(row=1, column=1)

    def __add_new_file(self, event=None):
        pass        

    def __event_file_selection(self, event=None):
        self.selected_file_name.set()
        self.search_file.delete(0, tk.END)

    def __event_remove_all(self, event=None):
        for file in self.selected_files.get_children():
            self.selected_files.delete(file)
    def __event_remove_selected_ones(self, event=None):
        for file in self.selected_files.selection():
            self.selected_files.delete(file)

    def set_ui_texts(self, string_pack):
        strings =[]
        if "strings" in string_pack.keys():
            for st in string_pack["strings"]:
                strings.append(st)
        print(string_pack["frames"])
        for frame in string_pack["frames"].values():
            strings.append(frame["strings"])
        for value, st in zip(self.strings, strings):
            if isinstance(value, tk.StringVar):
                value.set(st)
        # Additional set for non-StringVar() texts.

    def update_ui_language(self, string_pack):
        self.set_ui_texts(string_pack)


class Manuscript(tk.LabelFrame):
    def __init__(self, parent, language_pack, resources, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.parent = parent
        self.ui_texts = language_pack
        self.resources = resources
        # UI strings
        super().config(text=self.ui_texts["name"])
        # Value variables
        self.selected_file_name = tk.StringVar(value="")

        self.texts = []
        self.variables ={}
        self.frame= {
            "search_file": ttk.Frame(self),
            "files": ttk.Frame(self),
            "buttons": ttk.Frame(self)
            }

        # Frame 1 search bar
        self.selected_file = ttk.Entry(self.frame["search_file"], textvariable= self.selected_file_name)
        self.search_button = ttk.Button(self.frame["search_file"])
        self.__set_search_file_frame()
        
        # Frame 2 files list
        self.selected_files = ttk.Treeview(self.frame["files"])
        self.selected_files_scroll_y = ttk.Scrollbar(self.frame["files"])
        self.selected_files_scroll_x = ttk.Scrollbar(self.frame["files"])
        self.__set_files_frame()
        
        # Frame 3 buttons
        self.modulate_files_up = ttk.Button(self.frame["buttons"])
        self.modulate_files_down = ttk.Button(self.frame["buttons"])
        self.modulate_files_delete = ttk.Button(self.frame["buttons"], command=self.__event_remove_selected_ones)
        self.modulate_files_delete_all = ttk.Button(self.frame["buttons"], command=self.__event_remove_all)
        self.modulate_files_sort = ttk.Button(self.frame["buttons"])
        self.__set_modulate_buttons()
        
        # Event assign 

        # Locate layout elements
        self.search_file.grid(row=0, column=0)
        self.search_button.grid(row=0, column=1, columnspan=2)
        self.files.grid(row=1, column=0, rowspan=3)

        
    # Frame set
    def __set_search_file_frame(self):
        self.variables["selected_file"] = tk.StringVar(value="")
        self.selected_file.configure(textvariable=self.variables["selected_file"])

        self.search_button.configure(text="...")

        self.selected_file.grid(row=0, column=0)
        self.search_button.grid(row=0, column=1)
    def __set_files_frame(self):
        self.selected_files.configure(height =12, padding=2, columns=["index", "name"], selectmode="extended")
        # locate
        self.selected_files.pack(side = tk.LEFT, fill = tk.BOTH, anchor = tk.W)
        self.selected_files_scroll_y.pack(side = tk.RIGHT, fill = tk.Y, anchor = tk.E)
        self.selected_files_scroll_x.pack(side = tk.BOTTOM, fill = tk.X, anchor = tk.S)

        # Bind events
        self.selected_files.config(
            xscrollcommand = self.selected_files_scroll_x.set,
            yscrollcommand = self.selected_files_scroll_y.set
            )
        self.selected_files_scroll_x.config(command= self.selected_files.xview)
        self.selected_files_scroll_y.config(command= self.selected_files.yview)

        self.selected_files.grid(row=0, column=0)
        self.selected_files_scroll_x(row=1, column=0)
        self.selected_files_scroll_y(row=0, column=1)

    def __set_modulate_buttons(self):

        # Resource assign

        self.modulate_files_up.grid(row = 0, column=0)
        self.modulate_files_down.grid(row = 1, column=0)
        self.modulate_files_delete.grid(row = 2, column=0)
        self.modulate_files_delete_all.grid(row= 2 , column=1)
        self.modulate_files_sort.grid(row=0, column=1, rowspan=2)
    def __set_events(self):
        # Event assign
        self.selected_files.bind("<<TreeviewSelect>>", )
        self.selected_files.bind("<ButtonRelease-1>", self.__event_file_selection)


    @property
    def settings(self):
        pass

class FileInfo(tk.LabelFrame):
    def __init__(self, parent, language_pack, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.parent = parent
        self.ui_texts = language_pack

        # UI strings
        # Value variables
    def set_ui_strings(self):
        # Title set 
        super().configure(text=self.name)
class Output(tk.LabelFrame):
    def __init__(self, parent, language_pack,  *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.parent = parent
        self.ui_texts = language_pack

        # UI strings
        # Value variables


class Section(tk.Frame):
    name = "Section"
    def __init__(self, parent, language_pack,  *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent

    def update_ui_language(**kwargs):
        pass
class Imposition(tk.Frame):
    name = "Imposition"
    def __init__(self, parent, language_pack,  *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent

    def update_ui_language(**kwargs):
        pass

class PrintingMark(tk.Frame):
    name = "Printing Marks"
    def __init__(self, parent, language_pack,  *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent

    def update_ui_language(**kwargs):
        pass

class Utils(tk.Frame):
    name = "Utils"
    def __init__(self, parent, language_pack,  *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent

    def update_ui_language(**kwargs):
        pass

# Independent Frame
class ProgressBar(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent


if __name__ == "__main__":

    ui = UI(language_code="en")
