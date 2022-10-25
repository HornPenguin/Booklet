from distutils.sysconfig import customize_compiler
from statistics import variance

from numpy import var
from booklet.ui.tabs import *
from booklet.ui import HPFrame, HPLabelFrame
from booklet.data import section 



class Section(HPFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid_anchor(CENTER)

        self.sub_frames.append(
            Standard(
                self,
                self.ui_texts["frames"]["standard"],
                self.resources.pop("standard"),
                width = int(0.5*self.width),
                height = self.height
            )
        )
        self.sub_frames.append(
            Custom(
                self,
                self.ui_texts["frames"]["custom"],
                self.resources.pop("custom"),
                width = int(0.5*self.width),
                height = self.height
            )
        )

        self.sub_frames[0].grid(row = 0, column = 0, padx=10, ipady=4, sticky = N+S+E+W)
        self.sub_frames[1].grid(row = 0, column = 1, padx=10, ipady=4, sticky = N+S+E+W)

class Standard(HPLabelFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid_anchor(CENTER)
        self.grid_propagate(True)

        self.main_frame = HPFrame(self, width = int(0.95*self.width), height = int(0.95*self.height))
        self.main_frame.grid_propagate(False)
        # Variables
        self.custom_format_onoff = BooleanVar(value = False)
        self.custom_format_width = DoubleVar(value = 0.0)
        self.custom_format_height = DoubleVar(value = 0.0)
        self.page_collection_gather = IntVar(value = 0)
        self.page_range = StringVar(value = "")
        self.riffle_direction = BooleanVar(value = False)

        # Functional variables
        self.info_label_width = 14
        self.main_entry_width = 30

        # UI String setting
        self.string_vars["type"] = StringVar(value = self.ui_texts["strings"]["type"])
        self.string_vars["pages_per"] = StringVar(value = self.ui_texts["strings"]["pages_per"])
        self.string_vars["insert"] = StringVar(value = self.ui_texts["strings"]["insert"])
        self.string_vars["paper_format"] = StringVar(value = self.ui_texts["strings"]["paper_format"])
        self.string_vars["custom_format"] = StringVar(value = self.ui_texts["strings"]["custom_format"])
        self.string_vars["page_range"] = StringVar(value = self.ui_texts["strings"]["page_range"])
        self.string_vars["riffle_direction"] = StringVar(value = self.ui_texts["strings"]["riffle_direction"])
        self.string_vars["blank_pages"] = StringVar(value = self.ui_texts["strings"]["blank_pages"])

        # UI Frames
        self.type_frame = HPFrame(self.main_frame, width =int(0.9*self.width))
        self.pages_per_frame = HPFrame(self.main_frame, width =int(0.9*self.width))
        self.insert_frame = HPFrame(self.main_frame, width =int(0.9*self.width))
        self.paper_format_frame = HPFrame(self.main_frame, width =int(0.9*self.width))
        self.custom_format_frame = HPFrame(self.main_frame, width =int(0.9*self.width))
        self.page_range_frame = HPFrame(self.main_frame, width =int(0.9*self.width))
        self.riffle_frame = HPFrame(self.main_frame, width =int(0.9*self.width))
        self.blank_frame = HPFrame(self.main_frame, width =int(0.9*self.width))

        # labels
        self.type_label = Label(self.type_frame)
        self.pages_per_sec_label = Label(self.pages_per_frame)
        self.insert_label = Label(self.insert_frame)
        self.paper_format_label = Label(self.paper_format_frame)
        self.custom_format_label = Label(self.custom_format_frame)
        self.page_range_label = Label(self.page_range_frame)
        self.riffle_label = Label(self.riffle_frame)
        self.blank_label = Label(self.blank_frame)
        self.__set_labels()
        # Frame 2 "inputs"
        self.type_combobox = Combobox(self.type_frame)

        self.pages_per_sec_combobox = Combobox(self.pages_per_frame)
        
        self.brochures_combobox = Combobox(self.pages_per_frame)
        
        self.insert_combobox = Combobox(self.insert_frame)
        self.insert_product_label = Label(self.insert_frame, text="x")
        self.insert_gathered_pages_label  = Label(self.insert_frame)
        
        self.paper_format_combobox = Combobox(self.paper_format_frame)
        
        self.custom_format_onoff_checkbox = Checkbutton(self.custom_format_frame)
        self.custom_format_width_entry = Entry(self.custom_format_frame)
        self.custom_format_product_label = Label(self.custom_format_frame, text="x")
        self.custom_format_height_entry = Entry(self.custom_format_frame)
        
        self.page_range_entry = Entry(self.page_range_frame)
        
        self.riffle_combobox = Combobox(self.riffle_frame)
        
        self.blank_page_combbox = Combobox(self.blank_frame)
        self.__set_inputs()


        # Griding layout frames
        self.type_frame.grid(           row =0, column = 0, pady =1.5, padx = 2, sticky = E+W+S)
        self.pages_per_frame.grid(      row =1, column = 0, pady =1.5, padx = 2, sticky = E+W+S)
        self.insert_frame.grid(         row =2, column = 0, pady= 1.5, padx = 2, sticky = E+W+S)
        self.paper_format_frame.grid(   row =3, column = 0, pady =1.5, padx = 2, sticky = E+W+S)
        self.custom_format_frame.grid(  row =4, column = 0, pady =1.5, padx = 2, sticky = E+W+S)
        self.page_range_frame.grid(     row =5, column = 0, pady =1.5, padx = 2, sticky = E+W+S)
        self.riffle_frame.grid(         row =6, column = 0, pady =1.5, padx = 2, sticky = E+W+S)
        self.blank_frame.grid(          row =7, column = 0, pady =1.5, padx = 2, sticky = E+W+S)
        
        self.main_frame.grid(row = 0, column = 0)

    def __set_labels(self):
        self.type_label.configure(textvariable=self.string_vars["type"], anchor=CENTER, width = self.info_label_width)
        self.pages_per_sec_label.configure(textvariable=self.string_vars["pages_per"], anchor=CENTER, width = self.info_label_width)
        self.insert_label.configure(textvariable=self.string_vars["insert"], anchor=CENTER, width = self.info_label_width)
        self.paper_format_label.configure(textvariable=self.string_vars["paper_format"], anchor=CENTER, width = self.info_label_width)
        self.custom_format_label.configure(textvariable=self.string_vars["custom_format"], anchor=CENTER, width = self.info_label_width)
        self.page_range_label.configure(textvariable=self.string_vars["page_range"], anchor=CENTER, width = self.info_label_width)
        self.riffle_label.configure(textvariable=self.string_vars["riffle_direction"], anchor=CENTER, width = self.info_label_width)
        self.blank_label.configure(textvariable=self.string_vars["blank_pages"], anchor=CENTER, width = self.info_label_width)

        self.type_label.grid(           row=0, column=0, sticky = E+N+S+W)
        self.pages_per_sec_label.grid(  row=0, column=0, sticky = E+N+S+W)
        self.insert_label.grid(         row=0, column=0, sticky = E+N+S+W)
        self.paper_format_label.grid(   row=0, column=0, sticky = E+N+S+W)
        self.custom_format_label.grid(  row=0, column=0, sticky = E+N+S+W)
        self.page_range_label.grid(     row=0, column=0, sticky = E+N+S+W)
        self.riffle_label.grid(         row=0, column=0, sticky = E+N+S+W)
        self.blank_label.grid(          row=0, column=0, sticky = E+N+S+W)
    def __set_inputs(self):

        self.type_combobox.configure(values=section.section_type ,  width = self.main_entry_width, state="readonly")
        self.pages_per_sec_combobox.configure(width =int(0.38*self.main_entry_width), state="readonly")
        
        self.insert_combobox.configure(width = int(0.3*self.main_entry_width), state="readonly")
        self.insert_product_label = Label(self.insert_frame, text="x")
        self.insert_gathered_pages_label.configure(textvariable = self.page_collection_gather, width = int(0.3*self.width))
        
        self.brochures_combobox.configure( values=list(section.brochure_types.keys()),  width = int(0.56*self.main_entry_width), state="readonly")
        self.paper_format_combobox.configure(values=list(section.paper_formats.keys()), width = self.main_entry_width, state="readonly")
        
        self.custom_format_onoff_checkbox.configure(variable=self.custom_format_onoff)
        self.custom_format_width_entry.configure( width = int(0.2*self.main_entry_width))
        self.custom_format_height_entry.configure( width = int(0.2*self.main_entry_width))
        
        self.page_range_entry.configure(      width = self.main_entry_width)
        self.riffle_combobox.configure(value=list(section.riffle.keys()),  width = self.main_entry_width, state="readonly") 
        self.blank_page_combbox.configure(values=list(section.blank_mode) ,  width =self.main_entry_width , state="readonly")

        self.type_combobox.current(0)
        self.pages_per_sec_combobox.set(1)
        self.brochures_combobox.set("-")
        self.paper_format_combobox.current(0)
        self.riffle_combobox.current(0)
        self.blank_page_combbox.current(0)

        self.type_combobox.grid(            row = 0, column = 1)
        self.pages_per_sec_combobox.grid(   row = 0, column = 1, padx=(0, 2))
        self.brochures_combobox.grid(       row = 0, column = 2, padx=(2, 0))
        
        self.insert_combobox.grid(          row = 0, column = 1, padx=(0, 2))
        self.insert_product_label.grid(     row = 0, column = 2, padx= 2)
        self.insert_gathered_pages_label.grid(row=0, column = 3, padx= 2)

        self.paper_format_combobox.grid(    row = 0, column = 1)
        
        self.custom_format_onoff_checkbox.grid(row = 0, column = 1, padx=(0, 2))
        self.custom_format_width_entry.grid(row = 0, column = 2, padx = 2)
        self.custom_format_product_label.grid(row = 0, column = 3, padx = 2)
        self.custom_format_height_entry.grid(row = 0, column = 4, padx = 2)

        self.page_range_entry.grid(         row = 0, column = 1)
        
        self.riffle_combobox.grid(          row = 0, column = 1) 
        
        self.blank_page_combbox.grid(       row = 0, column = 1)

class Custom(HPLabelFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.sub_frames.append(
            Layout(
                self,
                self.ui_texts["frames"]["layout"],
                self.resources.pop("layout"),
                width = self.width
            )
        )
        self.sub_frames.append(
            Fcode(
                self,
                self.ui_texts["frames"]["fcode"],
                self.resources.pop("fcode"),
                width = self.width
            )
        )

        # Functional variables
        self.onoff_var = BooleanVar(value=False)
        # UI variables
        self.string_vars["onoff"] = StringVar(value= self.ui_texts["strings"]["onoff"])
        
        self.ui_frames["onoff"] = HPFrame(self, width = self.width)

        self.onoff_label = Label(self.ui_frames["onoff"])
        self.__set_labels()

        self.onoff_checkbutton = Checkbutton(self.ui_frames["onoff"])
        self.type_combobox = Combobox(self.ui_frames["onoff"])
        self.__set_inputs()
        
        self.ui_frames["onoff"].grid(row=0, column =0) 
        self.sub_frames[0].grid(row= 1 , column =0)
        self.sub_frames[1].grid(row= 2 , column =0)

    def __set_labels(self):
        self.onoff_label.configure(textvariable=self.string_vars["onoff"])
        
        self.onoff_label.grid(row= 0, column =0)
    def __set_inputs(self):
        self.onoff_checkbutton.configure(variable=self.onoff_var)
        self.type_combobox.configure(values = ["layout", "fcode"], state="readonly")

        self.onoff_checkbutton.grid(row= 0, column = 1)
        self.type_combobox.grid(row= 0, column = 2)

class Layout(HPLabelFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Variables
        self.layout_x_var = StringVar(value = "")
        self.layout_y_var = StringVar(value = "")
        self.front_map_var = StringVar(value = "")

        self.fold_sequence = ""

        # Functional variables
        self.main_entry_width = 5

        # Ui string

        self.string_vars["layout"] = StringVar(value = self.ui_texts["strings"]["layout"]) 
        self.string_vars["front"] = StringVar(value = self.ui_texts["strings"]["front"])

        # Ui Frames
        self.ui_frames["layout"] = HPFrame(self, width= self.width)
        self.ui_frames["front"] = HPFrame(self, width= self.width)
        # info labels
        self.info_labels = {}
        self.info_labels["layout"] = Label(self.ui_frames["layout"])
        self.info_labels["front"] = Label(self.ui_frames["front"])
        self.__set_info_labels()
        # inputs

        self.layout_x_entry = Entry(self.ui_frames["layout"])
        self.layout_times_label = Label(self.ui_frames["layout"], text="x")
        self.layout_y_entry = Entry(self.ui_frames["layout"])

        self.front_map_text = Text(self.ui_frames["front"])
        self.__set_inputs()

        self.ui_frames["layout"].grid(row = 0, column = 0, stick=N+S)
        self.ui_frames["front"].grid(row = 1, column = 0, stick=N+S)
    def __set_info_labels(self):
        self.info_labels["layout"].configure(textvariable = self.string_vars["layout"])
        self.info_labels["front"].configure(textvariable = self.string_vars["front"])

        self.info_labels["layout"].grid(row = 0, column = 0)
        self.info_labels["front"].grid(row = 0, column = 0)
    def __set_inputs(self):
        self.layout_x_entry.configure(textvariable = self.layout_x_var, width = self.main_entry_width)
        self.layout_y_entry.configure(textvariable = self.layout_y_var, width = self.main_entry_width)

        self.front_map_text.configure(width = 10, height = 5)

        self.front_map_text.grid(row= 0, column=1, padx = (2,2), sticky=N+W+S+E)

        self.layout_x_entry.grid(row= 0, column=1, padx = 2, sticky=N+S+W)
        self.layout_times_label.grid(row= 0, column=2, padx = 2, sticky=N+S+W)
        self.layout_y_entry.grid(row= 0, column=3, padx = 2, sticky=N+S+W)

class Fcode(HPLabelFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Ui frame
        self.ui_frames["start_axis"] = HPFrame(self, width=self.width)
        self.ui_frames["button"] = HPFrame(self)
        
        # Variables
        self.string_vars["start_axis"] = StringVar(value = self.ui_texts["strings"]["start_axis"])
        self.string_vars["preview"] = StringVar(value = self.ui_texts["strings"]["preview"])
        self.string_vars["apply"] = StringVar(value = self.ui_texts["strings"]["apply"])
        
        # Info label
        self.info_labels = {}
        self.info_labels["start_axis"] = Label(self.ui_frames["start_axis"])
        self.__set_info_labels()
        # Inputs
        self.start_axis_combobox = Combobox(self.ui_frames["start_axis"])
        self.fcode_input_text = Text(self, width =20, height= 8)
        self.view_preview_button = Button(self.ui_frames["button"])
        self.apply_button = Button(self.ui_frames["button"])
        self.__set_inputs()
        
        self.ui_frames["start_axis"].grid(row=0, column = 0)
        self.fcode_input_text.grid(row=1, column=0)
        self.ui_frames["button"].grid(row=2, column = 0)
    def __set_info_labels(self):
        self.info_labels["start_axis"].configure(textvariable=self.string_vars["start_axis"])
        self.info_labels["start_axis"].grid(row=0, column=0)
    def __set_inputs(self):
        self.start_axis_combobox.configure(values = self.resources["misc"]["start_axis"], state="readonly")
        self.start_axis_combobox.current(0)
        self.view_preview_button.configure(textvariable= self.string_vars["preview"])
        self.apply_button.configure(textvariable= self.string_vars["apply"])

        self.start_axis_combobox.grid(row=0, column=1)
        self.view_preview_button.grid(row=0, column=0)
        self.apply_button.grid(row=0, column=1)
        