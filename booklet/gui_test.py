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

#from booklet.core.manuscript import Manuscript as Method_Manuscript
#from booklet.core.modifiers import *
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
    def __init__(self, *args, language_code="en", font=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.call("source", resources_path(data.TK_THEME, data.PATH_RESOURCE))
        self.call("set_theme", "light")
        self.title(APP_NAME)
        self.language_code = language_code
        self.ui_texts = self.__load_ui_texts()
        
        self.font = font if font != None else None 

        self.tool_bar = ToolBar(self, self.ui_texts["menubar"], "")
        super().configure(menu=self.tool_bar)
        
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
            self.tab_notebook.add(tab, text=tab.ui_texts["name"])
        
        # Progress

        # Button
        self.button_generate = ttk.Button(self, command= self.execute_generation)

    def set_language(self, code:str='en'): # lanuage code
        self.language_code = code
        self.ui_texts = self.__load_ui_texts()

        self.tool_bar.update_ui_texts()
        for i, tab in enumerate(self.tabs):
            tab.update_ui_texts()
            self.tab_notebook.tab(i, tab.ui_texts["name"])
    #def set_resources_datas(self, urls:dict, images:dict, mics:dict, language_code:str="en"):
    #    self.language_code = language_code
    #    pass
    def locating_layout(self):
        self.tab_notebook.grid(row=0, column=0)

        self.button_generate.grid(row=2, column=0)
    def __load_ui_texts(self):
        lang_path =resources_path(self.language_code+".yaml", data.PATH_LANGUAGE)
        with open(lang_path, "r", encoding="utf-8") as lang:
            return yaml.load(lang, yaml.FullLoader)
    def load_settings(self):
        # open file dialog
        # conver to dictionary
        # Below code:
        file_path = tk.askopenfilename(
            initialdir="~", title="Load settings", filetypes=(("YAML", "*.yaml"),)
            )
        with open(file_path, "r", encoding="utf-8") as set_file:
           settings = yaml.load(set_file, yaml.FullLoader)
        for tab in self.tabs:
            tab.set_parameters(settings[tab.name])
    def save_settings(self):
        pass
    def execute_generation(self):
        settings = []
        for tab in self.tabs:
            settings[tab.name] = tab.settings

# ToolBar
class ToolBar(tk.Menu):
    def __init__(self, parent, language_pack, resources, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = parent
        self.ui_texts = language_pack
        self.resources = resources

        self.menus = [
            tk.Menu(tearoff=0),
            tk.Menu(tearoff=0),
            tk.Menu(tearoff=0),
            tk.Menu(tearoff=0)
            ]
        self.__set_menu_help_labels()
        self.__set_menu_reference_labels()
        self.__set_menu_settings_labels()
        self.__set_menu_language_labels()

        for menu, label in zip(self.menus, self.ui_texts.keys()):
            self.add_cascade(label=self.ui_texts[label]["name"], menu=menu)

    def __set_menu_help_labels(self):
        labels = self.ui_texts["help"]["submenu"]
        self.menus[0].add_command(label = labels["about"], command = self.about)
        self.menus[0].add_command(label = labels["license"], command = self.license)
        self.menus[0].add_command(label = labels["source"], command = self.source)
    def __set_menu_reference_labels(self):
        labels = self.ui_texts["reference"]["submenu"]
        self.menus[1].add_command(label = labels["tutorial"], command = self.tutorial)
        self.menus[1].add_command(label = labels["paper-format"], command = self.paper_format)
        self.menus[1].add_command(label = labels["paper-fold"], command = self.paper_fold)
    def __set_menu_settings_labels(self):
        labels = self.ui_texts["settings"]["submenu"]
        self.menus[2].add_command(label = labels["load"], command= self.load_setting)
        self.menus[2].add_command(label = labels["save"], command= self.save_setting)
    def __set_menu_language_labels(self):
        labels = self.ui_texts["language"]["submenu"]
        for language in labels:
            self.menus[3].add_command(
                label = language, 
                 command=partial(self.update_language, language)
                )



    def set_ui_texts(self):
        for i, menu in zip(range(0, len(self.menus)), self.ui_texts):
            self.entryconfigure(i, label = menu["name"])
    
    def about(self):
        pass
    def license(self):
        pass
    def source(self):
        open_url(self.resources["url"]["repository"])
    def tutorial(self):
        open_url(self.resources["url"]["tutorial"])
    def paper_format(self):
        format = self.resources["data"]["paper-format"]
    def paper_fold(self):
        fold_image = self.resources["image"]["paper-format"]
    def load_setting(self):
        self.parent.load_setting()
    def save_setting(self):
        self.parent.save_setting()
    def update_language(self, lang_code):
        self.parent.update_language(lang_code)
    def update_ui_texts(self, language_pack):
        self.ui_texts = language_pack
        self.set_ui_texts()

# Frame in Tabs
# essential routine: localization
#   All frame must provide 'set' and 'update' routine of its ui texts with the given lanugage arguments.

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
        self.modulate_files_delete = ttk.Button(self.frame["buttons"])
        self.modulate_files_delete_all = ttk.Button(self.frame["buttons"])
        self.modulate_files_sort = ttk.Button(self.frame["buttons"])
        self.__set_modulate_buttons_frame()
        
        # Event assign 

        # Locate layout elements

        self.frame["search_file"].grid(row = 0, column= 0, columnspan =2)
        self.frame["files"].grid(row = 1, column=0 )
        self.frame["buttons"].grid(row = 1, column=1 )

        
    # Frame set
    def __set_search_file_frame(self):
        self.variables["selected_file"] = tk.StringVar(value="")
        self.selected_file.configure(textvariable=self.variables["selected_file"])
        self.search_button.configure(text="...")

        self.selected_file.grid(row=0, column=0)
        self.search_button.grid(row=0, column=1)
    def __set_files_frame(self):
        self.selected_files.configure(height =12, padding=2, columns=["index", "name"], selectmode="extended")
        
        # Event assign
        self.selected_files.config(
            xscrollcommand = self.selected_files_scroll_x.set,
            yscrollcommand = self.selected_files_scroll_y.set
            )
        self.selected_files_scroll_x.config(command= self.selected_files.xview)
        self.selected_files_scroll_y.config(command= self.selected_files.yview)

        # Locate 001 Choose one of them
        self.selected_files.grid(row=0, column=0)
        self.selected_files_scroll_x.grid(row=1, column=0)
        self.selected_files_scroll_y.grid(row=0, column=1)
        # Locate 002
        self.selected_files.pack(side = tk.LEFT, fill = tk.BOTH, anchor = tk.W)
        self.selected_files_scroll_y.pack(side = tk.RIGHT, fill = tk.Y, anchor = tk.E)
        self.selected_files_scroll_x.pack(side = tk.BOTTOM, fill = tk.X, anchor = tk.S)


    def __set_modulate_buttons_frame(self):

        # Resource assign

        self.modulate_files_up.grid(row = 0, column=0)
        self.modulate_files_down.grid(row = 1, column=0)
        self.modulate_files_delete.grid(row = 2, column=0)
        self.modulate_files_delete_all.grid(row= 2 , column=1)
        self.modulate_files_sort.grid(row=0, column=1, rowspan=2)

        # Method assign
        self.modulate_files_up.configure(command=self.__method_move_file)
        self.modulate_files_down.configure(command=self.__method_move_file)
        self.modulate_files_delete.configure(command=self.__method_remove_selected_ones)
        self.modulate_files_delete_all.configure(command=self.__method_remove_all)
        self.modulate_files_sort.configure(command=self.__method_sort)

    def __set_events(self):
        # Event assign
        self.selected_files.bind("<<TreeviewSelect>>", )
        self.selected_files.bind("<ButtonRelease-1>", self.__event_file_selection)

    # Methods
    def __method_move_file(self):
        pass
    def __method_remove_selected_ones(self):
        pass
    def __method_remove_all(self):
        pass
    def __method_sort(self):
        pass
    @property
    def settings(self):
        return None
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

class Files(tk.Frame):
    def __init__(self, parent, language_pack, resources, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.width = 0
        self.height = 0
        self.ui_texts = language_pack
        self.name = self.ui_texts["name"]
        self.resources = resources

        if "width" in kwargs.keys():
            self.width = kwargs["width"]
        if "height" in kwargs.keys():
            self.height = kwargs["height"]

        self.frames = [
            Manuscript(self, self.ui_texts["manuscript"], self.resources["manuscript"]),
            FileInfo(self, self.ui_texts["file_info"], self.resources["file-info"]),
            Output(self, self.ui_texts["output"], self.resources["output"])
        ]

        self.set_frame_layout()
        
    def set_frame_layout(self):
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
        self.name = self.ui_texts["name"]
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
    #font = tk.font.Font(family="Noto Serif", size=12)
    ui = UI(language_code="ko")
    ui.geometry("400x270")
    ui.mainloop()
