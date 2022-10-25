from msilib.schema import ComboBox
from booklet.ui import HPFrame, HPLabelFrame
from booklet.ui.tabs import *
class Imposition(HPFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid_anchor(CENTER)

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

        self.sub_frames[0].grid(row=0, column=0, padx=(10, 10), pady=4)
        self.sub_frames[1].grid(row=0, column=1, padx=(10, 10), pady=4)


class BookBrochures(HPLabelFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid_anchor(CENTER)

        # variabels

        # functional variable


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
        self.ui_frames["fold_line"] = HPFrame(self, width = self.width)
        self.ui_frames["fold_gap"] = HPFrame(self, width = self.width)
        self.ui_frames["paper_thickness"] = HPFrame(self, width = self.width)

        # info labels

class Repetition(HPLabelFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid_anchor(CENTER)

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
        self.ui_frames["onoff"] = HPFrame(self, width = self.width)
        self.ui_frames["layout"] = HPFrame(self, width = self.width)
        self.ui_frames["fit"] = HPFrame(self, width = self.width)
        self.ui_frames["gap"] = HPFrame(self, width = self.width)
        self.ui_frames["gap_line"] = HPFrame(self, width = self.width)
        self.ui_frames["paper_format"] = HPFrame(self, width = self.width)
        self.ui_frames["page_format"] = HPFrame(self, width = self.width)
        self.ui_frames["max_fill"] = HPFrame(self, width = self.width)

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
        self.__set_info_labels()
        # inputs
        self.onoff_checkbutton = Checkbutton(self.ui_frames["onoff"])
        
        self.layout_x_entry = Entry(self.ui_frames["layout"])
        self.layout_times_lable = Label(self.ui_frames["layout"])
        self.layout_y_entry = Entry(self.ui_frames["layout"])

        self.fit_mode_combobox = Combobox(self.ui_frames["fit"])

        self.gap_checkbutton = Checkbutton(self.ui_frames["gap"])

        self.gap_line_checkbutton = Checkbutton(self.ui_frames["gap_line"])
        self.gap_line_location_combobox = Combobox(self.ui_frames["gap_line"])
        self.gap_line_color_button = tk_Button(self.ui_frames["gap_line"])
        self.gap_line_type_combobox = Combobox(self.ui_frames["gap_line"])
        self.gap_line_thcik_entry = Entry(self.ui_frames["gap_line"])

        self.paper_format_checkbutton = Checkbutton(self.ui_frames["paper_format"])
        self.paper_format_x_entry = Entry(self.ui_frames["paper_format"])
        self.paper_format_times_label = Label(self.ui_frames["paper_format"])
        self.paper_format_y_entry = Entry(self.ui_frames["paper_format"])

        self.page_format_checkbutton = Checkbutton(self.ui_frames["page_format"])
        self.page_format_x_entry = Entry(self.ui_frames["page_format"])
        self.page_format_times_label = Label(self.ui_frames["page_format"])
        self.page_format_y_entry = Entry(self.ui_frames["page_format"])

        self.max_fill_checkbutton = Checkbutton(self.ui_frames["max_fill"])
        
        self.__set_inputs()

        self.ui_frames["onoff"].grid( row =0 , column =0, padx=(2,2))
        self.ui_frames["layout"].grid( row =1 , column =0, padx=(2,2))
        self.ui_frames["fit"].grid( row =2 , column =0, padx=(2,2))
        self.ui_frames["gap"].grid( row =3 , column =0, padx=(2,2))
        self.ui_frames["gap_line"].grid( row =4 , column =0, padx=(2,2))
        self.ui_frames["paper_format"].grid( row =5 , column =0, padx=(2,2))
        self.ui_frames["page_format"].grid( row =6 , column =0, padx=(2,2))
        self.ui_frames["max_fill"].grid( row =7 , column =0, padx=(2,2))

    def __set_info_labels(self):
        pass
    def __set_inputs(self):
        pass

