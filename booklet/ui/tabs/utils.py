from booklet.ui.tabs import *
from booklet.ui import Validate, HPFrame, HPLabelFrame


class Utils(HPFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.side_frame = HPFrame(self, width = int(0.48*self.width))

        self.sub_frames.append(
            ToImage(
                self.side_frame,
                self.ui_texts["frames"]["toimage"],
                self.resources["toimage"],
                width = int(0.48*self.width),
                height = int(0.48*self.height)
            )
        )
        self.sub_frames.append(
            Duplex(
                self.side_frame,
                self.ui_texts["frames"]["duplex"],
                self.resources["duplex"],
                width = int(0.48*self.width),
                height = int(0.48*self.height)
            )
        )
        self.sub_frames.append(
            Note(
                self,
                self.ui_texts["frames"]["note"],
                self.resources["note"],
                width = int(0.48*self.width),
                height = self.height
            )
        )

        self.sub_frames[0].grid(row=0, column=0, pady = 4, padx = (10,10), sticky= N+W+S+E)
        self.sub_frames[1].grid(row=1, column=0, pady = 4, padx = (10,10), sticky= N+W+S+E)
        self.side_frame.grid(row=0, column =0, pady = 4, padx = (10,10), sticky=  N+S+W+E)
        self.sub_frames[2].grid(row=0, column=1, pady = 4, padx = (10,10), sticky=N+S+W+E)
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

class ToImage(HPLabelFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.main_frame = HPFrame(self, width= self.width, height=self.height)
        self.main_frame.grid_anchor(CENTER)
        # Variables
        self.toimage_onoff = BooleanVar(value = False)
        # Functional variables
        self.info_label_width = 15

        # Ui string
        self.string_vars["onoff"] = StringVar(value=self.ui_texts["strings"]["onoff"])

        self.ui_frames["image"] = HPFrame(self.main_frame, width= self.width)

        self.toimage_onoff_label = Label(self.ui_frames["image"])
        self.toimage_onoff_checkbutton = Checkbutton(self.ui_frames["image"])
        self.set_label()
        self.set_inputs()
        self.ui_frames["image"].grid(row=0, column=0, padx= 4, pady = 4, sticky=N+S+W)
        self.main_frame.grid(row=0, column= 0, sticky=N+S+W)
    def set_label(self):
        self.toimage_onoff_label.configure(textvariable=self.string_vars["onoff"], width=self.info_label_width, anchor = CENTER)

        self.toimage_onoff_label.grid(row=0, column=0,  sticky=N+S+W)
    def set_inputs(self):
        self.toimage_onoff_checkbutton.configure(variable=self.toimage_onoff)
        self.toimage_onoff_checkbutton.grid(row=0, column=1, padx = int(0.35* self.width), sticky=N+S+W)

class Duplex(HPLabelFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid_anchor(CENTER)

        self.main_frame = HPFrame(self, width = self.width, height = self.height)
        self.main_frame.grid_anchor(CENTER)
        # Variables
        self.duplex_onoff = BooleanVar(value = False)
        self.translation_x = DoubleVar(value=0.)
        self.translation_y = DoubleVar(value=0.)
        self.rotation = DoubleVar(value = 0.)
        self.preserve_dimension = BooleanVar(value = False)

        # Functional Variables
        self.info_label_width = 15
        self.main_entry_width = 30
        self.translation_onoff = BooleanVar(value = False)
        self.rotation_onoff = BooleanVar(value = False)

        # Ui strings
        self.string_vars["onoff"] = StringVar(value=self.ui_texts["strings"]["onoff"])
        self.string_vars["translation"] = StringVar(value=self.ui_texts["strings"]["translation"])
        self.string_vars["rotation"] = StringVar(value=self.ui_texts["strings"]["rotation"])
        self.string_vars["preserve"] = StringVar(value=self.ui_texts["strings"]["preserve"])

        # Ui frames

        self.ui_frames["onoff"] = HPFrame(self.main_frame, width = self.width)
        self.ui_frames["translation"] = HPFrame(self.main_frame, width = self.width)
        self.ui_frames["rotation"] = HPFrame(self.main_frame, width = self.width)
        self.ui_frames["preserve"] = HPFrame(self.main_frame, width = self.width)

        self.info_labels = {}
        self.info_labels["onoff"]  = Label(self.ui_frames["onoff"])
        self.info_labels["translation"] = Label(self.ui_frames["translation"])
        self.info_labels["rotation"] = Label(self.ui_frames["rotation"])
        self.info_labels["preserve"] = Label(self.ui_frames["preserve"])
        self.set_info_labels()
        
        # input elements
        self.onoff_checkbutton = Checkbutton(self.ui_frames["onoff"])
        self.translation_checkbutton = Checkbutton(self.ui_frames["translation"])
        self.translation_x_entry = Entry(self.ui_frames["translation"])
        self.translation_comma_label = Label(self.ui_frames["translation"], text=", ")
        self.translation_y_entry = Entry(self.ui_frames["translation"])
        self.rotation_checkbutton = Checkbutton(self.ui_frames["rotation"])
        self.rotation_entry = Entry(self.ui_frames["rotation"])
        self.preserve_checkbutton = Checkbutton(self.ui_frames["preserve"])
        self.set_inputs()
        
        self.validation_setting()

        # Grid
        self.ui_frames["onoff"].grid(       row= 0, column =0, pady = 4, sticky= W+N+S)
        self.ui_frames["translation"].grid( row= 1, column =0, pady = 4, sticky= W+N+S)
        self.ui_frames["rotation"].grid(    row= 2, column =0, pady = 4, sticky= W+N+S)
        self.ui_frames["preserve"].grid(    row= 3, column =0, pady = 4, sticky= W+N+S)

        #self.ui_frames["onoff"].configure(borderwidth=2, relief="groove")
        #self.main_frame.configure(borderwidth=2, relief="groove")
        self.main_frame.grid(row=0 , column=0, pady=(4,4), sticky= N+S+W)

    def set_info_labels(self):

        self.info_labels["onoff"].configure(textvariable = self.string_vars["onoff"], width = self.info_label_width, anchor = CENTER)
        self.info_labels["translation"].configure(textvariable = self.string_vars["translation"], width = self.info_label_width, anchor = CENTER)
        self.info_labels["rotation"].configure(textvariable = self.string_vars["rotation"], width = self.info_label_width, anchor = CENTER)
        self.info_labels["preserve"].configure(textvariable = self.string_vars["preserve"], width = self.info_label_width, anchor = CENTER)

        self.info_labels["onoff"].grid( row= 0, column = 0 , sticky = W+N+S)
        self.info_labels["translation"].grid( row= 0, column = 0 , sticky = W+N+S)
        self.info_labels["rotation"].grid( row= 0, column = 0 , sticky = W+N+S)
        self.info_labels["preserve"].grid( row= 0, column = 0 , sticky = W+N+S)
    def set_inputs(self):
        self.onoff_checkbutton.configure(variable= self.duplex_onoff)
        self.translation_checkbutton.configure(variable = self.translation_onoff)
        self.translation_x_entry.configure(textvariable= self.translation_x, width = int(0.45*self.main_entry_width))
        self.translation_y_entry.configure(textvariable= self.translation_y, width = int(0.45*self.main_entry_width))
        self.rotation_checkbutton.configure(variable= self.rotation_onoff)
        self.rotation_entry.configure(textvariable= self.rotation,  width = int(0.45*self.main_entry_width))
        self.preserve_checkbutton.configure(variable=self.preserve_dimension)

        self.onoff_checkbutton.grid(row=0, column=1, padx = int(0.32*self.width))

        self.translation_checkbutton.grid(row=0, column=1)
        self.translation_x_entry.grid(row=0, column=2)
        self.translation_comma_label.grid(row=0, column =3)
        self.translation_y_entry.grid(row=0, column=4)

        self.rotation_checkbutton.grid(row=0, column=1)
        self.rotation_entry.grid(row=0, column=2)

        self.preserve_checkbutton.grid(row=0, column=1, padx = int(0.32*self.width))
    def validation_setting(self):
        double_validator = self.register(Validate.double_value)

        self.translation_x_entry.configure(validate="all", validatecommand=(double_validator, "%V", "%P", r"%s", "%S"))
        self.translation_y_entry.configure(validate="all", validatecommand=(double_validator, "%V", "%P", r"%s", "%S"))
        self.rotation_entry.configure(validate="all", validatecommand=(double_validator, "%V", "%P", r"%s", "%S"))

class Note(HPLabelFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.sub_frames.append(
            Numbering(
                self,
                self.ui_texts["frames"]["numbering"],
                self.resources["numbering"],
                width = self.width,
                height = self.height
            )
        )
        # Variables
        self.note_onoff = BooleanVar(value = False)
        
        # Functional variables
        self.info_label_width = 15
        self.main_entry_width = 30

        # Ui strings
        self.string_vars["onoff"] = StringVar(value = self.ui_texts["strings"]["onoff"])
        self.string_vars["pages"] = StringVar(value = self.ui_texts["strings"]["pages"])

        # Ui frames
        self.ui_frames["onoff"] = HPFrame(self, width =self.width)
        self.ui_frames["pages"] = HPFrame(self, width = self.width)

        # Ui lables
        self.info_labels = {}
        self.info_labels["onoff"] = Label(self.ui_frames["onoff"])
        self.info_labels["pages"] = Label(self.ui_frames["pages"])
        self.set_labels()
        # input elements
        self.onoff_checkbutton = Checkbutton(self.ui_frames["onoff"])
        self.pages_entry = Entry(self.ui_frames["pages"])
        self.set_inputs()

        self.validation_setting()
        
        # Griding
        self.ui_frames["onoff"].grid(row=0, column=0, padx=(2,2), pady=2, sticky= N+W+S)
        self.ui_frames["pages"].grid(row=1, column=0, padx=(2,2), pady=2, sticky= N+W+S)
        self.sub_frames[0].grid(row=2, column=0, padx=(4,4), pady=(2, 10), sticky= N+W+S+E)
    
    def set_labels(self):
        self.info_labels["onoff"]
        self.info_labels["pages"]

        self.info_labels["onoff"].configure(textvariable = self.string_vars["onoff"], width = self.info_label_width, anchor = CENTER)
        self.info_labels["pages"].configure(textvariable = self.string_vars["pages"], width = self.info_label_width, anchor = CENTER)

        self.info_labels["onoff"].grid(row=0, column=0)
        self.info_labels["pages"].grid(row=0, column=0)
    def set_inputs(self):
        self.onoff_checkbutton.configure(variable=self.note_onoff)
        self.pages_entry.configure(width = self.main_entry_width)

        self.onoff_checkbutton.grid(row= 0 , column = 1, padx = (int(0.28*self.width),0))
        self.pages_entry.grid(row= 0 , column = 1, padx = (2,4))
    
    def validation_setting(self):
        int_positive_validator = self.register(Validate.int_positive_value)
        self.pages_entry.configure(validate="all", validatecommand=(int_positive_validator, "%V", "%P", r"%s", "%S"))
class Numbering(HPLabelFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.main_frame = HPFrame(self, width = self.width)

        # Variables
        self.numbering_onoff = BooleanVar(value = False)

        # Functional variables
        self.info_label_width = 13
        self.main_entry_width = 35

        # Ui strings
        self.string_vars["onoff"] = StringVar(value=self.ui_texts["strings"]["onoff"])
        self.string_vars["count"] = StringVar(value=self.ui_texts["strings"]["count"])
        self.string_vars["mark_on"] = StringVar(value=self.ui_texts["strings"]["mark_on"])
        self.string_vars["location"] = StringVar(value=self.ui_texts["strings"]["location"])
        self.string_vars["align"] = StringVar(value=self.ui_texts["strings"]["align"])
        self.string_vars["font"] = StringVar(value=self.ui_texts["strings"]["font"])
        self.string_vars["size"] = StringVar(value=self.ui_texts["strings"]["size"])
        # Ui frames
        self.ui_frames["onoff"] = HPFrame(self.main_frame, width = self.width)
        self.ui_frames["count"] = HPFrame(self.main_frame, width = self.width)
        self.ui_frames["mark_on"] = HPFrame(self.main_frame, width = self.width)
        self.ui_frames["location"] = HPFrame(self.main_frame, width = self.width)
        self.ui_frames["align"] = HPFrame(self.main_frame, width = self.width)
        self.ui_frames["font"] = HPFrame(self.main_frame, width = self.width)
        self.ui_frames["size"] = HPFrame(self.main_frame, width = self.width)

        # info labels
        self.info_labels = {}
        self.info_labels["onoff"] = Label(self.ui_frames["onoff"])
        self.info_labels["count"] = Label(self.ui_frames["count"])
        self.info_labels["mark_on"] = Label(self.ui_frames["mark_on"])
        self.info_labels["location"] = Label(self.ui_frames["location"])
        self.info_labels["align"] = Label(self.ui_frames["align"])
        self.info_labels["font"] = Label(self.ui_frames["font"])
        self.info_labels["size"] = Label(self.ui_frames["size"])

        self.set_labels()
        
        # inputs
        self.onoff_checkbutton = Checkbutton(self.ui_frames["onoff"])
        self.counts_combobox = Combobox(self.ui_frames["count"])
        self.marks_on_combobox = Combobox(self.ui_frames["mark_on"])
        self.location_combobox = Combobox(self.ui_frames["location"])
        self.align_combobox = Combobox(self.ui_frames["align"])
        self.font_combobox = Combobox(self.ui_frames["font"])
        self.font_size_combobox = Combobox(self.ui_frames["size"])
        self.set_inputs()
        
        # Griding        
        self.ui_frames["onoff"].grid( row=0, column = 0, pady=(1,1), sticky= N+W+S+E)
        self.ui_frames["count"].grid( row=1, column = 0, pady=(1,1), sticky= N+W+S+E)
        self.ui_frames["mark_on"].grid( row=2, column = 0, pady=(1,1), sticky= N+W+S+E)
        self.ui_frames["location"].grid( row=3, column = 0, pady=(1,1), sticky= N+W+S+E)
        self.ui_frames["align"].grid( row=4, column = 0, pady=(1,1), sticky= N+W+S+E)
        self.ui_frames["font"].grid( row=5, column = 0, pady=(1,1), sticky= N+W+S+E)
        self.ui_frames["size"].grid( row=6, column = 0, pady=(1,1), sticky= N+W+S+E)
        
        self.main_frame.grid(row= 0, column= 0, padx = (2,2), pady= (2,2), sticky=N+W+S)
    def set_labels(self):
        self.info_labels["onoff"].configure(textvariable= self.string_vars["onoff"], anchor = CENTER, width = self.info_label_width)
        self.info_labels["count"].configure(textvariable= self.string_vars["count"], anchor = CENTER, width = self.info_label_width)
        self.info_labels["mark_on"].configure(textvariable= self.string_vars["mark_on"], anchor = CENTER, width = self.info_label_width)
        self.info_labels["location"].configure(textvariable= self.string_vars["location"], anchor = CENTER, width = self.info_label_width)
        self.info_labels["align"].configure(textvariable= self.string_vars["align"], anchor = CENTER, width = self.info_label_width)
        self.info_labels["font"].configure(textvariable= self.string_vars["font"], anchor = CENTER, width = self.info_label_width)
        self.info_labels["size"].configure(textvariable= self.string_vars["size"], anchor = CENTER, width = self.info_label_width)

        self.info_labels["onoff"].grid(row=0, column=0, sticky = N+S+W)
        self.info_labels["count"].grid(row=0, column=0, sticky = N+S+W)
        self.info_labels["mark_on"].grid(row=0, column=0, sticky = N+S+W)
        self.info_labels["location"].grid(row=0, column=0, sticky = N+S+W)
        self.info_labels["align"].grid(row=0, column=0, sticky = N+S+W)
        self.info_labels["font"].grid(row=0, column=0, sticky = N+S+W)
        self.info_labels["size"].grid(row=0, column=0, sticky = N+S+W)
    def set_inputs(self):
        self.onoff_checkbutton.configure(variable = self.numbering_onoff)

        self.counts_combobox.configure(
                values=list(self.ui_texts["variables"]["count"].values()), 
                width = self.main_entry_width, 
                state = "readonly"
            )
        self.marks_on_combobox.configure(
            values=list(self.ui_texts["variables"]["mark_on"].values()), 
            width = self.main_entry_width, state = "readonly"
            )
        self.location_combobox.configure(
            values=list(self.ui_texts["variables"]["location"].values()), 
            width = self.main_entry_width, state = "readonly")
        self.align_combobox.configure(
            values=list(self.ui_texts["variables"]["align"].values()), width = self.main_entry_width, state = "readonly")
        self.font_combobox.configure(values=self.resources["misc"]["font"], width = self.main_entry_width, state = "readonly")
        self.font_size_combobox.configure(values=self.resources["misc"]["size"], width = self.main_entry_width, state = "readonly")

        self.counts_combobox.current(0)
        self.marks_on_combobox.current(0)
        self.location_combobox.current(0)
        self.align_combobox.current(0)

        self.onoff_checkbutton.grid(row =0, column = 1, padx=(int(0.3*self.width)))
        self.counts_combobox.grid(row =0, column = 1, padx = 10)
        self.marks_on_combobox.grid(row =0, column = 1, padx = 10)
        self.location_combobox.grid(row =0, column = 1, padx = 10)
        self.align_combobox.grid(row =0, column = 1, padx = 10)
        self.font_combobox.grid(row =0, column = 1, padx = 10)
        self.font_size_combobox.grid(row =0, column = 1, padx = 10)


