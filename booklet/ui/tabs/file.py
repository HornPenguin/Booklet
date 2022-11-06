from functools import partial
from pathlib import Path

from PIL import Image, ImageTk
import PyPDF2 as pypdf

from booklet.ui.tabs import *
from booklet.ui import Validate, HPFrame, HPLabelFrame, HPVScrollWapper
from booklet.utils.conversion import pts2mm
from booklet.utils.matrix import exchange
from booklet.utils.pdftime import pdf2local_time





class FileIO(HPFrame):
    MANUSCRIPT = 0
    FILEINFO = 1
    OUTPUT =2
    def __init__(self, *args, **kwargs):
        #self.width = kwargs["width"] if "width" in kwargs.keys() else 0
        #self.height = kwargs["height"] if "height" in kwargs.keys() else 0
        super().__init__(*args, **kwargs)
        self.grid_anchor(CENTER)
        
        
        #self.main_frame = HPFrame(self, width=self.width, height=self.height)

        self.sub_frames.append(
                Manuscript(
                    self, 
                    self.ui_texts["frames"]["manuscript"],
                    self.resources["manuscript"],
                    width = int(0.5*self.width),
                    height = self.height
                )
            )
        self.sub_frames.append(
                FileInfo(
                    self, 
                    self.ui_texts["frames"]["file_info"],
                    self.resources["manuscript"],
                    width = int(0.5*self.width),
                    height = int(0.55*self.height)
                )
            )
        self.sub_frames.append(
                Output(
                    self, 
                    self.ui_texts["frames"]["output"],
                    self.resources["manuscript"],
                    width = int(0.5*self.width),
                    height = int(0.45*self.height)
                )
            )

        self.sub_frames[0].grid(row = 0, column = 0, rowspan = 2, padx = 10, pady = 2, ipady=4, sticky = N+S+E+W)
        self.sub_frames[2].grid(row = 1, column = 1, rowspan = 1, padx = 10, pady = 2, ipady=4, sticky = N+S+E+W)
        self.sub_frames[1].grid(row = 0, column = 1, rowspan = 1, padx = 10, pady = 2, ipady=4, sticky = N+S+E+W)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
    @property
    def settings(self):
        pass
    @settings.setter
    def settings(self, *args):
        pass

    #def call_frames_routine(self, frame_index, attr_name, *args, **kwargs):
    #    method = getattr(self.sub_frames[frame_index], attr_name)
    #    method(*args, **kwargs)
    #def get_frames_property(self, frame_index, attr_name):
    #    return getattr(self.sub_frames[frame_index], attr_name)

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
        self.grid_anchor(CENTER)

        self.main_frame = HPFrame(self, width = self.width, height = self.height)
        self.layout_frames = {
            "search_file": HPFrame(self.main_frame, width=self.width),
            "files": HPFrame(self.main_frame, width= int(0.79*self.width)),
            "buttons": HPFrame(self.main_frame, width= int(0.2*self.width)),
        }
        
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
        self.set_search_file_frame()
        
        # Frame 2 files list
        self.selected_files = Treeview(self.layout_frames["files"])
        self.selected_files_scroll_y = Scrollbar(self.layout_frames["files"])
        self.set_files_frame()
        
        # Frame 3 buttons Button
        self.modulate_files_up = tk_Button(self.layout_frames["buttons"])
        self.modulate_files_down = tk_Button(self.layout_frames["buttons"])
        self.modulate_files_delete = tk_Button(self.layout_frames["buttons"])
        self.modulate_files_delete_all = tk_Button(self.layout_frames["buttons"])
        self.modulate_files_sort = tk_Button(self.layout_frames["buttons"])
        self.set_modulate_buttons_frame()
        
        # Event assign 

        # Locate layout elements
        
        self.layout_frames["search_file"].grid(row = 0, column= 0, columnspan =2, padx=0, pady=2, sticky=W+N)
        self.layout_frames["files"].grid(row = 1, column=0, padx=0, pady=2, ipady=2,  sticky=W+N+S)
        self.layout_frames["buttons"].grid(row = 1,  column=1, ipadx=0, padx=0, pady=2, sticky=N+W)

        self.main_frame.pack(padx=10, fill=BOTH)

        

    def update_ui_texts(self, language_pack):
        self.ui_texts = language_pack
        super().config(text=self.ui_texts["name"])
        self.selected_files.heading("#2", text=self.ui_texts["strings"]["files"])
    # Frame set
    def set_search_file_frame(self):
        self.string_vars["selected_file"] = StringVar(value="")
        #characters_number = self.get_character_width()
        self.selected_file.configure(
            textvariable=self.string_vars["selected_file"],
            width = 50
            )
        self.search_button.configure(text="...", command=self.method_open_file, width = 4)

        self.selected_file.grid(row=0, column=0, padx=2, sticky=W)
        self.search_button.grid(row=0, column=1, padx=2, ipadx=2)
    def set_files_frame(self):
        self.selected_files.configure(
            padding = 2, 
            height = 17,
            columns = [" ","files"],
            displaycolumns=[" ","files"],
            show = 'headings', 
            selectmode = "extended"
            )
        self.selected_files.heading(" ", text=" ")
        self.selected_files.column(" ", width=10)
        self.selected_files.heading("files", text=self.ui_texts["strings"]["files"])
        self.selected_files.column("files", width=320, stretch=True)

        self.layout_frames["files"].configure(width=int(self.width))
        
        # Event assign
        self.selected_files.bind("<ButtonRelease-1>", self.method_focusing_file)

        self.selected_files.config(
            yscrollcommand = self.selected_files_scroll_y.set
            )
        self.selected_files_scroll_y.config(command= self.selected_files.yview, orient="vertical")

        self.selected_files.grid(           row=0, column=0, pady=0, padx=0, sticky=W+N+S)
        self.selected_files_scroll_y.grid(  row=0, column=1, pady=0, padx=0, sticky=E+N+S)
    def set_modulate_buttons_frame(self):
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
        self.modulate_files_up.configure(command=partial(self.method_move_file, True))
        self.modulate_files_down.configure(command=partial(self.method_move_file, False))
        self.modulate_files_delete.configure(command=self.method_remove_selected_ones)
        self.modulate_files_delete_all.configure(command=self.method_remove_all)
        self.modulate_files_sort.configure(command=self.method_sort)

        # Events assign
        self.modulate_files_up.bind("<Enter>", partial(self.effect_hover_button, button_name="up", type_e=True))
        self.modulate_files_up.bind("<Leave>", partial(self.effect_hover_button, button_name="up", type_e=False))
        self.modulate_files_down.bind("<Enter>", partial(self.effect_hover_button, button_name="down", type_e=True))
        self.modulate_files_down.bind("<Leave>", partial(self.effect_hover_button, button_name="down", type_e=False))
        self.modulate_files_delete.bind("<Enter>", partial(self.effect_hover_button, button_name="delete", type_e=True))
        self.modulate_files_delete.bind("<Leave>", partial(self.effect_hover_button, button_name="delete", type_e=False))
        self.modulate_files_delete_all.bind("<Enter>", partial(self.effect_hover_button, button_name="delete_all", type_e=True))
        self.modulate_files_delete_all.bind("<Leave>", partial(self.effect_hover_button, button_name="delete_all", type_e=False))
        self.modulate_files_sort.bind("<Enter>", partial(self.effect_hover_button, button_name="sort", type_e=True))
        self.modulate_files_sort.bind("<Leave>", partial(self.effect_hover_button, button_name="sort", type_e=False))

        # Locate
        self.modulate_files_sort.grid(row=0, column=0, pady=2, sticky=N+W)
        self.modulate_files_up.grid(row = 1, column=0, pady=2, sticky=N+W)
        self.modulate_files_down.grid(row = 2, column=0, pady=2, sticky=N+W)
        self.modulate_files_delete.grid(row = 3, column=0, pady=2, sticky=N+W)
        self.modulate_files_delete_all.grid(row= 4 , column=0, pady=2, sticky=N+W)
        
    # Intertal_methods
    #def get_character_width(self):
    #    point = self.font["size"]
    #    pixel_width = int(self.width*0.8)
    #    glyph_width = 3.5
    #    return int(pixel_width/glyph_width)
    def get_file_infos(self, file_path):
        if type(file_path) != str and not isinstance(file_path, Path):
            raise TypeError(
                f"Given path must be a string variable. Current:{type(file_path)}"
            )
        if type(file_path) == str:
            file_path =Path(file_path)

        if not file_path.is_file():
            raise ValueError(f"File {str(file_path)} does not exist.")
        
        pdf = pypdf.PdfFileReader(file_path)
        file ={
            "name": file_path.name,
            "path": file_path,
            "title": None,
            "authors" : None,
            "created_date": None,
            "mod_date": None,
            "pages" : len(pdf.pages),
            "page_size": (pts2mm(float(pdf.getPage(0).mediaBox.width)), pts2mm(float(pdf.getPage(0).mediaBox.height)))
        }
        pdfinfos = pdf.metadata
        file["title"] = pdfinfos["/Title"] if "/Title" in pdfinfos.keys() else None
        file["authors"] = pdfinfos["/Author"] if "/Author" in pdfinfos.keys() else None
        if "/CreationDate" in pdfinfos.keys():
            try:
                datetime = pdf2local_time(pdfinfos["/CreationDate"])
                file["created_date"] = datetime.strftime(r"%Y-%m-%d  %H:%M:%S") 
            except:
                file["created_date"] = pdfinfos["/CreationDate"]
        if "/ModDate" in pdfinfos.keys():
            try:
                datetime = pdf2local_time(pdfinfos["/ModDate"])
                file["mod_date"] = datetime.strftime(r"%Y-%m-%d  %H:%M:%S") 
            except:
                file["mod_date"] = pdfinfos["/ModDate"]

        return file 
    def get_focused_file(self):
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
    def effect_hover_button(self, event, button_name, type_e): # type_e = True: enter, leave
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
    def method_focusing_file(self, event):
        focused_index, focused = self.get_focused_file()

        if focused:
            # Get file object
            # print("index:", focused_index)
            # print("file_list:", [ item["name"] for item in self.file_list])
            children = self.selected_files.get_children()
            # print("treeview:", children)
            #for item in children:
            #    print("items:", self.selected_files.item(item))
            file = self.file_list[focused_index]
            # Set entry  
            self.string_vars["selected_file"].set(str(file["path"]))
            self.focused_file = file
            self.parent.call_frames_routine(self.parent.FILEINFO, "update_file_infos", self.focused_file)
        else:
            pass
    def method_open_file(self):
        filenames = filedialog.askopenfilenames(
            __init__ialdir="~", title="Select Manuscript", filetypes=(("PDF", "*.pdf"),)
        )
        if len(filenames) != 0:
            for filename in filenames:
                file= self.get_file_infos(filename)

                self.file_list.append(file)
                self.focused_file = file

                self.string_vars["selected_file"].set(str(self.focused_file["path"]))
                # Add to treeview
                self.selected_files.insert("", "end", values=(len(self.file_list), file["name"]))
                first_iid = self.selected_files.get_children()[0]
                #print(first_iid)
                self.selected_files.focus([first_iid])
                self.selected_files.selection_set([first_iid])
                self.focused_file = self.file_list[0]
                self.parent.call_frames_routine(self.parent.FILEINFO, "update_file_infos", self.focused_file)

        else:
            print(f"Not a vaild PDF file: file ({filenames})")
        
        self.sorted = False
    def method_move_file(self, direction=True):
        focused_index, focused = self.get_focused_file()
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
    def method_remove_selected_ones(self):
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
        
        self.parent.call_frames_routine(self.parent.FILEINFO, "update_file_infos", None)
    def method_remove_all(self):
        for item in self.selected_files.get_children():
            self.selected_files.delete(item)
        self.file_list = []
        self.string_vars["selected_file"].set("")

        self.sorted = False
        self.parent.call_frames_routine(self.parent.FILEINFO, "update_file_infos", None)
    def method_sort(self, event=None):
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
    @property
    def currnet_files(self):
        return self.file_list
class FileInfo(HPLabelFrame):
    #
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid_anchor(N)
        self.grid_propagate(False)

        # This method overlapes inner frame to outer boundary during scrolling
        # See, for solution, https://stackoverflow.com/questions/16188420/tkinter-scrollbar-for-frame
        #self.content_canvas = Canvas(self, width = self.width, height = self.height, bd=0, highlightthickness=0)
        #self.content_scroll_y = Scrollbar(self, orient="vertical", command= self.content_canvas.yview)
        #self.content_canvas.configure(yscrollcommand=self.content_scroll_y.set)
        #self.main_frame = HPFrame(self, width= self.width, height =self.height)
        #self.main_frame.bind(
        #            "<Configure>",
        #            lambda e: self.content_canvas.configure(
        #                scrollregion=self.content_canvas.bbox("all")
        #            )
        #        )
        #self.content_canvas.create_window((0, 0), window=self.main_frame, anchor="nw")
        
        self.main_frame = HPVScrollWapper(self, width= int(self.width), height =int(self.height))
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
        # UI string setting
        self.string_vars["name"] = StringVar(value=self.ui_texts["strings"]["name"])
        self.string_vars["path"] = StringVar(value=self.ui_texts["strings"]["path"])
        self.string_vars["title"] = StringVar(value=self.ui_texts["strings"]["title"])
        self.string_vars["author"] = StringVar(value=self.ui_texts["strings"]["author"])
        self.string_vars["created_date"] = StringVar(value=self.ui_texts["strings"]["created_date"])
        self.string_vars["mod_date"] = StringVar(value=self.ui_texts["strings"]["mod_date"])
        self.string_vars["pages"] = StringVar(value=self.ui_texts["strings"]["pages"])
        self.string_vars["page_size"] = StringVar(value=self.ui_texts["strings"]["page_format"])

        # UI frame
        self.ui_frames ={}
        self.ui_frames["name"] =           HPFrame(self.main_frame.frame, width = self.width)
        self.ui_frames["path"] =           HPFrame(self.main_frame.frame, width = self.width)
        self.ui_frames["title"] =          HPFrame(self.main_frame.frame, width = self.width)
        self.ui_frames["author"] =         HPFrame(self.main_frame.frame, width = self.width)
        self.ui_frames["create_date"] =    HPFrame(self.main_frame.frame, width = self.width)
        self.ui_frames["mod_date"] =       HPFrame(self.main_frame.frame, width = self.width)
        self.ui_frames["pages"] =          HPFrame(self.main_frame.frame, width = self.width)
        self.ui_frames["page_size"] =      HPFrame(self.main_frame.frame, width = self.width)

        self.name_label = Label(self.ui_frames["name"], textvariable=self.string_vars["name"])
        self.path_label = Label(self.ui_frames["path"], textvariable=self.string_vars["path"])
        self.title_label = Label(self.ui_frames["title"], textvariable=self.string_vars["title"])
        self.author_label = Label(self.ui_frames["author"], textvariable=self.string_vars["author"])
        self.create_date_label = Label(self.ui_frames["create_date"], textvariable=self.string_vars["created_date"])
        self.mod_date_label = Label(self.ui_frames["mod_date"], textvariable=self.string_vars["mod_date"])
        self.pages_label = Label(self.ui_frames["pages"], textvariable=self.string_vars["pages"])
        self.page_size_label = Label(self.ui_frames["page_size"], textvariable=self.string_vars["page_size"])

        # Frame 2 print
        self.name_label_var = Label(self.ui_frames["name"], textvariable=self.file_infos["name"])
        self.path_label_var =  Label(self.ui_frames["path"], textvariable=self.file_infos["path"])
        self.title_label_var = Label(self.ui_frames["title"], textvariable=self.file_infos["title"])
        self.author_label_var = Label(self.ui_frames["author"], textvariable=self.file_infos["authors"])
        self.create_date_label_var = Label(self.ui_frames["create_date"], textvariable=self.file_infos["created_date"])
        self.mod_date_label_var = Label(self.ui_frames["mod_date"], textvariable=self.file_infos["mod_date"])
        self.pages_label_var = Label(self.ui_frames["pages"], textvariable=self.file_infos["pages"])

        self.page_size_label_frame = HPFrame(self.ui_frames["page_size"])
        self.page_size_width_label_var = Label(self.page_size_label_frame, textvariable=self.file_infos["page_size"][0])
        self.page_size_product = Label(self.page_size_label_frame, text="x") # Product image
        self.page_size_height_label_var = Label(self.page_size_label_frame, textvariable=self.file_infos["page_size"][1])

        self.set_labels()

        self.ui_frames["name"].grid(           row=0, column=0, sticky=W+N+S, pady=1, ipady= 0.5, padx=2)
        self.ui_frames["path"].grid(           row=1, column=0, sticky=W+N+S, pady=1, ipady= 0.5, padx=2)
        self.ui_frames["title"].grid(          row=2, column=0, sticky=W+N+S, pady=1, ipady= 0.5, padx=2)
        self.ui_frames["author"].grid(         row=3, column=0, sticky=W+N+S, pady=1, ipady= 0.5, padx=2)
        self.ui_frames["create_date"].grid(    row=4, column=0, sticky=W+N+S, pady=1, ipady= 0.5, padx=2)
        self.ui_frames["mod_date"].grid(       row=5, column=0, sticky=W+N+S, pady=1, ipady= 0.5, padx=2)
        self.ui_frames["pages"].grid(          row=6, column=0, sticky=W+N+S, pady=1, ipady= 0.5, padx=2)
        self.ui_frames["page_size"].grid(      row=7, column=0, sticky=W+N+S, pady=1, ipady= 0.5, padx=2)

        #self.content_canvas.grid(row=0, column=0, sticky = W+N+S)
        #self.content_scroll_y.grid(row=0, column =1 , sticky = N+S+E)

        #self.main_frame.configure(borderwidth=2, relief="groove")
        self.main_frame.grid(row=0, column=0, padx=(0,0), sticky= N+S+W+E)

    def set_labels(self):
        info_label_width = 16
        info_wrap_width = int(0.34*self.width)
        label_width = 30
        wrap_width = int(0.5*self.width)

        self.name_label.configure(width = info_label_width, wraplength= info_wrap_width, anchor="center")
        self.path_label.configure(width = info_label_width, wraplength= info_wrap_width, anchor="center")
        self.title_label.configure(width = info_label_width, wraplength= info_wrap_width, anchor="center")
        self.author_label.configure(width = info_label_width, wraplength= info_wrap_width, anchor="center")
        self.create_date_label.configure(width = info_label_width, wraplength= info_wrap_width, anchor="center")
        self.mod_date_label.configure(width = info_label_width, wraplength= info_wrap_width, anchor="center")
        self.pages_label.configure(width = info_label_width, wraplength= info_wrap_width, anchor="center")
        self.page_size_label.configure(width = info_label_width, wraplength= info_wrap_width, anchor="center")

        self.name_label_var.configure(width = label_width, wraplength=wrap_width, anchor="center")
        self.path_label_var.configure(width = label_width, wraplength=wrap_width)
        self.title_label_var.configure(width = label_width, wraplength=wrap_width, anchor="center")
        self.author_label_var.configure(width = label_width, wraplength=wrap_width, anchor="center")
        self.create_date_label_var.configure(width = label_width, wraplength=wrap_width, anchor="center")
        self.mod_date_label_var.configure(width = label_width, wraplength=wrap_width, anchor="center")
        self.pages_label_var.configure(width = label_width, wraplength=wrap_width, anchor="center")
        
        self.page_size_label_frame.configure(width = wrap_width)
        self.page_size_width_label_var.configure(width = int(0.48*label_width), wraplength=int(0.45*wrap_width), anchor="center")
        self.page_size_height_label_var.configure(width = int(0.48*label_width), wraplength=int(0.45*wrap_width), anchor="center")


        self.name_label.grid(row =0, column =0, sticky=W)
        self.name_label_var.grid(row =0, column =1, sticky=W, padx = 5)

        self.path_label.grid(row =0, column =0, sticky=W)
        self.path_label_var.grid(row =0, column =1, sticky=W, padx = 5)

        self.title_label.grid(row =0, column =0, sticky=W)
        self.title_label_var.grid(row =0, column =1, sticky=W, padx = 5)

        self.author_label.grid(row =0, column =0, sticky=W)
        self.author_label_var.grid(row =0, column =1, sticky=W, padx = 5)

        self.create_date_label.grid(row =0, column =0, sticky=W)
        self.create_date_label_var.grid(row =0, column =1, sticky=W, padx = 5)

        self.mod_date_label.grid(row =0, column =0, sticky=W)
        self.mod_date_label_var.grid(row =0, column =1, sticky=W, padx = 5)

        self.pages_label.grid(row =0, column =0, sticky=W)
        self.pages_label_var.grid(row =0, column =1, sticky=W, padx = 5)

        self.page_size_label.grid(row =0, column =0, sticky=W)

        self.page_size_width_label_var.grid(row=0, column=0, sticky = N+S+W+E)
        self.page_size_product.grid(row=0, column=1, sticky= W+E)
        self.page_size_height_label_var.grid(row=0, column=2, sticky = N+S+W+E)

        self.page_size_label_frame.grid(row =0, column =1, sticky = W+E, padx = 5)

    def update_file_infos(self, focused_file):
        if focused_file is not None:
            for key in focused_file.keys():
                if isinstance(self.file_infos[key], StringVar):
                    if key == "path":
                        self.file_infos[key].set(focused_file[key].parents[0])
                    else:
                        self.file_infos[key].set(focused_file[key])
                elif isinstance(self.file_infos[key], tuple):
                    for i in range(0, len(self.file_infos[key])):
                        self.file_infos[key][i].set(focused_file[key][i])
        else:
            for key in self.file_infos:
                if isinstance(self.file_infos[key], StringVar):
                    self.file_infos[key].set("")
                elif isinstance(self.file_infos[key], tuple):
                    self.file_infos[key][i].set(0.0)
        self.main_frame.scroll_region_update()

    
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
        
        # Ui texts
        self.string_vars["merge"] = StringVar(value=self.ui_texts["strings"]["merge"])
        self.string_vars["total_page"] = StringVar(value=self.ui_texts["strings"]["total_page"])
        self.string_vars["name"] = StringVar(value=self.ui_texts["strings"]["name"])
        self.string_vars["as"] = StringVar(value=self.ui_texts["strings"]["as"])
        self.string_vars["split_per"] = StringVar(value=self.ui_texts["strings"]["split_per"])
        # Variables
        self.merge_onoff = BooleanVar(value=False)
        self.name_entry_var  = StringVar(value="")
        self.names = {
            "name": StringVar(value=""),
            "prefix": StringVar(value=""),
            "suffix": StringVar(value="_HPBooklet")
        }
        self.split_per_onoff = BooleanVar(value=False)
        self.split_per_page = IntVar(value = 1)
        self.output_directory_path = StringVar(value="")
        # Functional variables
        self.info_label_width = 13
        self.main_entry_width = 38
        self.total_pages = IntVar(value = 0)
        self.name_type_previous = list(self.names.keys())[0]
        # Frames
        self.layout_frames = {
            "merge" : HPFrame(self, width = self.width),
            "name" : HPFrame(self, width = self.width),
            "split": HPFrame(self, width = self.width),
            "output_directory": HPFrame(self, width = self.width)
        }

        self.merge_label = Label(self.layout_frames["merge"])
        self.merge_label_checkbutton = Checkbutton(self.layout_frames["merge"])
        self.total_pages_label = Label(self.layout_frames["merge"])
        self.total_pages_label_var = Label(self.layout_frames["merge"])
        self.set_merge_frame()

        self.file_name_label = Label(self.layout_frames["name"])
        self.file_name_entry = Entry(self.layout_frames["name"])
        self.file_name_as_label = Label(self.layout_frames["name"])
        self.file_name_types_combo = Combobox(self.layout_frames["name"])
        self.set_file_name_frame()

        self.split_label = Label(self.layout_frames["split"])
        self.split_checkbutton = Checkbutton(self.layout_frames["split"])
        self.split_per_entry = Entry(self.layout_frames["split"])
        self.set_split_frame()

        self.directory_entry = Entry(
            self.layout_frames["output_directory"], 
            textvariable= self.output_directory_path,
            state="disabled")
        self.search_directory = Button(
            self.layout_frames["output_directory"], 
            width=5)
        self.set_output_directory_frame()

        self.validation_setting()

        self.layout_frames["merge"].grid(row= 0, column =0, padx=5, sticky = W+E+N, ipady = 3)
        self.layout_frames["name"].grid(row= 1, column =0, padx=5, sticky = W+E+N, ipady = 3)
        self.layout_frames["split"].grid(row=2, column = 0, padx = 5, sticky=W+E+N, ipady = 3)
        self.layout_frames["output_directory"].grid(row=3, column=0, padx = 5, sticky=S+W+E, ipady = 3, pady = 10)
    def set_merge_frame(self):
        self.merge_label.configure(width = self.info_label_width, textvariable = self.string_vars["merge"], anchor="center")
        self.merge_label_checkbutton.configure(variable = self.merge_onoff, command=self.command_total_page_cal)
        self.total_pages_label.configure(textvariable=self.string_vars["total_page"], anchor="center")
        self.total_pages_label_var.configure(textvariable = self.total_pages)


        self.merge_label.grid(          row = 0, column = 0, padx = (5,5), sticky=W+E)
        self.merge_label_checkbutton.grid( row = 0, column = 1, padx = 5, sticky=W+E)
        self.total_pages_label.grid(    row = 0, column = 2, padx = 5, sticky=W+E)
        self.total_pages_label_var.grid(row = 0, column = 3, padx = 5, sticky=W+E)
        self.layout_frames["merge"].configure(borderwidth=2)
    def set_file_name_frame(self):
        self.file_name_label.configure(width = self.info_label_width, textvariable = self.string_vars["name"], anchor="center")
        self.file_name_entry.configure(textvariable = self.name_entry_var, width = int(0.40*self.main_entry_width))
        self.file_name_as_label.configure(textvariable = self.string_vars["as"], anchor="center")
        self.file_name_types_combo.configure(value=list(self.names.keys()), state="readonly", width = int(0.025*self.width))
        self.file_name_types_combo.current(0)
        self.file_name_types_combo.bind("<<ComboboxSelected>>", self.event_name_types_selected)

        self.file_name_label.grid(      row = 0, column = 0, padx=(5,5))
        self.file_name_entry.grid(      row = 0, column = 1, padx=(2,2))
        self.file_name_as_label.grid(   row = 0, column = 2, padx=(2,2))
        self.file_name_types_combo.grid(row = 0, column = 3, padx=(2,2))
    def set_split_frame(self):
        self.split_label.configure(width = self.info_label_width, textvariable = self.string_vars["split_per"], anchor="center")
        self.split_checkbutton.configure(variable = self.split_per_onoff, command = self.command_split_check)
        self.split_per_entry.configure(
            textvariable = self.split_per_page, 
            state=DISABLED)
        self.split_label.grid(row= 0, column = 0, padx = (5,5), sticky= N+S+W)
        self.split_checkbutton.grid(row= 0, column = 1, sticky= N+S+W)
        self.split_per_entry.grid(row= 0, column = 2, sticky= N+S+W)
    def set_output_directory_frame(self):
        self.directory_entry.configure(
            textvariable= self.output_directory_path,
            width = 37
        )
        self.search_directory.configure(text="...", command = self.method_open_directory, width = 4)

        self.directory_entry.grid(row = 0, column=0, padx=2, sticky = W+N+S)
        self.search_directory.grid(row=0, column=1, padx=2, ipadx = 2)

    def method_open_directory(self):
        pass
    def command_split_check(self):
        if self.split_per_onoff.get():
            self.split_per_entry.configure(state=ACTIVE)
        else:
            self.split_per_entry.configure(state=DISABLED)
    def command_total_page_cal(self):
        file_list = self.parent.get_frames_property(self.parent.MANUSCRIPT, "currnet_files")
        if len(file_list) >= 1 :
            total_pages = 0
            for file in file_list:
                total_pages += file["pages"]
            self.total_pages.set(total_pages)
        else:
            self.total_pages.set(0)
            
        
    def event_name_types_selected(self, event=None):

        i = self.file_name_types_combo.current()
        key = list(self.names.keys())[i]

        string = self.names[key].get()
        current = self.name_entry_var.get()

        self.names[self.name_type_previous].set(current)
        self.name_entry_var.set(string)
        self.name_type_previous = key

    def validation_setting(self):
        positive_integer_validator_command = self.register(Validate.int_positive_value)
        self.split_per_entry.configure(validate="all", validatecommand=(positive_integer_validator_command, "%V", "%P", r"%s", "%S"))
    def update_ui_texts(self, ui_texts):
        super().update_ui_texts(ui_texts)
        super().config(text=self.ui_texts["name"])