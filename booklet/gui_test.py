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
from tkinter import ttk
from tkinter import filedialog
from tkinter.colorchooser import askcolor

if platform.system() != "Darwin":
    from tkinter import Label, Button
else:
    from tkmacosx import Label, Button
from tkinter import StringVar, IntVar, DoubleVar

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
from booklet.utils.matrix import exchange

# UI--------------------------------------------------------------------------------------------

#    booklet_ui = UI()
#    booklet_ui.set_language()
#    booklet_ui.set_layout()
#    booklet_ui.execute()

class UI(tk.Tk):
    def __init__(self, *args, language_code="en", font=None, width=650, height=500, resources=None,  **kwargs):
        super().__init__(*args, **kwargs)
        self.width = width
        self.height = height
        self.call("source", resources_path(data.TK_THEME, data.PATH_RESOURCE))
        self.call("set_theme", "light")
        self.title(APP_NAME)
        self.language_code = language_code
        self.ui_texts = self.__load_ui_texts()
        self.resources = resources

        self.font = font if font != None else None 


        self.variables = {"button": tk.StringVar(value=self.ui_texts["Generate"])}
        self.tool_bar = ToolBar(self, self.ui_texts["menubar"], "")
        super().configure(menu=self.tool_bar)
        
        # Tabs
        self.tab_notebook = ttk.Notebook(
            self, 
            width=self.width, 
            height=int(self.height*0.7)
            )
        notebook_height = int(self.height*0.7)
        self.tabs = [
            Files(self.tab_notebook, self.ui_texts["tabs"]["files"], self.resources["Files"], width=self.width, height=notebook_height), 
            #Section(self.tab_notebook).set_ui_texts(self.ui_texts["Section"]),
            #Imposition(self.tab_notebook).set_ui_texts(self.ui_texts["Imposition"]),
            #PrintingMark(self.tab_notebook).set_ui_texts(self.ui_texts["Printing Marks"]),
            #Utils(self.tab_notebook).set_ui_texts(self.language_code)
        ]
        for tab in self.tabs:
            self.tab_notebook.add(tab, text=tab.ui_texts["name"])
        
        # Progress

        # Button
        self.button_generate = ttk.Button(self, width= 80,textvariable=self.variables["button"], command= self.execute_generation)

        self.locating_layout()
        self.geometry(f"{self.width}x{self.height}")

    def set_language(self, code:str='en'): # lanuage code
        self.language_code = code
        self.ui_texts = self.__load_ui_texts()

        self.tool_bar.update_ui_texts(self.ui_texts["menubar"])
        
        for i, tab in enumerate(self.tabs):
            lang_pack = list(self.ui_texts["tabs"].values())[i]
            tab.update_ui_texts(lang_pack)
            self.tab_notebook.tab(i, text = lang_pack["name"])

        self.variables["button"].set(self.ui_texts["Generate"])
    #def set_resources_datas(self, urls:dict, images:dict, mics:dict, language_code:str="en"):
    #    self.language_code = language_code
    #    pass
    def locating_layout(self):
        self.tab_notebook.grid(row=0, column=0, pady=10)

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
        super().__init__(parent, *args, **kwargs)
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
            self.entryconfigure(i, label = self.ui_texts[menu]["name"])
            if menu != "language":
                for j in range(0, len(self.ui_texts[menu]["submenu"])):
                    label_value = list(self.ui_texts[menu]["submenu"].values())[j]
                    self.menus[i].entryconfigure(j, label = label_value)

    
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
        self.parent.set_language(lang_code)
    def update_ui_texts(self, language_pack):
        self.ui_texts = language_pack
        self.set_ui_texts()

# Frame in Tabs
# essential routine: localization
#   All frame must provide 'set' and 'update' routine of its ui texts with the given lanugage arguments.

class Manuscript(tk.LabelFrame):
    def __init__(self, parent, language_pack, resources, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        #------------------------------------------
        self.grid_propagate(True)
        self.width = 0
        self.height = 0
        if "width" in kwargs.keys():
            self.width = kwargs["width"]
        if "height" in kwargs.keys():
            self.height= kwargs["height"]
        # Temperorary Zone
        self.font= {"size":12}

        #------------------------------------------
        self.ui_texts = language_pack
        self.resources = resources
        self.button_images = {}
        
        # UI strings
        super().config(text=self.ui_texts["name"])

        # Value variables
        self.selected_file_name = tk.StringVar(value="")
        
        self.texts = []
        self.variables ={}
        self.main_frame = ttk.Frame(self, width=self.width, height=self.height)
        self.frame= {
            "search_file": ttk.Frame(self.main_frame, width = self.width),
            "files": ttk.Frame(self.main_frame),
            "buttons": ttk.Frame(self.main_frame, width= int(0.2*self.width))
            }
        for key in self.resources["images"].keys():
            self.button_images[key] = ImageTk.PhotoImage(self.resources["images"][key], master = self.frame["buttons"])

        # Funtional variables
        self.file_list = [] 
        self.focused_file = None
        self.sorted = False
        self.sort_type = True # True: ascend False: descend 
        self.focused_files_pre = []


        # Frame 1 search bar
        self.selected_file = ttk.Entry(
            self.frame["search_file"], 
            textvariable= self.selected_file_name,
            state="disabled")
        self.search_button = ttk.Button(
            self.frame["search_file"], 
            width=5  )
        self.__set_search_file_frame()
        
        # Frame 2 files list
        self.selected_files = ttk.Treeview(self.frame["files"])
        self.selected_files_scroll_y = ttk.Scrollbar(self.frame["files"])
        self.__set_files_frame()
        
        # Frame 3 buttons
        self.modulate_files_up = tk.Button(self.frame["buttons"])
        self.modulate_files_down = tk.Button(self.frame["buttons"])
        self.modulate_files_delete = tk.Button(self.frame["buttons"])
        self.modulate_files_delete_all = tk.Button(self.frame["buttons"])
        self.modulate_files_sort = tk.Button(self.frame["buttons"])
        self.__set_modulate_buttons_frame()
        
        # Event assign 

        # Locate layout elements
        
        self.frame["search_file"].grid(row = 0, column= 0, columnspan =2, padx=0, pady=2, sticky=tk.W+tk.N)
        self.frame["files"].grid(row = 1, padx=0, pady=2, column=0, sticky=tk.W+tk.N)
        self.frame["buttons"].grid(row = 1, ipadx=0, padx=0, pady=2, column=1, sticky=tk.N+tk.W)

        self.main_frame.pack(padx=10, fill=tk.BOTH)
    def update_ui_texts(self, language_pack):
        self.ui_texts = language_pack
        super().config(text=self.ui_texts["name"])
        self.selected_files.heading("#2", text=self.ui_texts["strings"]["files"])
    # Frame set
    def __set_search_file_frame(self):
        self.variables["selected_file"] = tk.StringVar(value="")
        #characters_number = self.__get_character_width()
        self.selected_file.configure(
            textvariable=self.variables["selected_file"],
            width = 42
            )
        self.search_button.configure(text="...", command=self.__method_open_file, width = 4)

        self.selected_file.grid(row=0, column=0, padx=2, sticky=tk.W)
        self.search_button.grid(row=0, column=1, padx=2, ipadx=2)
    def __set_files_frame(self):
        self.selected_files.configure(
            height = 8, 
            padding = 2, 
            columns = [" ","files"],
            displaycolumns=[" ","files"],
            show = 'headings', 
            selectmode = "extended"
            )
        self.selected_files.heading(" ", text=" ")
        self.selected_files.column(" ", width=10)
        self.selected_files.heading("files", text=self.ui_texts["strings"]["files"])
        self.selected_files.column("files", width=250, stretch=True)

        self.frame["files"].configure(width=int(self.width), height=self.height)
        self.frame["files"].grid_propagate(False)
        
        # Event assign
        self.selected_files.bind("<ButtonRelease-1>", self.__method_focusing_file)

        self.selected_files.config(
            yscrollcommand = self.selected_files_scroll_y.set
            )
        self.selected_files_scroll_y.config(command= self.selected_files.yview, orient="vertical")

        self.selected_files.grid(           row=0, column=0, pady=0, padx=0, sticky=tk.W+tk.N)
        self.selected_files_scroll_y.grid(  row=0, column=1, pady=0, padx=0, sticky=tk.E+tk.N+tk.S)
    def __set_modulate_buttons_frame(self):
        # Style settings:
        self.modulate_files_up.configure(bd=0)
        self.modulate_files_down.configure(bd=0)
        self.modulate_files_delete.configure(bd=0)
        self.modulate_files_delete_all.configure(bd=0)
        self.modulate_files_sort.configure(bd=0)
        # Resource assign
        self.modulate_files_up.configure(image = self.button_images['up'])
        self.modulate_files_down.configure(image = self.button_images['down'])
        self.modulate_files_delete.configure(image = self.button_images['delete'])
        self.modulate_files_delete_all.configure(image = self.button_images['delete_all'])
        self.modulate_files_sort.configure(image = self.button_images['sort_up'])
        
        # Method assign
        self.modulate_files_up.configure(command=partial(self.__method_move_file, True))
        self.modulate_files_down.configure(command=partial(self.__method_move_file, False))
        self.modulate_files_delete.configure(command=self.__method_remove_selected_ones)
        self.modulate_files_delete_all.configure(command=self.__method_remove_all)
        self.modulate_files_sort.configure(command=self.__method_sort)

        # Events assign
        self.modulate_files_up.bind("<Enter>", partial(self.__effect_hover_button, button_name="up", type_e=True))
        self.modulate_files_up.bind("<Leave>", partial(self.__effect_hover_button, button_name="up", type_e=False))
        self.modulate_files_down.bind("<Enter>", partial(self.__effect_hover_button, button_name="down", type_e=True))
        self.modulate_files_down.bind("<Leave>", partial(self.__effect_hover_button, button_name="down", type_e=False))
        self.modulate_files_delete.bind("<Enter>", partial(self.__effect_hover_button, button_name="delete", type_e=True))
        self.modulate_files_delete.bind("<Leave>", partial(self.__effect_hover_button, button_name="delete", type_e=False))
        self.modulate_files_delete_all.bind("<Enter>", partial(self.__effect_hover_button, button_name="delete_all", type_e=True))
        self.modulate_files_delete_all.bind("<Leave>", partial(self.__effect_hover_button, button_name="delete_all", type_e=False))
        self.modulate_files_sort.bind("<Enter>", partial(self.__effect_hover_button, button_name="sort", type_e=True))
        self.modulate_files_sort.bind("<Leave>", partial(self.__effect_hover_button, button_name="sort", type_e=False))

        # Locate
        self.modulate_files_sort.grid(row=0, column=0, pady=2, sticky=tk.N+tk.W)
        self.modulate_files_up.grid(row = 1, column=0, pady=2, sticky=tk.N+tk.W)
        self.modulate_files_down.grid(row = 2, column=0, pady=2, sticky=tk.N+tk.W)
        self.modulate_files_delete.grid(row = 3, column=0, pady=2, sticky=tk.N+tk.W)
        self.modulate_files_delete_all.grid(row= 4 , column=0, pady=2, sticky=tk.N+tk.W)
        
    # Intertal_methods
    #def __get_character_width(self):
    #    point = self.font["size"]
    #    pixel_width = int(self.width*0.8)
    #    glyph_width = 3.5
    #    return int(pixel_width/glyph_width)
    def __get_file_infos(self, file_path):
        if type(file_path) != str and not isinstance(file_path, Path):
            raise TypeError(
                f"Given path must be a string variable. Current:{type(file_path)}"
            )
        if type(file_path) == str:
            file_path =Path(file_path)

        if not file_path.is_file():
            raise ValueError("File {file_path} does not exist.")
        
        pdf = pypdf.PdfFileReader(file_path)
        file ={
            "name": file_path.name,
            "path": file_path,
            "title": None,
            "authors" : None,
            "created_date": None,
            "mod_date": None,
            "pages" : len(pdf.pages),
            "page_size": (float(pdf.getPage(0).mediaBox.width), float(pdf.getPage(0).mediaBox.height))
        }
        pdfinfos = pdf.metadata
        file["title"] = pdfinfos["/Title"] if "/Title" in pdfinfos.keys() else None
        file["authors"] = pdfinfos["/Author"] if "/Author" in pdfinfos.keys() else None
        file["created_date"] = pdfinfos["/CreationDate"] if "/CreationDate" in pdfinfos.keys() else None
        file["mod_date"] = pdfinfos["/ModDate"] if "/ModDate" in pdfinfos.keys() else None
        
        return file 
    def __get_focused_file(self):
        current_selection = self.selected_files.selection()
        focused_file = None
        if len(current_selection) ==0:
            return 0
        elif len(current_selection) == 1:
            self.focused_files_pre = list(current_selection)
            focused_file = current_selection[0]
        else:
            for file in current_selection:
                if not file in self.focused_files_pre:
                    self.focused_files_pre.append(file)
                    focused_file = file
        if focused_file is None: return False
        else: return self.selected_files.index(focused_file), focused_file
    # Effects
    def __effect_hover_button(self, event, button_name, type_e): # type_e = True: enter, leave
        if button_name != "sort":
            key = button_name + ("_hover" if type_e else "") 
        elif button_name == "sort":
            key_name = button_name+("_up" if self.sort_type else "_down") 
            key = key_name + ("_hover" if type_e else "") 
        
        if button_name == "up":
                button = self.modulate_files_up
        elif button_name  == "down":
            button = self.modulate_files_down
        elif button_name == "delete":
            button = self.modulate_files_delete
        elif button_name == "delete_all":
            button = self.modulate_files_delete_all
        elif button_name == "sort":
            button = self.modulate_files_sort
        button.configure(image = self.button_images[key])
    # Methods
    def __method_focusing_file(self, event):
        focused_index, focused = self.__get_focused_file()
        if focused:
            # Get file object
            print("index:", focused_index)
            print("file_list:", [ item["name"] for item in self.file_list])
            children = self.selected_files.get_children()
            print("treeview:", children)
            for item in children:
                print("items:", self.selected_files.item(item))
            file = self.file_list[focused_index]
            # Set entry  
            self.variables["selected_file"].set(str(file["path"]))
            self.focused_file = file
        else:
            pass
    def __method_open_file(self):
        filenames = filedialog.askopenfilenames(
            initialdir="~", title="Select Manuscript", filetypes=(("PDF", "*.pdf"),)
        )
        if len(filenames) != 0:
            for filename in filenames:
                file= self.__get_file_infos(filename)

                self.file_list.append(file)
                self.focused_file = file

                self.variables["selected_file"].set(str(self.focused_file["path"]))
                # Add to treeview
                self.selected_files.insert("", "end", values=(len(self.file_list), file["name"]))
                self.selected_files.get_children()
        else:
            print(f"Not a vaild PDF file: file ({filenames})")
        
        self.sorted = False
    def __method_move_file(self, direction=True):
        focused_index, focused = self.__get_focused_file()
        if not focused:
            return 1

        if direction: # up
            previous = self.selected_files.prev(focused)
            if previous != "": # Not a top
                self.selected_files.move(focused, self.selected_files.parent(focused), focused_index-1)
                self.file_list = exchange(focused_index, focused_index-1, self.file_list)
                to_index = focused_index-1
            else: # Top
                return 2
        else: # down
            next = self.selected_files.next(focused)
            if next !="":
                self.selected_files.move(focused, self.selected_files.parent(focused), focused_index+1)
                self.file_list = exchange(focused_index, focused_index+1, self.file_list)
                to_index = focused_index+1
            else:
                return 3
        remains = []
        for item in self.selected_files.get_children():
            remains.append(self.selected_files.item(item)["values"])
            self.selected_files.delete(item)
        for i, value in enumerate(remains):
            self.selected_files.insert('', 'end', values=(i+1, value[1]))
        
        self.selected_files.selection_add(self.selected_files.get_children()[to_index])

        self.sorted = False
    def __method_remove_selected_ones(self):
        selected_index= self.selected_files.selection()
        non_selected_index = [self.selected_files.index(item) for item in self.selected_files.get_children() if item not in selected_index]
        files_remained = []
        for i in non_selected_index:
            files_remained.append(self.file_list[i])
        self.file_list = files_remained
        for item in self.selected_files.selection():
            self.selected_files.delete(item)
        
        remains = []
        for item in self.selected_files.get_children():
            remains.append(self.selected_files.item(item)["values"])
            self.selected_files.delete(item)
        for i, value in enumerate(remains):
            self.selected_files.insert('', 'end', values=(i+1, value[1]))
    def __method_remove_all(self):
        for item in self.selected_files.get_children():
            self.selected_files.delete(item)
        self.file_list = []
        self.variables["selected_file"].set("")

        self.sorted = False
    def __method_sort(self, event=None):
        print("Sort")
        print("Current State:", self.sorted)
        print("Sort type:", "Ascend" if self.sort_type else "Dscend")

        item_names = [self.selected_files.item(item)["values"][1] for item in self.selected_files.get_children()]

        if self.sort_type: # ascend
            item_names = sorted(item_names)
            self.file_list = sorted(self.file_list, key= lambda x: x['name'])
            self.sort_type = False
        else: # descend
            item_names = sorted(item_names, reverse=True)
            self.file_list = sorted(self.file_list, key= lambda x: x['name'], reverse=True)
            self.sort_type = True

        for item in self.selected_files.get_children():
            self.selected_files.delete(item)
        for i, name in enumerate(item_names):
            self.selected_files.insert('','end', values=(i+1, name))

        self.sorted = True
    @property
    def focused_file_info(self):
        return self.focused_file
class FileInfo(tk.LabelFrame):
    def __init__(self, parent, language_pack, resources, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        #------------------------------------------
        self.grid_propagate(True)
        self.width = 0
        self.height = 0
        if "width" in kwargs.keys():
            self.width = kwargs["width"]
        if "height" in kwargs.keys():
            self.height= kwargs["height"]
        # Temperorary Zone
        self.font= {"size":12}

        #------------------------------------------
        self.ui_texts = language_pack
        self.resources = resources
        
        # UI strings
        super().config(text=self.ui_texts["name"])
        self.ui_texts_variables = {
            "name": tk.StringVar(value=self._ui_texts["strings"]["name"]),
            "path": tk.StringVar(value=self._ui_texts["strings"]["path"]),
            "title": tk.StringVar(value=self._ui_texts["strings"]["title"]),
            "authors" : tk.StringVar(value=self._ui_texts["strings"]["author"]),
            "created_date": tk.StringVar(value=self._ui_texts["strings"]["created_date"]),
            "mod_date": tk.StringVar(value=self._ui_texts["strings"]["mod_date"]),
            "pages" : tk.StringVar(value=self._ui_texts["strings"]["pages"]),
            "page_format": tk.StringVar(value=self._ui_texts["strings"]["page_format"]),
        }
        # Value variables
        self.variables = {
            "name": tk.StringVar(value=""), 
            "path": tk.StringVar(value=""),
            "title": tk.StringVar(value=""),
            "authors": tk.StringVar(value=""),
            "created_date": tk.StringVar(value=""),
            "mod_date": tk.StringVar(value=""),
            "pages": tk.StringVar(value=""),
            "page_format_x": tk.DoubleVar(value=0.),
            "page_format_y": tk.DoubleVar(value=0.)
        }

        # Frame

        self.frame = {
            "texts" : ttk.Frame(self),
            "values" : ttk.Frame(self)
        }

        # Frame 1 "texts"
        self.file_name = ttk.Label(self.frame["texts"])
        self.file_path = ttk.Label(self.frame["texts"])
        self.file_title = ttk.Label(self.frame["texts"])
        self.file_author = ttk.Label(self.frame["texts"])
        self.file_created_date = ttk.Label(self.frame["texts"])
        self.file_mod_date = ttk.Label(self.frame["texts"])
        self.file_pages = ttk.Label(self.frame["texts"])
        self.file_page_format = ttk.Label(self.frame["texts"])
        # Frame 2 "values"

        # Locate
        self.frame["texts"].grid(row=0, column=0, padx =5, pady=2)
        self.frame["values"].grid(row=0, column=1, padx =5, pady=2)

    def __set_text_frame(self):
        pass
    def __set_values_frame(self):
        pass
    def set_ui_strings(self):
        # Title set 
        super().config(text=self.ui_texts["name"])
        for variable, string in zip(self.ui_texts_variables, self.ui_texts["strings"]):
            variable.set(string)
    def update_ui_texts(self):
        pass
class Output(tk.LabelFrame):
    def __init__(self, parent, language_pack, resources, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.ui_texts = language_pack

        #------------------------------------------
        self.grid_propagate(True)
        self.width = 0
        self.height = 0
        if "width" in kwargs.keys():
            self.width = kwargs["width"]
        if "height" in kwargs.keys():
            self.height= kwargs["height"]
        # Temperorary Zone
        self.font= {"size":12}

        #------------------------------------------
        self.ui_texts = language_pack
        self.resources = resources

        # UI strings
        super().config(text=self.ui_texts["name"])
        self.ui_texts_variables = {
            "merge": tk.StringVar(value=""),
            "total_pages": tk.StringVar(value=""),
            "name": tk.StringVar(value="")
        }
        # Value variables
        self.variables = {
            "output_path": tk.StringVar(value=""),
            "name" : tk.StringVar(value=""),
            "prefix" : tk.StringVar(value=""),
            "suffix" : tk.StringVar(value="")
        }

        # Frame

        self.frame = {
            "merge": ttk.Frame(self),
            "name" : ttk.Frame(self),
            "output_path": ttk.Frame(self)
        }

        # Frame 1 "merge"
        self.frame["merge"]
        # Frame 2 "name"
        self.frame["name"]
        self.name_label = ttk.Label(self.frame["name"])
        # Frame 3 "output_path"
        self.frame["output_path"]
        


        self.frame["merge"].grid(row=0, column=0)
        self.frame["name"].grid(row=1, column=0)
        self.frame["output_path"].grid(row=2, column=0)
    def update_ui_texts(self):
        pass

class Files(tk.Frame):
    def __init__(self, parent, language_pack, resources, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.width = 0
        self.height = 0
        if "width" in kwargs.keys():
            self.width = kwargs["width"]
        if "height" in kwargs.keys():
            self.height= kwargs["height"]

        self.ui_texts = language_pack
        self.name = self.ui_texts["name"]
        self.resources = resources
        #temp
        #self.resources["manuscript"] = ""
        #self.resources["file-info"] = ""
        #self.resources["output"] = ""


        self.frames = [
            Manuscript(self, self.ui_texts["frames"]["manuscript"], self.resources["manuscript"], width=int(self.width/2), height=int(0.75*self.height)),
            #FileInfo(self, self.ui_texts["frames"]["file_info"], self.resources["file-info"]),
            #Output(self, self.ui_texts["frames"]["output"], self.resources["output"])
        ]

        self.set_frame_layout()
        
    def set_frame_layout(self):
        self.frames[0].grid(row=0, column=0, rowspan=2, pady = 5, padx=5)
        #self.frames[1].grid(row=0, column=1)
        #self.frames[2].grid(row=1, column=1)

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
        self.ui_texts = string_pack
        self.name = self.ui_texts["name"]
        strings =[]
        if "strings" in self.ui_texts.keys():
            for st in self.ui_texts["strings"]:
                strings.append(st)
            for value, st in zip(self.strings, strings):
                if isinstance(value, tk.StringVar):
                    value.set(st)
        for i, frame_pack in zip(range(0, len(self.frames)), self.ui_texts["frames"].values()):
            self.frames[i].update_ui_texts(frame_pack)
        
        # Additional set for non-StringVar() texts.

    def update_ui_texts(self, string_pack):
        self.set_ui_texts(string_pack)


class Section(tk.Frame):
    name = "Section"
    def __init__(self, parent, language_pack,  *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent

    def update_ui_texts(self):
        pass
class Imposition(tk.Frame):
    name = "Imposition"
    def __init__(self, parent, language_pack,  *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent

    def update_ui_texts(self):
        pass

class PrintingMark(tk.Frame):
    name = "Printing Marks"
    def __init__(self, parent, language_pack,  *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent

    def update_ui_texts(self):
        pass

class Utils(tk.Frame):
    name = "Utils"
    def __init__(self, parent, language_pack,  *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent

    def update_ui_texts(self):
        pass

import os
# Independent Frame
class ProgressBar(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent


if __name__ == "__main__":
    #font = tk.font.Font(family="Noto Serif", size=12)
    resources = {
        "Files": {
            "manuscript": {"images": data.button_icons_manuscripts}
            },
        }
    ui = UI(language_code="en", width=650, height=500, resources= resources)
    ui.mainloop()