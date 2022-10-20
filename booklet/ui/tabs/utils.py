from booklet.ui.tabs import *
from booklet.ui import HPFrame, HPLabelFrame


class Utils(HPFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.sub_frames.append(
            ToImage(
                self,
                self.ui_texts["frames"]["toimage"],
                self.resources["toimage"],
                width = int(0.48*self.width),
                height = int(0.48*self.height)
            )
        )
        self.sub_frames.append(
            Duplex(
                self,
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

        self.sub_frames[0].grid(row=0, column=0, pady = 4, padx = (10,10), sticky= N+W+E)
        self.sub_frames[1].grid(row=1, column=0, pady = 4, padx = (10,10), sticky= N+W+E)
        self.sub_frames[2].grid(row=0, column=1, rowspan= 2, pady = 4, padx = (10,10), sticky= N+S+E)
        
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
        self.__set_label()
        self.__set_inputs()
        self.ui_frames["image"].grid(row=0, column=0, padx= 4, pady = 4, sticky=N+S+W)
        self.main_frame.grid(row=0, column= 0, sticky=N+S+W)
    def __set_label(self):
        self.toimage_onoff_label.configure(textvariable=self.string_vars["onoff"], width=self.info_label_width, anchor = CENTER)

        self.toimage_onoff_label.grid(row=0, column=0,  sticky=N+S+W)
    def __set_inputs(self):
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
        self.__set_info_labels()
        
        # input elements
        self.onoff_checkbutton = Checkbutton(self.ui_frames["onoff"])
        self.translation_checkbutton = Checkbutton(self.ui_frames["translation"])
        self.translation_x_entry = Entry(self.ui_frames["translation"])
        self.translation_comma_label = Label(self.ui_frames["translation"], text=", ")
        self.translation_y_entry = Entry(self.ui_frames["translation"])
        self.rotation_checkbutton = Checkbutton(self.ui_frames["rotation"])
        self.rotation_entry = Entry(self.ui_frames["rotation"])
        self.preserve_checkbutton = Checkbutton(self.ui_frames["preserve"])
        self.__set_inputs()
        
        # Grid
        self.ui_frames["onoff"].grid(       row= 0, column =0, pady = 4, sticky= W+N+S)
        self.ui_frames["translation"].grid( row= 1, column =0, pady = 4, sticky= W+N+S)
        self.ui_frames["rotation"].grid(    row= 2, column =0, pady = 4, sticky= W+N+S)
        self.ui_frames["preserve"].grid(    row= 3, column =0, pady = 4, sticky= W+N+S)

        #self.ui_frames["onoff"].configure(borderwidth=2, relief="groove")
        #self.main_frame.configure(borderwidth=2, relief="groove")
        self.main_frame.grid(row=0 , column=0, pady=(4,4), sticky= N+S+W)

    def __set_info_labels(self):

        self.info_labels["onoff"].configure(textvariable = self.string_vars["onoff"], width = self.info_label_width, anchor = CENTER)
        self.info_labels["translation"].configure(textvariable = self.string_vars["translation"], width = self.info_label_width, anchor = CENTER)
        self.info_labels["rotation"].configure(textvariable = self.string_vars["rotation"], width = self.info_label_width, anchor = CENTER)
        self.info_labels["preserve"].configure(textvariable = self.string_vars["preserve"], width = self.info_label_width, anchor = CENTER)

        self.info_labels["onoff"].grid( row= 0, column = 0 , sticky = W+N+S)
        self.info_labels["translation"].grid( row= 0, column = 0 , sticky = W+N+S)
        self.info_labels["rotation"].grid( row= 0, column = 0 , sticky = W+N+S)
        self.info_labels["preserve"].grid( row= 0, column = 0 , sticky = W+N+S)
    def __set_inputs(self):
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

        # Ui strings

        # Ui frames


class Numbering(HPLabelFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Variables

        # Functional variables

        # Ui strings

        # Ui frames

