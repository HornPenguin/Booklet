import tkinter as tk
from tkinter import Toplevel, ttk
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

class HPPopUp(Toplevel):
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


# Based on
#   https://web.archive.org/web/20170514022131id_/http://tkinter.unpythonic.net/wiki/VerticalScrolledFrame

class HPFrameVScroll(HPFrame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame.
    * Construct and pack/place/grid normally.
    * This frame only allows vertical scrolling.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Create a canvas object and a vertical scrollbar for scrolling it.
        self.vscrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL)
        self.vscrollbar.grid(row=0, column=1, sticky = tk.N+tk.S+tk.E)
        #self.vscrollbar.pack(fill=tk.Y, side=tk.RIGHT, expand=tk.FALSE)
        self.canvas = tk.Canvas(self, bd=0, highlightthickness=0,
                           yscrollcommand=self.vscrollbar.set)
        #canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)
        self.canvas.grid(row=0, column=0, sticky=tk.W+tk.E)
        self.vscrollbar.config(command=self.canvas.yview)

        # Reset the view
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        # Create a frame inside the canvas which will be scrolled with it.
        self.interior = HPFrame(self.canvas)
        self.interior_id = self.canvas.create_window(0, 0, window=self.interior,
                                           anchor=tk.NW)

        # Track changes to the canvas and frame width and sync them,
        # also updating the scrollbar.
        def _configure_interior(event):
            # Update the scrollbars to match the size of the inner frame.
            size = (self.interior.winfo_reqwidth(), self.interior.winfo_reqheight())
            self.canvas.config(scrollregion="0 0 %s %s" % size)
            if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
                # Update the canvas's width to fit the inner frame.
                self.canvas.config(width=self.interior.winfo_reqwidth())
        self.interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
                # Update the inner frame's width to fill the canvas.
                self.canvas.itemconfigure(self.interior_id, width=self.canvas.winfo_width())
        self.canvas.bind('<Configure>', _configure_canvas)

    def scroll_region_update(self):
        self.canvas.update_idletasks()
        self.canvas.config(scrollregion=self.interior.bbox())


