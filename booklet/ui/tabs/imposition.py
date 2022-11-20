
from tkinter.colorchooser import askcolor
from tkinter import PhotoImage

from booklet.ui import Validate, HPFrame, HPLabelFrame
from booklet.ui.tabs import *
from booklet.utils.color import rgb2hex

class Imposition(HPFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid_anchor(CENTER)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.sub_frames.append(
            BookBrochures(
                self,
                self.ui_texts["frames"]["bookbrochures"],
                self.resources["bookbrochures"],
                width = int(0.5*self.width),
                height = self.height
            )
        )
        self.sub_frames.append(
            Repetition(
                self,
                self.ui_texts["frames"]["repetition"],
                self.resources["repetition"],
                width = int(0.5*self.width),
                height = self.height
            )
        )

        self.sub_frames[0].grid(row=0, column=0, padx=(10, 10), pady=4, sticky=N+S+E+W)
        self.sub_frames[1].grid(row=0, column=1, padx=(10, 10), pady=4, sticky=N+S+E+W)
    
class BookBrochures(HPLabelFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.grid_anchor(CENTER)

        # variabels
        self.onoff_bool = BooleanVar(value = False)
        self.layout_x_int = IntVar(value= 1)
        self.layout_y_int = IntVar(value= 1)
        self.collection_mark_bool = BooleanVar(value = False)
        self.collection_mark_color = rgb2hex(0, 0, 0)
        self.gap_bool = BooleanVar(value = False)
        self.gap_v_double = DoubleVar(value = 0.)
        self.gap_h_double = DoubleVar(value = 0.)

        self.fold_line_bool = BooleanVar(value = False)
        self.fold_gap_bool = BooleanVar(value = False)
        self.paper_thick_bool = BooleanVar(value = False)
        self.paper_thick_double = DoubleVar(value = 0.)

        # functional variable
        self.info_labels_width = 15
        self.main_entry_width = 30


        # UI string setting
        self.string_vars["onoff"] = StringVar(value = self.ui_texts["strings"]["onoff"])
        self.string_vars["layout"] = StringVar(value = self.ui_texts["strings"]["layout"])
        self.string_vars["collection_mark"] = StringVar(value = self.ui_texts["strings"]["collection_mark"])
        self.string_vars["gap"] = StringVar(value = self.ui_texts["strings"]["gap"])
        self.string_vars["fold_line"] = StringVar(value = self.ui_texts["strings"]["fold_line"])
        self.string_vars["fold_gap"] = StringVar(value = self.ui_texts["strings"]["fold_gap"])
        self.string_vars["paper_thickness"] = StringVar(value = self.ui_texts["strings"]["paper_thickness"])
        # UI frames
        self.ui_frames["onoff"] = HPFrame(self, width = self.width)
        self.ui_frames["layout"] = HPFrame(self, width = self.width)
        self.ui_frames["collection_mark"] = HPFrame(self, width = self.width)
        self.ui_frames["gap"] = HPFrame(self, width = self.width)
        self.ui_frames["fold_gap"] = HPFrame(self, width = self.width)
        self.ui_frames["fold_line"] = HPFrame(self, width = self.width)
        self.ui_frames["paper_thickness"] = HPFrame(self, width = self.width)

        # info labels
        self.info_labels = {}
        self.info_labels["onoff"] = Label(self.ui_frames["onoff"])
        self.info_labels["layout"] = Label(self.ui_frames["layout"])
        self.info_labels["collection_mark"] = Label(self.ui_frames["collection_mark"])
        self.info_labels["gap"] = Label(self.ui_frames["gap"])
        self.info_labels["fold_gap"] = Label(self.ui_frames["fold_gap"])
        self.info_labels["fold_line"] = Label(self.ui_frames["fold_line"])
        self.info_labels["paper_thickness"] = Label(self.ui_frames["paper_thickness"])
        self.set_info_labels()

        # inputs

        self.onoff_checkbutton  = Checkbutton(self.ui_frames["onoff"])
        self.layout_x_entry = Entry(self.ui_frames["layout"])
        self.layout_times_label = Label(self.ui_frames["layout"], text="x")
        self.layout_y_entry = Entry(self.ui_frames["layout"])

        self.collection_mark_checkbutton = Checkbutton(self.ui_frames["collection_mark"])
        self.collection_mark_button = tk_Button(self.ui_frames["collection_mark"])

        self.gap_checkbutton  = Checkbutton(self.ui_frames["gap"])
        self.gap_v_entry = Entry(self.ui_frames["gap"])
        self.gap_comma_label = Label(self.ui_frames["gap"], text=", ")
        self.gap_h_entry = Entry(self.ui_frames["gap"])

        self.fold_gap_line_checkbutton = Checkbutton(self.ui_frames["fold_line"])
        self.fold_gap_checkbutton = Checkbutton(self.ui_frames["fold_gap"])
        self.paper_thick_checkbutton = Checkbutton(self.ui_frames["paper_thickness"])
        self.paper_thick_entry = Entry(self.ui_frames["paper_thickness"])
        
        self.set_inputs()

        self.validation_setting()

        self.event_setting()

        self.ui_frames["onoff"].grid(           row=0, column =0, padx = (4,4 ), pady=(6,2), sticky=N+W+S)
        self.ui_frames["layout"].grid(          row=1, column =0, padx = (4,4 ), pady=(2,2), sticky=N+W+S)
        self.ui_frames["collection_mark"].grid( row=2, column =0, padx = (4,4 ), pady=(2,2), sticky=N+W+S)
        self.ui_frames["gap"].grid(             row=3, column =0, padx = (4,4 ), pady=(2,2), sticky=N+W+S)
        self.ui_frames["fold_gap"].grid(        row=4, column =0, padx = (4,4 ), pady=(2,2), sticky=N+W+S)
        self.ui_frames["fold_line"].grid(       row=5, column =0, padx = (4,4 ), pady=(2,2), sticky=N+W+S)
        self.ui_frames["paper_thickness"].grid( row=6, column =0, padx = (4,4 ), pady=(2,2), sticky=N+W+S)
    
    def set_info_labels(self):
        self.info_labels["onoff"].configure(textvariable = self.string_vars["onoff"], anchor=CENTER, width =self.info_labels_width)
        self.info_labels["layout"].configure(textvariable = self.string_vars["layout"], anchor=CENTER, width =self.info_labels_width)
        self.info_labels["collection_mark"].configure(textvariable = self.string_vars["collection_mark"], anchor=CENTER, width =self.info_labels_width)
        self.info_labels["gap"].configure(textvariable = self.string_vars["gap"], anchor=CENTER, width =self.info_labels_width)
        self.info_labels["fold_gap"].configure(textvariable = self.string_vars["fold_gap"], anchor=CENTER, width =self.info_labels_width)
        self.info_labels["fold_line"].configure(textvariable = self.string_vars["fold_line"], anchor=CENTER, width =self.info_labels_width)
        self.info_labels["paper_thickness"].configure(textvariable = self.string_vars["paper_thickness"], anchor=CENTER, width =self.info_labels_width)

        self.info_labels["onoff"].grid( row=0, column = 0)
        self.info_labels["layout"].grid( row=0, column = 0)
        self.info_labels["collection_mark"].grid( row=0, column = 0)
        self.info_labels["gap"].grid( row=0, column = 0)
        self.info_labels["fold_gap"].grid( row=0, column = 0)
        self.info_labels["fold_line"].grid( row=0, column = 0)
        self.info_labels["paper_thickness"].grid( row=0, column = 0)
    
    def set_inputs(self):
        self.onoff_checkbutton.configure(variable = self.onoff_bool)
        self.layout_y_entry.configure(textvariable=self.layout_y_int, width = int(0.36*self.main_entry_width), state = "readonly")
        self.layout_x_entry.configure(textvariable=self.layout_x_int, width = int(0.36*self.main_entry_width), state = "readonly")

        self.collection_mark_checkbutton.configure(variable = self.collection_mark_bool)
        self.pixel_button = PhotoImage(width=1, height=1)
        self.collection_mark_button.configure(bg="black", image= self.pixel_button, width = 15, height =15, compound="c")

        self.gap_checkbutton.configure(variable = self.gap_bool)
        self.gap_v_entry.configure(textvariable=self.gap_v_double, width =int(0.36*self.main_entry_width))
        self.gap_h_entry.configure(textvariable=self.gap_h_double, width =int(0.36*self.main_entry_width))

        self.fold_gap_line_checkbutton.configure(variable = self.fold_gap_bool)
        self.fold_gap_checkbutton.configure(variable = self.fold_line_bool)
        self.paper_thick_checkbutton.configure(variable = self.paper_thick_bool)
        self.paper_thick_entry.configure(textvariable = self.paper_thick_double, width = int(0.7*self.main_entry_width))

        self.onoff_checkbutton.grid( row= 0, column =1, padx=(int(0.35*self.width),))

        self.layout_x_entry.grid( row= 0, column =1, padx = (2,2))
        self.layout_times_label.grid( row= 0, column =2, padx = (2,2))
        self.layout_y_entry.grid( row= 0, column =3, padx = (2,2))

        self.collection_mark_checkbutton.grid( row= 0, column =1)
        self.collection_mark_button.grid( row= 0, column =2)

        self.gap_checkbutton.grid( row= 0, column =1)
        self.gap_v_entry.grid( row= 0, column =2)
        self.gap_comma_label.grid( row =0, column =3)
        self.gap_h_entry.grid( row= 0, column =4)

        self.fold_gap_line_checkbutton.grid( row= 0, column =1)
        self.fold_gap_checkbutton.grid( row= 0, column =1)
        self.paper_thick_checkbutton.grid( row= 0, column =1)
        self.paper_thick_entry.grid(row=0, column=2)
    
    def validation_setting(self):
        positive_integer_validation = self.register(Validate.int_positive_value )
        positive_double_validation = self.register(Validate.double_positive_value)

        # integer
        self.layout_x_entry.configure(validate="all", validatecommand= (positive_integer_validation, "%V", "%P", r"%s", "%S"))
        self.layout_y_entry.configure(validate="all", validatecommand= (positive_integer_validation, "%V", "%P", r"%s", "%S"))

        # double
        self.gap_v_entry.configure( validate="all", validatecommand= (positive_double_validation,"%V", "%P", r"%s", "%S"))
        self.gap_h_entry.configure( validate="all", validatecommand= (positive_double_validation,"%V", "%P", r"%s", "%S"))
        self.paper_thick_entry.configure( validate="all", validatecommand= (positive_double_validation,"%V", "%P", r"%s", "%S"))

    def event_setting(self):
        self.collection_mark_button.configure(command= self.ask_color_collection_mark)
    
    def ask_color_collection_mark(self):
        color = askcolor()
        if color is not None:
            colorhex = color[1]
            if colorhex is None:
                pass
            self.collection_mark_color = colorhex
            self.collection_mark_button.configure(bg = colorhex)
class Repetition(HPLabelFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.grid_anchor(CENTER)

        # Variables

        self.onoff_bool = BooleanVar(value = False)
        self.layout_x = IntVar(value = 1)
        self.layout_y = IntVar(value = 1)
        self.gap_bool = BooleanVar(value = False)
        self.gap_double = DoubleVar(value = 0.)
        self.gap_line_bool =  BooleanVar(value = False)
        self.gap_line_thick_double = DoubleVar(value = 0.)
        self.paper_format_bool =  BooleanVar(value = False)
        self.paper_format_x = DoubleVar(value= 0.)
        self.paper_format_y = DoubleVar(value= 0.)
        self.page_format_bool =  BooleanVar(value = False)
        self.page_format_x = DoubleVar(value= 0.)
        self.page_format_y = DoubleVar(value= 0.)
        self.max_fill_bool =  BooleanVar(value = False)
        # Functional variable
        self.info_labels_width = 15
        self.main_entry_width = 30

        # UI string setting
        self.string_vars["onoff"] = StringVar(value = self.ui_texts["strings"]["onoff"])
        self.string_vars["layout"] = StringVar(value = self.ui_texts["strings"]["layout"])
        self.string_vars["fit"] = StringVar(value = self.ui_texts["strings"]["fit"])
        self.string_vars["gap"] = StringVar(value = self.ui_texts["strings"]["gap"])
        self.string_vars["gap_line"] = StringVar(value = self.ui_texts["strings"]["gap_line"])
        self.string_vars["paper_format"] = StringVar(value = self.ui_texts["strings"]["paper_format"])
        self.string_vars["page_format"] = StringVar(value = self.ui_texts["strings"]["page_format"])
        self.string_vars["max_fill"] = StringVar(value = self.ui_texts["strings"]["max_fill"])
        # UI frames
        self.ui_frames["onoff"] = HPFrame(self, width = self.width, grid_anchor = CENTER)
        self.ui_frames["layout"] = HPFrame(self, width = self.width, grid_anchor = CENTER)
        self.ui_frames["fit"] = HPFrame(self, width = self.width, grid_anchor = CENTER)
        self.ui_frames["gap"] = HPFrame(self, width = self.width, grid_anchor = CENTER)
        self.ui_frames["gap_line"] = HPFrame(self, width = self.width, grid_anchor = CENTER)
        self.ui_frames["paper_format"] = HPFrame(self, width = self.width, grid_anchor = CENTER)
        self.ui_frames["page_format"] = HPFrame(self, width = self.width, grid_anchor = CENTER)
        self.ui_frames["max_fill"] = HPFrame(self, width = self.width, grid_anchor = CENTER)
        

        # info_labels
        self.info_labels = {}
        self.info_labels["onoff"] = Label(self.ui_frames["onoff"])
        self.info_labels["layout"] = Label(self.ui_frames["layout"])
        self.info_labels["fit"] = Label(self.ui_frames["fit"])
        self.info_labels["gap"] = Label(self.ui_frames["gap"])
        self.info_labels["gap_line"] = Label(self.ui_frames["gap_line"])
        self.info_labels["paper_format"] = Label(self.ui_frames["paper_format"])
        self.info_labels["page_format"] = Label(self.ui_frames["page_format"])
        self.info_labels["max_fill"] = Label(self.ui_frames["max_fill"])
        self.set_info_labels()
        # inputs
        self.onoff_checkbutton = Checkbutton(self.ui_frames["onoff"])
        
        self.layout_x_entry = Entry(self.ui_frames["layout"])
        self.layout_times_label = Label(self.ui_frames["layout"], text="x")
        self.layout_y_entry = Entry(self.ui_frames["layout"])

        self.fit_mode_combobox = Combobox(self.ui_frames["fit"])

        self.gap_checkbutton = Checkbutton(self.ui_frames["gap"])
        self.gap_thick_entry = Entry(self.ui_frames["gap"])

        self.gap_line_checkbutton = Checkbutton(self.ui_frames["gap_line"])
        self.gap_line_location_combobox = Combobox(self.ui_frames["gap_line"])
        self.gap_line_color_button = tk_Button(self.ui_frames["gap_line"])
        self.gap_line_type_combobox = Combobox(self.ui_frames["gap_line"])
        self.gap_line_thick_entry = Entry(self.ui_frames["gap_line"])
        self.gap_line_thick_label = Label(self.ui_frames["gap_line"], text="(pts)")

        self.paper_format_checkbutton = Checkbutton(self.ui_frames["paper_format"])
        self.paper_format_x_entry = Entry(self.ui_frames["paper_format"])
        self.paper_format_times_label = Label(self.ui_frames["paper_format"], text= "x")
        self.paper_format_y_entry = Entry(self.ui_frames["paper_format"])

        self.page_format_checkbutton = Checkbutton(self.ui_frames["page_format"])
        self.page_format_x_entry = Entry(self.ui_frames["page_format"])
        self.page_format_times_label = Label(self.ui_frames["page_format"], text= "x")
        self.page_format_y_entry = Entry(self.ui_frames["page_format"])

        self.max_fill_checkbutton = Checkbutton(self.ui_frames["max_fill"])
        
        self.set_inputs()

        self.validation_setting()

        self.event_setting()

        self.ui_frames["onoff"].grid(       row =0 , column =0, padx=(2,2), pady=(6,3), sticky=N+S+W)
        self.ui_frames["layout"].grid(      row =1 , column =0, padx=(2,2), pady=(3,3), sticky=N+S+W)
        self.ui_frames["fit"].grid(         row =2 , column =0, padx=(2,2), pady=(3,3), sticky=N+S+W)
        self.ui_frames["gap"].grid(         row =3 , column =0, padx=(2,2), pady=(3,3), sticky=N+S+W)
        self.ui_frames["gap_line"].grid(    row =4 , column =0, padx=(2,2), pady=(3,3), sticky=N+S+W)
        self.ui_frames["paper_format"].grid(row =5 , column =0, padx=(2,2), pady=(3,3), sticky=N+S+W)
        self.ui_frames["page_format"].grid( row =6 , column =0, padx=(2,2), pady=(3,3), sticky=N+S+W)
        self.ui_frames["max_fill"].grid(    row =7 , column =0, padx=(2,2), pady=(3,3), sticky=N+S+W)

    def set_info_labels(self):
        self.info_labels["onoff"].configure(textvariable = self.string_vars["onoff"], anchor = CENTER, width = self.info_labels_width)
        self.info_labels["layout"].configure(textvariable = self.string_vars["layout"], anchor = CENTER, width = self.info_labels_width)
        self.info_labels["fit"].configure(textvariable = self.string_vars["fit"], anchor = CENTER, width = self.info_labels_width)
        self.info_labels["gap"].configure(textvariable = self.string_vars["gap"], anchor = CENTER, width = self.info_labels_width)
        self.info_labels["gap_line"].configure(textvariable = self.string_vars["gap_line"], anchor = CENTER, width = self.info_labels_width)
        self.info_labels["paper_format"].configure(textvariable = self.string_vars["paper_format"], anchor = CENTER, width = self.info_labels_width)
        self.info_labels["page_format"].configure(textvariable = self.string_vars["page_format"], anchor = CENTER, width = self.info_labels_width)
        self.info_labels["max_fill"].configure(textvariable = self.string_vars["max_fill"], anchor = CENTER, width = self.info_labels_width)

        self.info_labels["onoff"].grid(         row= 0, column = 0 , sticky= N+S+W)
        self.info_labels["layout"].grid(        row= 0, column = 0 , sticky= N+S+W)
        self.info_labels["fit"].grid(           row= 0, column = 0 , sticky= N+S+W)
        self.info_labels["gap"].grid(           row= 0, column = 0 , sticky= N+S+W)
        self.info_labels["gap_line"].grid(      row= 0, column = 0 , rowspan= 2, sticky= N+S+W)
        self.info_labels["paper_format"].grid(  row= 0, column = 0 , sticky= N+S+W)
        self.info_labels["page_format"].grid(   row= 0, column = 0 , sticky= N+S+W)
        self.info_labels["max_fill"].grid(      row= 0, column = 0 , sticky= N+S+W)
    def set_inputs(self):
        
        self.onoff_checkbutton.configure(variable = self.onoff_bool)
        self.onoff_checkbutton.grid(row=0, column= 1, padx=(int(0.25*self.width), 0 ), sticky=N+S+W+E)
        
        self.layout_x_entry.configure(textvariable=self.layout_x, width = int(0.37*self.main_entry_width))
        self.layout_y_entry.configure(textvariable=self.layout_y, width = int(0.37*self.main_entry_width))
        self.layout_x_entry.grid(row=0, column= 1, sticky=N+S+W+E)
        self.layout_times_label.grid(row=0, column= 2, sticky=N+S+W+E)
        self.layout_y_entry.grid(row=0, column= 3, sticky=N+S+W+E)

        self.fit_mode_combobox.configure(
            values= list(self.ui_texts["variables"]["fit"].values()), 
            state = "readonly", width = int(1.*self.main_entry_width))
        self.fit_mode_combobox.current(0)
        self.fit_mode_combobox.grid(row=0, column= 1, sticky=N+S+W+E)

        self.gap_checkbutton.configure(variable = self.gap_bool)
        self.gap_thick_entry.configure(textvariable=self.gap_double, width = int(0.8*self.main_entry_width))
        self.gap_checkbutton.grid(row=0, column= 1, sticky=N+S+W+E)
        self.gap_thick_entry.grid(row=0, column= 2, sticky=N+S+W+E)

        self.gap_line_checkbutton.configure(variable = self.gap_line_bool)
        self.gap_line_location_combobox.configure(
            values = list(self.ui_texts["variables"]["gap_position"].values()), 
            width = int(0.4 * self.main_entry_width), 
            state = "readonly")
        self.gap_line_location_combobox.current(0)
        self.pixel_button = PhotoImage(width=1, height=1)
        self.gap_line_color_button.configure(bg='blue', image= self.pixel_button, width = 15, height =15, compound="c")
        self.gap_line_type_combobox.configure(
            values = list(self.ui_texts["variables"]["gap_type"].values()), width = int(0.4 * self.main_entry_width), state = "readonly")
        self.gap_line_type_combobox.current(0)
        self.gap_line_thick_entry.configure(textvariable=self.gap_line_thick_double, width = int(0.2*self.main_entry_width))

        self.gap_line_checkbutton.grid( row =0, column = 1, padx = (0,2))
        self.gap_line_location_combobox.grid( row =0, column = 2, padx = (2,2))
        self.gap_line_color_button.grid(    row =1, column = 1, padx = (2,2), pady=2)
        self.gap_line_type_combobox.grid(   row =1, column = 2, padx = (2,2), pady=2)
        self.gap_line_thick_entry.grid(     row =1, column = 3, padx = (2,2), pady=2)
        self.gap_line_thick_label.grid(     row =1, column = 4, padx = (2,2), pady=2)

        self.paper_format_checkbutton.configure(variable=self.paper_format_bool)
        self.paper_format_x_entry.configure(textvariable=self.paper_format_x, width = int(0.35*self.main_entry_width))
        self.paper_format_y_entry.configure(textvariable=self.paper_format_y, width = int(0.35*self.main_entry_width))

        self.paper_format_checkbutton.grid( row= 0, column=1)
        self.paper_format_x_entry.grid( row= 0, column=2)
        self.paper_format_times_label.grid( row= 0, column=3)
        self.paper_format_y_entry.grid( row= 0, column=4)

        self.page_format_checkbutton.configure(variable = self.page_format_bool)
        self.page_format_x_entry.configure(textvariable=self.page_format_x, width = int(0.35*self.main_entry_width))
        self.page_format_y_entry.configure(textvariable=self.page_format_y, width = int(0.35*self.main_entry_width))

        self.page_format_checkbutton.grid( row= 0, column =1)
        self.page_format_x_entry.grid( row= 0, column =2)
        self.page_format_times_label.grid( row= 0, column =3)
        self.page_format_y_entry.grid( row= 0, column =4)

        self.max_fill_checkbutton.configure(variable = self.max_fill_bool)
        self.max_fill_checkbutton.grid(row=0, column =1, padx=(int(0.25*self.width), 0 ))

    def validation_setting(self):
        positive_integer_validation = self.register(Validate.int_positive_value)
        positive_double_validation = self.register(Validate.double_positive_value)

        self.layout_x_entry.configure(validate="all", validatecommand= (positive_integer_validation, "%V", "%P", r"%s", "%S"))
        self.layout_y_entry.configure(validate="all", validatecommand= (positive_integer_validation, "%V", "%P", r"%s", "%S"))
        self.paper_format_x_entry.configure(validate="all", validatecommand= (positive_double_validation, "%V", "%P", r"%s", "%S"))
        self.paper_format_y_entry.configure(validate="all", validatecommand= (positive_double_validation, "%V", "%P", r"%s", "%S"))
        self.page_format_x_entry.configure(validate="all", validatecommand= (positive_double_validation, "%V", "%P", r"%s", "%S"))
        self.page_format_y_entry.configure(validate="all", validatecommand= (positive_double_validation, "%V", "%P", r"%s", "%S"))
    def event_setting(self):
        self.gap_line_color_button.configure(command = self.ask_color_gap_line)

    def ask_color_gap_line(self):
        color = askcolor()
        if color is not None:
            colorhex = color[1]
            if colorhex is None:
                pass
            self.gap_line_color = colorhex
            self.gap_line_color_button.configure(bg = colorhex)


