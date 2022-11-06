from logging.config import valid_ident
import re

from booklet.ui.tabs import *
from booklet.ui import Validate, HPFrame, HPLabelFrame, HPVScrollWapper
from booklet.data import section 



class Section(HPFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid_anchor(CENTER)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

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
    
    page_range_format_re_str = r"([ ]{0,}\d+[ ]{0,}-{1,1}[ ]{0,}\d+[ ]{0,}|[ ]{0,}\d+[ ]{0,})"
    invaild_chars_re_str= r"([^-,\d\s])+?"

    page_range_extractor = re.compile(page_range_format_re_str)
    invaild_chars_extractor = re.compile(invaild_chars_re_str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.grid_anchor(CENTER)
        self.grid_propagate(True)

        self.main_frame = HPFrame(self, width = int(0.95*self.width), height = int(0.95*self.height))
        self.main_frame.grid_propagate(False)
        # Variables
        self.onoff_bool = BooleanVar(value = False)
        self.custom_format_onoff = BooleanVar(value = False)
        self.custom_format_width = DoubleVar(value = 0.0)
        self.custom_format_height = DoubleVar(value = 0.0)
        self.page_collection_gather = IntVar(value = 0)
        self.page_range = StringVar(value = "")
        self.page_range_total = IntVar(value = 0)
        self.riffle_direction = BooleanVar(value = False)

        # Functional variables
        self.info_label_width = 14
        self.main_entry_width = 30

        # UI String setting
        self.string_vars["onoff"] = StringVar(value = self.ui_texts["strings"]["onoff"])
        self.string_vars["type"] = StringVar(value = self.ui_texts["strings"]["type"])
        self.string_vars["pages_per"] = StringVar(value = self.ui_texts["strings"]["pages_per"])
        self.string_vars["insert"] = StringVar(value = self.ui_texts["strings"]["insert"])
        self.string_vars["paper_format"] = StringVar(value = self.ui_texts["strings"]["paper_format"])
        self.string_vars["custom_format"] = StringVar(value = self.ui_texts["strings"]["custom_format"])
        self.string_vars["page_range"] = StringVar(value = self.ui_texts["strings"]["page_range"])
        self.string_vars["riffle_direction"] = StringVar(value = self.ui_texts["strings"]["riffle_direction"])
        self.string_vars["blank_pages"] = StringVar(value = self.ui_texts["strings"]["blank_pages"])

        # UI Frames
        self.ui_frames["onoff"] = HPFrame(self.main_frame, width =int(0.9*self.width))
        self.ui_frames["type"] = HPFrame(self.main_frame, width =int(0.9*self.width))
        self.ui_frames["pages_per"] = HPFrame(self.main_frame, width =int(0.9*self.width))
        self.ui_frames["insert"] = HPFrame(self.main_frame, width =int(0.9*self.width))
        self.ui_frames["paper_format"] = HPFrame(self.main_frame, width =int(0.9*self.width))
        self.ui_frames["custom_format"] = HPFrame(self.main_frame, width =int(0.9*self.width))
        self.ui_frames["page_range"] = HPFrame(self.main_frame, width =int(0.9*self.width))
        self.ui_frames["riffle"] = HPFrame(self.main_frame, width =int(0.9*self.width))
        self.ui_frames["blank"] = HPFrame(self.main_frame, width =int(0.9*self.width))

        # labels
        self.onoff_label = Label(self.ui_frames["onoff"])
        self.type_label = Label(self.ui_frames["type"])
        self.pages_per_sec_label = Label(self.ui_frames["pages_per"])
        self.insert_label = Label(self.ui_frames["insert"])
        self.paper_format_label = Label(self.ui_frames["paper_format"])
        self.custom_format_label = Label(self.ui_frames["custom_format"])
        self.page_range_label = Label(self.ui_frames["page_range"])
        self.page_range_total_label = Label(self.ui_frames["page_range"])
        self.riffle_label = Label(self.ui_frames["riffle"])
        self.blank_label = Label(self.ui_frames["blank"])
        self.set_labels()

        # Frame 2 "inputs"
        self.onoff_checkbutton = Checkbutton(self.ui_frames["onoff"])

        self.type_combobox = Combobox(self.ui_frames["type"])

        self.pages_per_sec_combobox = Combobox(self.ui_frames["pages_per"])
        
        self.brochures_combobox = Combobox(self.ui_frames["pages_per"])
        
        self.insert_combobox = Combobox(self.ui_frames["insert"])
        self.insert_product_label = Label(self.ui_frames["insert"], text="x")
        self.insert_gathered_pages_label  = Label(self.ui_frames["insert"])
        
        self.paper_format_combobox = Combobox(self.ui_frames["paper_format"])
        
        self.custom_format_onoff_checkbox = Checkbutton(self.ui_frames["custom_format"])
        self.custom_format_width_entry = Entry(self.ui_frames["custom_format"])
        self.custom_format_product_label = Label(self.ui_frames["custom_format"], text="x")
        self.custom_format_height_entry = Entry(self.ui_frames["custom_format"])
        
        self.page_range_entry = Entry(self.ui_frames["page_range"])
        
        self.riffle_combobox = Combobox(self.ui_frames["riffle"])
        
        self.blank_page_combbox = Combobox(self.ui_frames["blank"])
        self.set_inputs()

        self.validation_setting()

        # Griding layout frames
        self.ui_frames["onoff"].grid(          row =0, column = 0, pady =1.5, padx = 2, sticky = E+W+S)
        self.ui_frames["type"].grid(           row =1, column = 0, pady =1.5, padx = 2, sticky = E+W+S)
        self.ui_frames["pages_per"].grid(      row =2, column = 0, pady =1.5, padx = 2, sticky = E+W+S)
        self.ui_frames["insert"].grid(         row =3, column = 0, pady= 1.5, padx = 2, sticky = E+W+S)
        self.ui_frames["paper_format"].grid(   row =4, column = 0, pady =1.5, padx = 2, sticky = E+W+S)
        self.ui_frames["custom_format"].grid(  row =5, column = 0, pady =1.5, padx = 2, sticky = E+W+S)
        self.ui_frames["page_range"].grid(     row =6, column = 0, pady =1.5, padx = 2, sticky = E+W+S)
        self.ui_frames["riffle"].grid(         row =7, column = 0, pady =1.5, padx = 2, sticky = E+W+S)
        self.ui_frames["blank"].grid(          row =8, column = 0, pady =1.5, padx = 2, sticky = E+W+S)
        
        self.main_frame.grid(row = 0, column = 0)

    def set_labels(self):
        self.onoff_label.configure(textvariable=self.string_vars["onoff"], anchor = CENTER, width = self.info_label_width)
        self.type_label.configure(textvariable=self.string_vars["type"], anchor=CENTER, width = self.info_label_width)
        self.pages_per_sec_label.configure(textvariable=self.string_vars["pages_per"], anchor=CENTER, width = self.info_label_width)
        self.insert_label.configure(textvariable=self.string_vars["insert"], anchor=CENTER, width = self.info_label_width)
        self.paper_format_label.configure(textvariable=self.string_vars["paper_format"], anchor=CENTER, width = self.info_label_width)
        self.custom_format_label.configure(textvariable=self.string_vars["custom_format"], anchor=CENTER, width = self.info_label_width)
        self.page_range_label.configure(textvariable=self.string_vars["page_range"], anchor=CENTER, width = self.info_label_width)
        self.riffle_label.configure(textvariable=self.string_vars["riffle_direction"], anchor=CENTER, width = self.info_label_width)
        self.blank_label.configure(textvariable=self.string_vars["blank_pages"], anchor=CENTER, width = self.info_label_width)

        self.onoff_label.grid(          row=0, column=0, sticky = E+N+S+W)
        self.type_label.grid(           row=0, column=0, sticky = E+N+S+W)
        self.pages_per_sec_label.grid(  row=0, column=0, sticky = E+N+S+W)
        self.insert_label.grid(         row=0, column=0, sticky = E+N+S+W)
        self.paper_format_label.grid(   row=0, column=0, sticky = E+N+S+W)
        self.custom_format_label.grid(  row=0, column=0, sticky = E+N+S+W)
        self.page_range_label.grid(     row=0, column=0, sticky = E+N+S+W)
        self.riffle_label.grid(         row=0, column=0, sticky = E+N+S+W)
        self.blank_label.grid(          row=0, column=0, sticky = E+N+S+W)
    def set_inputs(self):

        self.onoff_checkbutton.configure(variable= self.onoff_bool)

        self.type_combobox.configure(values=section.section_type ,  width = self.main_entry_width, state="readonly")
        self.pages_per_sec_combobox.configure(width =int(0.38*self.main_entry_width), state="readonly")
        
        self.insert_combobox.configure(width = int(0.3*self.main_entry_width), state="readonly")
        self.insert_product_label = Label(self.ui_frames["insert"], text="x")
        self.insert_gathered_pages_label.configure(textvariable = self.page_collection_gather, width = int(0.3*self.width))
        
        self.brochures_combobox.configure( values=list(section.brochure_types.keys()),  width = int(0.56*self.main_entry_width), state="readonly")
        self.paper_format_combobox.configure(values=list(section.paper_formats.keys()), width = self.main_entry_width, state="readonly")
        
        self.custom_format_onoff_checkbox.configure(variable=self.custom_format_onoff)
        self.custom_format_width_entry.configure( width = int(0.2*self.main_entry_width))
        self.custom_format_height_entry.configure( width = int(0.2*self.main_entry_width))
        
        self.page_range_entry.configure(textvariable = self.page_range, width = int(0.8*self.main_entry_width))
        self.page_range_total_label.configure(textvariable=self.page_range_total)
        self.riffle_combobox.configure(value=list(section.riffle.keys()),  width = self.main_entry_width, state="readonly") 
        self.blank_page_combbox.configure(values=list(section.blank_mode) ,  width =self.main_entry_width , state="readonly")

        self.type_combobox.current(0)
        self.pages_per_sec_combobox.set(1)
        self.brochures_combobox.set("-")
        self.paper_format_combobox.current(0)
        self.riffle_combobox.current(0)
        self.blank_page_combbox.current(0)


        self.onoff_checkbutton.grid(        row = 0, column = 1, padx = int(0.32*self.width))
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
        self.page_range_total_label.grid(   row = 0, column = 2, padx = 4)
        
        self.riffle_combobox.grid(          row = 0, column = 1) 
        
        self.blank_page_combbox.grid(       row = 0, column = 1)

    def validation_setting(self):

        #self.onoff_checkbutton.configure()
        page_validator_command = self.register(self._validate_page_range)
        positive_double_validator_command = self.register(Validate.double_value)

        self.page_range_entry.configure(validate = "all", validatecommand=(page_validator_command, "%V", "%P", r"%s", "%S"))
        self.custom_format_width_entry.configure(validate = "all", validatecommand = (positive_double_validator_command, "%V", "%P", r"%s", "%S"))
        self.custom_format_height_entry.configure(validate = "all", validatecommand = (positive_double_validator_command, "%V", "%P", r"%s", "%S"))

    # %V, %P, %s, %S
    def _validate_page_range(self, event,  current_text, previous_text, inserted_text):
        text_c = current_text.replace(" ", "")
        if text_c == "" or text_c is None:
            return True
        if text_c[0] not in "123456789":
            return False
        if self.invaild_chars_extractor.search(text_c) is not None:
            print(f"Invaild characters: {self.invaild_chars_extractor.findall(text_c)}")
            return False
        # Total page of pdf
        # how to get? 
        #  self.parent.parent.get_frames_property
        # self.parent : Section
        # self.parent.parent : HPNotebook frame
        file_io_index = self.parent.parent.INDEX["FileIO"]
        FileIO_Frame = list(self.parent.parent.children.values())[file_io_index]
        
        total_pages = FileIO_Frame.get_frames_property(FileIO_Frame.OUTPUT, "total_pages").get()
        range_list = self.page_range_extractor.findall(text_c)
        
        pre =1
        range_total = 0
        for page_str in range_list:
            if "-" in page_str:
                i_s, l_s = page_str.split("-")
                if i_s == "":
                    print("Negative number")
                    return False
                i = int(i_s)
                l = int(l_s)
                if (i <= pre and pre >1):
                    pass
                if i >= l:
                    if event == "focusout":
                        self.page_range.set(f"1-{total_pages}")
                        return False
                    if len(i_s) < len(l_s):
                        pre = ",".join(previous_text.split(",")[0:-1])
                        self.page_range.set(pre)
                        return False
                if l > total_pages:
                    return False
                pre = l
                range_total += l - i +1
            else:
                n = int(page_str)
                if n > total_pages:
                    return False
                if (n<= pre and pre >1):
                    if event == "focusout":
                        pre = ",".join(previous_text.split(",")[0:-1])
                        self.page_range.set(pre)
                        return False
                    if str(pre) < page_str:
                        pre = ",".join(previous_text.split(",")[0:-1])
                        self.page_range.set(pre)
                        return False
                pre = n
                range_total += 1

        self.page_range_total.set(range_total)
        return True

class Custom(HPLabelFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.grid_anchor(CENTER)
        self.grid_propagate(True)

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

        # Variables
        self.onoff_var = BooleanVar(value=False)
        # Functional variables
        self.info_labels_width = 15
        self.main_entry_width = 30
        # UI variables
        self.string_vars["onoff"] = StringVar(value= self.ui_texts["strings"]["onoff"])
        
        self.ui_frames["onoff"] = HPFrame(self, width = self.width)

        self.onoff_label = Label(self.ui_frames["onoff"])
        self.set_labels()

        self.onoff_checkbutton = Checkbutton(self.ui_frames["onoff"])
        self.type_combobox = Combobox(self.ui_frames["onoff"])
        self.set_inputs()
        
        self.ui_frames["onoff"].grid(row=0, column =0, pady =1.5, padx = (4,4))
        self.sub_frames[0].grid(row= 1 , column =0, pady =1.5, padx = (4,4), sticky= N+S+W+E)
        self.sub_frames[1].grid(row= 2 , column =0, pady =1.5, padx = (4,4), sticky= N+S+W+E)

    def set_labels(self):
        self.onoff_label.configure(
            textvariable=self.string_vars["onoff"], 
            width = self.info_labels_width,
            anchor= CENTER
            )
        
        self.onoff_label.grid(row= 0, column =0)
    def set_inputs(self):
        self.onoff_checkbutton.configure(variable=self.onoff_var)
        self.type_combobox.configure(values = ["layout", "fcode"], state="readonly", width = int(0.4*self.main_entry_width))
        #self.type_combobox.current(0)

        self.onoff_checkbutton.grid(row= 0, column = 1)
        self.type_combobox.grid(row= 0, column = 2, padx=(2, 20))

class Layout(HPLabelFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid_anchor(CENTER)
        # Variables
        self.layout_x_var = StringVar(value = "")
        self.layout_y_var = StringVar(value = "")
        self.front_map_var = StringVar(value = "")

        self.fold_sequence = ""

        # Functional variables
        self.info_labels_width = 15
        self.main_entry_width = 15
        # Ui string

        self.string_vars["layout"] = StringVar(value = self.ui_texts["strings"]["layout"]) 
        self.string_vars["front"] = StringVar(value = self.ui_texts["strings"]["front"])

        # Ui Frames
        self.ui_frames["layout"] = HPFrame(self, width= self.width)
        self.scroll_frame = HPVScrollWapper(self, width = self.width, height= int(0.7*self.height))
        self.ui_frames["front"] = HPFrame(self.scroll_frame, width= self.width)
        # info labels
        self.info_labels = {}
        self.info_labels["layout"] = Label(self.ui_frames["layout"])
        self.info_labels["front"] = Label(self.ui_frames["front"])
        self.set_info_labels()
        # inputs

        self.layout_x_entry = Entry(self.ui_frames["layout"])
        self.layout_times_label = Label(self.ui_frames["layout"], text="x")
        self.layout_y_entry = Entry(self.ui_frames["layout"])

        self.front_map_text = Text(self.ui_frames["front"])
        self.set_inputs()

        self.validation_setting()

        self.ui_frames["layout"].grid(row = 0, column = 0, pady=2, stick=N+S)
        self.scroll_frame.grid(row= 1, column = 0, pady=2, ipady=2, stick=N+W+S)
        self.ui_frames["front"].grid(row = 0, column = 0, stick=N+W+S)
    def set_info_labels(self):
        self.info_labels["layout"].configure(textvariable = self.string_vars["layout"], width = self.info_labels_width, anchor=CENTER)
        self.info_labels["front"].configure(textvariable = self.string_vars["front"], width = self.info_labels_width, anchor=CENTER)

        self.info_labels["layout"].grid(row = 0, column = 0)
        self.info_labels["front"].grid(row = 0, column = 0)
    def set_inputs(self):
        self.layout_x_entry.configure(textvariable = self.layout_x_var, width = self.main_entry_width)
        self.layout_y_entry.configure(textvariable = self.layout_y_var, width = self.main_entry_width)

        self.front_map_text.configure(width = 36, height = 6)

        self.front_map_text.grid(row= 0, column=1, padx = (2,2), sticky=N+W+S+E)

        self.layout_x_entry.grid(row= 0, column=1, padx = 2, sticky=N+S+W)
        self.layout_times_label.grid(row= 0, column=2, padx = 2, sticky=N+S+W)
        self.layout_y_entry.grid(row= 0, column=3, padx = 2, sticky=N+S+W)

    def validation_setting(self):
        positive_integer_validation = self.register(Validate.int_positive_value)
        self.layout_x_entry.configure(validate="all", validatecommand=(positive_integer_validation , "%V", "%P", r"%s", "%S"))
        self.layout_y_entry.configure(validate="all", validatecommand=(positive_integer_validation , "%V", "%P", r"%s", "%S"))

class Fcode(HPLabelFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid_anchor(CENTER)

        
        # Variables
        self.string_vars["start_axis"] = StringVar(value = self.ui_texts["strings"]["start_axis"])
        self.string_vars["preview"] = StringVar(value = self.ui_texts["strings"]["preview"])
        self.string_vars["apply"] = StringVar(value = self.ui_texts["strings"]["apply"])
        
        # Functional variables
        self.info_labels_width = 15

        # Ui frame
        self.ui_frames["start_axis"] = HPFrame(self, width=self.width)
        self.ui_frames["scroll_text"] = HPVScrollWapper(self, width= self.width, height = self.height)
        self.ui_frames["button"] = HPFrame(self)
        

        # Info label
        self.info_labels = {}
        self.info_labels["start_axis"] = Label(self.ui_frames["start_axis"])
        self.set_info_labels()
        # Inputs
        self.start_axis_combobox = Combobox(self.ui_frames["start_axis"])
        self.fcode_input_text = Text(self.ui_frames["scroll_text"], width =45, height= 8)
        self.view_preview_button = Button(self.ui_frames["button"])
        self.apply_button = Button(self.ui_frames["button"])
        self.set_inputs()
        
        self.ui_frames["start_axis"].grid(  row=0, column = 0, pady= 2, sticky=N+S)
        self.ui_frames["scroll_text"].grid( row=1, column = 0, pady= 2, sticky=N+S+E)
        self.ui_frames["button"].grid(      row=2, column = 0, pady= 2, sticky=N+S)
    def set_info_labels(self):
        self.info_labels["start_axis"].configure(
            textvariable=self.string_vars["start_axis"], 
            width = self.info_labels_width, 
            anchor = CENTER
            )
        self.info_labels["start_axis"].grid(row=0, column=0)
    def set_inputs(self):
        self.start_axis_combobox.configure(values = self.resources["misc"]["start_axis"], state="readonly")
        self.start_axis_combobox.current(0)
        self.view_preview_button.configure(textvariable= self.string_vars["preview"])
        self.apply_button.configure(textvariable= self.string_vars["apply"])

        self.start_axis_combobox.grid(row=0, column=1, padx=2)
        self.view_preview_button.grid(row=0, column=0, padx=2)
        self.apply_button.grid(row=0, column=1)
        self.fcode_input_text.grid(row=0, column=0, sticky=N+S+E)
        