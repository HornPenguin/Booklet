from booklet.ui.tabs import *
from booklet.ui import Validate, HPFrame, HPLabelFrame

from PIL import ImageTk



class PrintingMarks(HPFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sub_frames.append(
            Marks(
                self,
                self.ui_texts["frames"]["printingmarks"],
                self.resources["printingmarks"],
                width = self.width,
                height = self.height
            )
        )
        
        self.sub_frames[0].grid(row=0, column=0, padx = (10, 10), pady =4 , sticky = N+S)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

class Marks(HPLabelFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.grid_anchor(CENTER)

        #self.text = Text(self, width =30, height =8)
        #self.text.grid(row =0, column =0)

        # Variables
        self.margin_onoff = BooleanVar(value = False)
        self.margin_double  = DoubleVar(value = 0.)
        self.crop_onoff = BooleanVar(value = False)
        self.trim_onoff = BooleanVar(value = False)
        self.registration_onoff = BooleanVar(value = False)
        self.cmyk_onoff = BooleanVar(value = False)
        self.direction_onoff = BooleanVar(value = False)
        self.angle_onoff = BooleanVar(value = False)
        self.duplex_onoff = BooleanVar(value = False)

        # Functional variables
        self.info_labels_width = 15
        self.main_entry_width = 30

        # Ui strings

        self.string_vars["margin"] = StringVar(value = self.ui_texts["strings"]["margin"])
        self.string_vars["crop"] = StringVar(value = self.ui_texts["strings"]["crop"])
        self.string_vars["trim"] = StringVar(value = self.ui_texts["strings"]["trim"])
        self.string_vars["reg"] = StringVar(value = self.ui_texts["strings"]["reg"])
        self.string_vars["cmyk"] = StringVar(value = self.ui_texts["strings"]["cmyk"])
        self.string_vars["direction"] = StringVar(value = self.ui_texts["strings"]["direction"])
        self.string_vars["angle"] = StringVar(value = self.ui_texts["strings"]["angle"])
        self.string_vars["duplex"] = StringVar(value = self.ui_texts["strings"]["duplex"])
        # Ui frames

        self.ui_frames["margin"] = HPFrame(self, width = self.width)
        self.ui_frames["crop"] = HPFrame(self, width = self.width)
        self.ui_frames["trim"] = HPFrame(self, width = self.width)
        self.ui_frames["reg"] = HPFrame(self, width = self.width)
        self.ui_frames["cmyk"] = HPFrame(self, width = self.width)
        self.ui_frames["direction"] = HPFrame(self, width = self.width)
        self.ui_frames["angle"] = HPFrame(self, width = self.width)
        self.ui_frames["duplex"] = HPFrame(self, width = self.width)

        # info labels
        self.info_labels = {}
        self.info_labels["margin"] = Label(self.ui_frames["margin"])
        self.info_labels["crop"] = Label(self.ui_frames["crop"])
        self.info_labels["trim"] = Label(self.ui_frames["trim"])
        self.info_labels["reg"] = Label(self.ui_frames["reg"])
        self.info_labels["cmyk"] = Label(self.ui_frames["cmyk"])
        self.info_labels["direction"] = Label(self.ui_frames["direction"])
        self.info_labels["angle"] = Label(self.ui_frames["angle"])
        self.info_labels["duplex"] = Label(self.ui_frames["duplex"])
        self.set_info_labels()
        # inputs
        self.margin_entry = Entry(self.ui_frames["margin"])
        self.margin_checkbutton = Checkbutton(self.ui_frames["margin"])
        self.crop_checkbutton = Checkbutton(self.ui_frames["crop"])
        self.trim_checkbutton = Checkbutton(self.ui_frames["trim"])
        self.reg_checkbutton = Checkbutton(self.ui_frames["reg"])
        self.cmyk_checkbutton = Checkbutton(self.ui_frames["cmyk"])
        self.direction_checkbutton = Checkbutton(self.ui_frames["direction"])
        self.angle_checkbutton = Checkbutton(self.ui_frames["angle"])
        self.duplex_checkbutton = Checkbutton(self.ui_frames["duplex"])
        self.set_inputs()

        # Routine images
        self.crop_image_label = Label(self.ui_frames["crop"])
        self.trim_image_label = Label(self.ui_frames["trim"])
        self.reg_image_label = Label(self.ui_frames["reg"])
        self.cmyk_image_label = Label(self.ui_frames["cmyk"])
        self.direction_image_label = Label(self.ui_frames["direction"])
        self.angle_image_label = Label(self.ui_frames["angle"])
        self.duplex_image_label = Label(self.ui_frames["duplex"])
        self.set_images()

        self.validation_setting()

        self.ui_frames["margin"].grid(      row= 0, column =0, pady= 2, sticky=N+S+W)
        self.ui_frames["crop"].grid(        row= 1, column =0, pady= 2, sticky=N+S+W)
        self.ui_frames["trim"].grid(        row= 2, column =0, pady= 2, sticky=N+S+W)
        self.ui_frames["reg"].grid(         row= 3, column =0, pady= 2, sticky=N+S+W)
        self.ui_frames["cmyk"].grid(        row= 4, column =0, pady= 2, sticky=N+S+W)
        self.ui_frames["direction"].grid(   row= 5, column =0, pady= 2, sticky=N+S+W)
        self.ui_frames["angle"].grid(       row= 6, column =0, pady= 2, sticky=N+S+W)
        self.ui_frames["duplex"].grid(      row= 7, column =0, pady= 2, sticky=N+S+W)

    def set_info_labels(self,):
        self.info_labels_width 

        self.info_labels["margin"].configure(textvariable=self.string_vars["margin"], anchor=CENTER, width = self.info_labels_width )
        self.info_labels["crop"].configure(textvariable=self.string_vars["crop"], anchor=CENTER, width = self.info_labels_width )
        self.info_labels["trim"].configure(textvariable=self.string_vars["trim"], anchor=CENTER, width = self.info_labels_width )
        self.info_labels["reg"].configure(textvariable=self.string_vars["reg"], anchor=CENTER, width = self.info_labels_width )
        self.info_labels["cmyk"].configure(textvariable=self.string_vars["cmyk"], anchor=CENTER, width = self.info_labels_width )
        self.info_labels["direction"].configure(textvariable=self.string_vars["direction"], anchor=CENTER, width = self.info_labels_width )
        self.info_labels["angle"].configure(textvariable=self.string_vars["angle"], anchor=CENTER, width = self.info_labels_width )
        self.info_labels["duplex"].configure(textvariable=self.string_vars["duplex"], anchor=CENTER, width = self.info_labels_width )

        self.info_labels["margin"].grid(row = 0, column =0, sticky= N+S+W)
        self.info_labels["crop"].grid(row = 0, column =0, sticky= N+S+W)
        self.info_labels["trim"].grid(row = 0, column =0, sticky= N+S+W)
        self.info_labels["reg"].grid(row = 0, column =0, sticky= N+S+W)
        self.info_labels["cmyk"].grid(row = 0, column =0, sticky= N+S+W)
        self.info_labels["direction"].grid(row = 0, column =0, sticky= N+S+W)
        self.info_labels["angle"].grid(row = 0, column =0, sticky= N+S+W)
        self.info_labels["duplex"].grid(row = 0, column =0, sticky= N+S+W)
    def set_inputs(self,):
        self.margin_checkbutton.configure(variable = self.margin_onoff)
        self.margin_entry.configure(textvariable=self.margin_double, width =int(0.4*self.main_entry_width))

        self.crop_checkbutton.configure(variable = self.crop_onoff)
        self.trim_checkbutton.configure(variable = self.trim_onoff)
        self.reg_checkbutton.configure(variable = self.registration_onoff)
        self.cmyk_checkbutton.configure(variable = self.cmyk_onoff)
        self.direction_checkbutton.configure(variable = self.direction_onoff)
        self.angle_checkbutton.configure(variable = self.angle_onoff)
        self.duplex_checkbutton.configure(variable = self.duplex_onoff)

        self.margin_checkbutton.grid( row= 0, column = 1, padx = 2)
        self.margin_entry.grid( row= 0, column = 2, padx = 2)

        self.crop_checkbutton.grid(         row= 0, column = 1, padx =2)
        self.trim_checkbutton.grid(         row= 0, column = 1, padx =2)
        self.reg_checkbutton.grid(          row= 0, column = 1, padx =2)
        self.cmyk_checkbutton.grid(         row= 0, column = 1, padx =2)
        self.direction_checkbutton.grid(    row= 0, column = 1, padx =2)
        self.angle_checkbutton.grid(        row= 0, column = 1, padx =2)
        self.duplex_checkbutton.grid(       row= 0, column = 1, padx =2)
    def set_images(self):
        self.imagetk = {key : ImageTk.PhotoImage(self.resources["images"][key], master = self) for key in self.resources["images"]} 
        self.crop_image_label.configure(        image= self.imagetk["crop"])
        self.trim_image_label.configure(        image= self.imagetk["trim"])
        self.reg_image_label.configure(         image= self.imagetk["registration"])
        self.cmyk_image_label.configure(        image= self.imagetk["cmyk"])
        self.direction_image_label.configure(   image= self.imagetk["direction"])
        self.angle_image_label.configure(       image= self.imagetk["angle"])
        self.duplex_image_label.configure(      image= self.imagetk["duplex"])

        self.crop_image_label.grid(row=0,column =2, padx = (2, 2), pady=(1,1))
        self.trim_image_label.grid(row=0,column =2, padx = (2, 2), pady=(1,1))
        self.reg_image_label.grid(row=0,column =2, padx = (2, 2), pady=(1,1))
        self.cmyk_image_label.grid(row=0,column =2, padx = (2, 2), pady=(1,1))
        self.direction_image_label.grid(row=0,column =2, padx = (2, 2), pady=(1,1))
        self.angle_image_label.grid(row=0,column =2, padx = (2, 2), pady=(1,1))
        self.duplex_image_label.grid(row=0,column =2, padx = (2, 2), pady=(1,1))
    def validation_setting(self):

        positive_double_validation = self.register(Validate.double_positive_value)
        self.margin_entry.configure(
            validate="all",
            validatecommand=(positive_double_validation, "%V", "%P", r"%s", "%S")
        )
