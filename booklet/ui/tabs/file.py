import sys
from functools import partial
from pathlib import Path


from tkinter import Button as tk_Button
from tkinter import W, E, N, S, BOTH
from tkinter import StringVar, IntVar, DoubleVar
from tkinter import DISABLED, ACTIVE
from tkinter import filedialog

from tkinter.ttk import Button, Label, Frame, Entry, Treeview, Scrollbar
if sys.platform.startswith("darwin"):
    from tkmacosx import Button

from PIL import Image, ImageTk
import PyPDF2 as pypdf

from booklet.ui import HPFrame, HPLabelFrame
from booklet.utils.matrix import exchange


class FileIO(HPFrame):
    def __init__(self, *args, **kwargs):
        self.width = kwargs["width"] if "width" in kwargs.keys() else 0
        self.height = kwargs["height"] if "height" in kwargs.keys() else 0
        #del(kwargs["width"])
        #del(kwargs["height"])
        
        super().__init__(*args, **kwargs)
        
        self.main_frame = HPFrame(self, width=self.width, height=self.height)

        self.sub_frames.append(
                Manuscript(
                    self.main_frame, 
                    self.ui_texts["frames"]["manuscript"],
                    self.resources["manuscript"],
                    width = int(0.5*self.width),
                    height = self.height
                )
            )
        self.sub_frames.append(
                FileInfo(
                    self.main_frame, 
                    self.ui_texts["frames"]["file_info"],
                    self.resources["manuscript"],
                    width = int(0.5*self.width),
                    height = int(0.55*self.height)
                )
            )
        self.sub_frames.append(
                Output(
                    self.main_frame, 
                    self.ui_texts["frames"]["output"],
                    self.resources["manuscript"],
                    width = int(0.5*self.width),
                    height = int(0.45*self.height)
                )
            )

        self.sub_frames[0].grid(row = 0, column = 0, rowspan = 2, padx = 10, pady = 2, ipady=4)
        self.sub_frames[1].grid(row = 0, column = 1, rowspan = 1, padx = 10, pady = 2, ipady=4)
        self.sub_frames[2].grid(row = 1, column = 1, rowspan = 1, padx = 10, pady = 2, ipady=4)
        self.main_frame.pack( padx =1, pady=1)
    
    @property
    def settings(self):
        pass
    @settings.setter
    def settings(self, *args):
        pass

class Manuscript(HPLabelFrame):
    # --------------------------
    # |      search_file       |
    # |------------------------| 
    # |             |          |
    # |    files    | buttons  |
    # |             |          |
    # --------------------------

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        

        self.main_frame = Frame(self, width = self.width, height = self.height)
        self.layout_frames = {
            "search_file": HPFrame(self.main_frame, width=self.width),
            "files": HPFrame(self.main_frame),
            "buttons": HPFrame(self.main_frame, width= int(0.2*self.width)),
        }
        # Locate layout elements
        
        self.layout_frames["search_file"].grid(row = 0, column= 0, columnspan =2, padx=0, pady=2, sticky=W+N)
        self.layout_frames["files"].grid(row = 1, padx=0, pady=2, ipady=4, column=0, sticky=W+N+S)
        self.layout_frames["buttons"].grid(row = 1, ipadx=0, padx=0, pady=2, column=1, sticky=N+W)

        self.button_images ={}
        for key in self.resources["images"]["button"].keys():
            self.button_images[key] = ImageTk.PhotoImage(self.resources["images"]["button"][key], master = self.layout_frames["buttons"])

        # Variables
        self.selected_file_name = StringVar(value="")
        
        self.texts = []
        self.string_vars ={}

        # Funtional variables
        self.file_list = [] 
        self.focused_file = None
        self.sorted = False
        self.sort_type = True # True: ascend False: descend 
        self.focused_files_pre = []

        # Frame 1 search bar
        self.selected_file = Entry(
            self.layout_frames["search_file"], 
            textvariable= self.selected_file_name,
            state="disabled")
        self.search_button = Button(
            self.layout_frames["search_file"], 
            width=5  )
        self.__set_search_file_frame()
        
        # Frame 2 files list
        self.selected_files = Treeview(self.layout_frames["files"])
        self.selected_files_scroll_y = Scrollbar(self.layout_frames["files"])
        self.__set_files_frame()
        
        # Frame 3 buttons Button
        self.modulate_files_up = tk_Button(self.layout_frames["buttons"])
        self.modulate_files_down = tk_Button(self.layout_frames["buttons"])
        self.modulate_files_delete = tk_Button(self.layout_frames["buttons"])
        self.modulate_files_delete_all = tk_Button(self.layout_frames["buttons"])
        self.modulate_files_sort = tk_Button(self.layout_frames["buttons"])
        self.__set_modulate_buttons_frame()
        
        # Event assign 

        
        self.main_frame.pack(padx=10, fill=BOTH)
    def update_ui_texts(self, language_pack):
        self.ui_texts = language_pack
        super().config(text=self.ui_texts["name"])
        self.selected_files.heading("#2", text=self.ui_texts["strings"]["files"])
    # Frame set
    def __set_search_file_frame(self):
        self.string_vars["selected_file"] = StringVar(value="")
        #characters_number = self.__get_character_width()
        self.selected_file.configure(
            textvariable=self.string_vars["selected_file"],
            width = 42
            )
        self.search_button.configure(text="...", command=self.__method_open_file, width = 4)

        self.selected_file.grid(row=0, column=0, padx=2, sticky=W)
        self.search_button.grid(row=0, column=1, padx=2, ipadx=2)
    def __set_files_frame(self):
        self.selected_files.configure(
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

        self.layout_frames["files"].configure(width=int(self.width), height=self.height)
        
        # Event assign
        self.selected_files.bind("<ButtonRelease-1>", self.__method_focusing_file)

        self.selected_files.config(
            yscrollcommand = self.selected_files_scroll_y.set
            )
        self.selected_files_scroll_y.config(command= self.selected_files.yview, orient="vertical")

        self.selected_files.grid(           row=0, column=0, pady=0, padx=0, sticky=W+N)
        self.selected_files_scroll_y.grid(  row=0, column=1, pady=0, padx=0, sticky=E+N+S)
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
        self.modulate_files_sort.grid(row=0, column=0, pady=2, sticky=N+W)
        self.modulate_files_up.grid(row = 1, column=0, pady=2, sticky=N+W)
        self.modulate_files_down.grid(row = 2, column=0, pady=2, sticky=N+W)
        self.modulate_files_delete.grid(row = 3, column=0, pady=2, sticky=N+W)
        self.modulate_files_delete_all.grid(row= 4 , column=0, pady=2, sticky=N+W)
        
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
            pass
        elif len(current_selection) == 1:
            self.focused_files_pre = list(current_selection)
            focused_file = current_selection[0]
        else:
            for file in current_selection:
                if not file in self.focused_files_pre:
                    self.focused_files_pre.append(file)
                    focused_file = file
                    
        if focused_file is None: return (False, False)
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
            self.string_vars["selected_file"].set(str(file["path"]))
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

                self.string_vars["selected_file"].set(str(self.focused_file["path"]))
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
        self.string_vars["selected_file"].set("")

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

class FileInfo(HPLabelFrame):
    # -----------------------
    # |             |       |
    # | left_labels | print |
    # |             |       |
    # -----------------------
    #
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        

        self.main_frame = HPFrame(self)
        self.layout_frames ={
            "left_labels" : HPFrame(self.main_frame),
            "print" : HPFrame(self.main_frame),
        }

        # Variable
        self.file_infos ={
            "name": StringVar(value =""),
            "path": StringVar(value =""),
            "title": StringVar(value =""),
            "authors" : StringVar(value =""),
            "created_date": StringVar(value =""),
            "mod_date": StringVar(value =""),
            "pages" : StringVar(value =""),
            "page_size": (DoubleVar(value=0.0), DoubleVar(value=0.0))
        }
        
        # Frame 1 left_labels
        self.string_vars["name"] = StringVar(value=self.ui_texts["strings"]["name"])
        self.string_vars["path"] = StringVar(value=self.ui_texts["strings"]["path"])
        self.string_vars["title"] = StringVar(value=self.ui_texts["strings"]["title"])
        self.string_vars["author"] = StringVar(value=self.ui_texts["strings"]["author"])
        self.string_vars["created_date"] = StringVar(value=self.ui_texts["strings"]["created_date"])
        self.string_vars["mod_date"] = StringVar(value=self.ui_texts["strings"]["mod_date"])
        self.string_vars["pages"] = StringVar(value=self.ui_texts["strings"]["pages"])
        self.string_vars["page_size"] = StringVar(value=self.ui_texts["strings"]["page_format"])

        self.name_label = Label(self.layout_frames["left_labels"], textvariable=self.string_vars["name"])
        self.path_label = Label(self.layout_frames["left_labels"], textvariable=self.string_vars["path"])
        self.title_label = Label(self.layout_frames["left_labels"], textvariable=self.string_vars["title"])
        self.author_label = Label(self.layout_frames["left_labels"], textvariable=self.string_vars["author"])
        self.create_date_label = Label(self.layout_frames["left_labels"], textvariable=self.string_vars["created_date"])
        self.mod_date_label = Label(self.layout_frames["left_labels"], textvariable=self.string_vars["mod_date"])
        self.pages_label = Label(self.layout_frames["left_labels"], textvariable=self.string_vars["pages"])
        self.page_size_label = Label(self.layout_frames["left_labels"], textvariable=self.string_vars["page_size"])
        self.__set_left_labels_frame()

        # Frame 2 print
        self.name_label_var = Label(self.layout_frames["print"], textvariable=self.file_infos["name"])
        self.path_label_var =  Label(self.layout_frames["print"], textvariable=self.file_infos["path"])
        self.title_label_var = Label(self.layout_frames["print"], textvariable=self.file_infos["title"])
        self.author_label_var = Label(self.layout_frames["print"], textvariable=self.file_infos["authors"])
        self.create_date_label_var = Label(self.layout_frames["print"], textvariable=self.file_infos["created_date"])
        self.mod_date_label_var = Label(self.layout_frames["print"], textvariable=self.file_infos["mod_date"])
        self.pages_label_var = Label(self.layout_frames["print"], textvariable=self.file_infos["pages"])

        self.page_size_frame = HPFrame(self.layout_frames["print"])
        self.page_size_width_label_var = Label(self.page_size_frame, textvariable=self.file_infos["page_size"][0])
        self.page_size_product = Label(self.page_size_frame) # Product image
        self.page_size_height_label_var = Label(self.page_size_frame, textvariable=self.file_infos["page_size"][1])
        self.__set_print_frame()

        self.layout_frames["left_labels"].grid(row=0, column=0)
        self.layout_frames["print"].grid(row=0, column=1)
        self.main_frame.pack(padx=10, fill=BOTH)
    
    def __set_left_labels_frame(self):
        self.name_label.grid(       row = 0, column = 0, pady=1, padx=2 )
        self.path_label.grid(       row = 1, column = 0, pady=1, padx=2 )
        self.title_label.grid(      row = 2, column = 0, pady=1, padx=2 )
        self.author_label.grid(     row = 3, column = 0, pady=1, padx=2 )
        self.create_date_label.grid(row = 4, column = 0, pady=1, padx=2 )
        self.mod_date_label.grid(   row = 5, column = 0, pady=1, padx=2 )
        self.pages_label.grid(      row = 6, column = 0, pady=1, padx=2 )
        self.page_size_label.grid(  row = 9, column = 0, pady=1, padx=2 )

        self.layout_frames["left_labels"].configure(width = int(0.45*self.width))
    def __set_print_frame(self):
        self.layout_frames["print"].configure(width = int(0.55*self.width))

    def __update_file_infos(self):
        focused = self.parent.sub_frames[0].focused_file # Manuscript
        if focused is  not None:
            for key in focused.keys():
                self.file_infos[key].set(focused[key])
    
    def update_ui_texts(self, ui_texts):
        super().update_ui_texts(ui_texts)
        super().config(text=self.ui_texts["name"])


class Output(HPLabelFrame):
    # --------------------------  
    # |             |          |
    # | left_labels |  inputs  |
    # |             |          |
    # |------------------------|
    # |       output_dir       |
    # --------------------------
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        

        self.layout_frames = {
            "left_label": HPFrame(self, width = int(0.33*self.width)),
            "name": HPFrame(self, width = int(0.33*self.width)),
            "output_dir": HPFrame(self, width = int(0.33*self.width)),
        }