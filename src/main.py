#BSD 3-Clause License
#
#Copyright (c) 2022, HornPenguin Co.
#All rights reserved.
#
#Redistribution and use in source and binary forms, with or without
#modification, are permitted provided that the following conditions are met:
#
#1. Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
#2. Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
#3. Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
#FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
#DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
#CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
#OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.



__author__ = "Hyunseong Kim"
__company__ = "HornPenguin"
__version__ = "0.0.1"
__license__ = "BSD license"

import tkinter as tk
from tkinter import NW, Checkbutton, ttk, filedialog
from tkinter.colorchooser import askcolor
from PIL import Image, ImageTk
from functools import partial
import os

import textdata
from image_data import logo
import base64
from io import BytesIO
#---------------------------------------------------------
import routines


# Tab_advanced
#===========================================================
# Paper size: h x w
# Page range: []
# Fold option: Sheet num = n1 x n2 <- ratio modification
# Imposition option: On, Off
# Sig Proof: color option
# Attachement PDF: Cover and back: front, back, none

# Progress Bar

#UI--------------------------------------------------------------------------------------------
class HP_Booklet:
    def __init__(self, icon_path, homepage, source, tutorial, textpady, fix = False, width = 390, height =780):
        self.url_homepage = homepage
        self.url_source = source
        self.url_tutorial = tutorial

        self.fix = fix
        self.window_width = width
        self.window_height = height

        self.window = tk.Tk()
        self.window.call('source', routines.resource_path('azure.tcl','resource'))
        self.window.call("set_theme", "light")
        self.window.title('HornPenguin Booklet')

        # Tab: basic, Advanced
        self.Tabwindow = ttk.Notebook(self.window)
        self.Tabwindow.grid(row=1, column=0)

        self.tab_basic = ttk.Frame(self.Tabwindow)
        self.tab_advance = ttk.Frame(self.Tabwindow)
        
        self.Tabwindow.add(self.tab_basic, text='basic')
        self.Tabwindow.add(self.tab_advance, text='advanced')


        self.initiate_window()

        self.icon_path = icon_path
        self.window.iconbitmap(self.icon_path)
       
       # Menu setting
       # Help: About, Format, Tutorial, License, Contact, Source, homepage, support

        self.menu = tk.Menu(self.window)
        self.menu_help = tk.Menu(self.menu, tearoff=0)
        self.initiate_menu()
        self.window.configure(menu=self.menu)

        #Text pad
        self.text_pady =textpady

        #input_file info

        self.title = tk.StringVar(value = '')
        self.author = tk.StringVar(value = '')
        self.page_n = tk.IntVar(value = 0)
        self.page_format = tk.StringVar(value = '')
        self.filename = tk.StringVar(value = '')

        self.addBlankpages = tk.IntVar(value = 0)
        self.foldvalue = tk.BooleanVar(value = False)

        #Advanced variables
        # Paper size: h x w
        # Page range: []
        # Fold option: Sheet num = n1 x n2 <- ratio modification
        # Imposition option: On, Off
        # Sig Proof: color option
        # Attachement PDF: Cover and back: front, back, none

        self.pagerange_var = tk.StringVar(value = '')
        self.ns = tk.IntVar(value=0)

        self.custom_width = tk.IntVar(value=0)
        self.custom_height = tk.IntVar(value=0)

        self.customformatbool = tk.BooleanVar(value=False)
        self.impositionbool = tk.BooleanVar(value=False)
        self.splitpersigbool = tk.BooleanVar(value=False)
        self.sig_color = tk.StringVar(value='#729fcf')

        #Printing--------------------------------------------------------

        self.sigproofbool = tk.BooleanVar(value=False)
        self.trimbool = tk.BooleanVar(value=False)
        self.registrationbool = tk.BooleanVar(value=False)
        self.cymkbool = tk.BooleanVar(value=False)

        
    def initiate_window(self):
        self.window.winfo_height
        x = int((self.window.winfo_screenwidth() - self.window.winfo_width())/2)
        y = int((self.window.winfo_screenheight() - self.window.winfo_height())/2)

        if self.fix:
            self.window.geometry(f'{self.window_width}x{self.window_height}+{x}+{y}')
        self.window.resizable(False,True)

        #Stack top of windows arrangement at beginning of program 
        self.window.attributes('-topmost', True)
        self.window.update()
        self.window.attributes('-topmost', False)
    
    def popup_window(self, width, height, text, title, tpadx=10, tpady=2.5, fix=False, align='center', button_text = "Ok"):
        sub_window = tk.Toplevel(self.window)
        sub_window.title(title)
        #sub_window.geometry(f'{width}x{height}')
        sub_window.resizable(False,True)
        sub_window.iconbitmap(self.icon_path)

        text_label = ttk.Label(sub_window, text= text, wraplengt=width -20)
        text_label.configure(anchor=align)
        text_label.pack(padx=tpadx, pady = tpady)

        destorybutton = ttk.Button(sub_window, text=button_text , width=15, comman=sub_window.destroy)
        destorybutton.pack(padx=int(2*tpadx),pady=int(2*tpady))

        if fix:
            sub_window.transient(self.window)
            sub_window.grab_set()
            self.window.wait_window(sub_window)
        return 0

    # Popup table routines
    def popup_window_table(self, width, height, column_names, data, title, tpadx=10, tpady=2.5, fix=False, align = 'center'):
        sub_window = tk.Toplevel(self.window)
        sub_window.title(title)
        sub_window.geometry(f'{width}x{height}')
        if fix:
            sub_window.resizable(True,True)
        else:
            sub_window.resizable(False,False)
        
        sub_window.iconbitmap(self.icon_path)

        table = ttk.Treeview(sub_window, selectmode='browse',height = 36)
        table.pack(fill='both')
        table['column'] = column_names

        table.column("#0", width=0, stretch=tk.NO)
        table.heading("#0", text="", anchor=tk.W)
        #Head and column setting
        for x in column_names: 
            table.column(x, width=100, anchor=align)
            table.heading(x, text=x, anchor=align)
        
        #Data innsert

        for i, d in enumerate(data):
            table.insert(parent = '', index= 'end', iid=i, values=d)

    def initiate_menu(self):
        # Help: About, Format, Tutorial, License, support
        self.menu.add_cascade(label = "Help", menu=self.menu_help)

        about_window = partial(self.popup_window, 400, 220, textdata.about_text, "About", 10, 2.5, False)
        self.menu_help.add_command(label="About", command=about_window)
        
        format_window = partial(self.popup_window_table, 320, 480, textdata.format_head, textdata.format_table, "Paper Format", 30, 2.5, False)
        self.menu_help.add_command(label="Paper Format", command=format_window)

        self.menu_help.add_command(label="Tutorial", command = partial(routines.open_url, self.url_tutorial))
        self.menu_help.add_command(label="Homepage", command = partial(routines.open_url,self.url_homepage))
        self.menu_help.add_command(label="Source", command = partial(routines.open_url,self.url_source))

        license = partial(self.popup_window, 600, 800, textdata.license, "License", 10, 2.5, False)
        self.menu_help.add_command(label="License", command= license)

    def open_file(self):
        filename = filedialog.askopenfilename(
            initialdir= "~", 
            title="Select Manuscript", 
            filetypes= (("PDF", "*.pdf"),)
        )
        if filename != '':
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, filename)

            title, author, page_num, page_size = routines.get_pdf_info(filename)
            if title != False:
                self.title.set(title)
                self.author.set(author)
                self.page_n.set(int(page_num))
                self.pagerange.delete(0,tk.END)
                self.pagerange.insert(0, f"1-{self.page_n.get()}")
                self.page_format.set(f'{page_size[0]}x{page_size[1]}')
                textdata.PaperFormat["Default"] = f'{page_size[0]}x{page_size[1]}'
                self.custom_width.set(page_size[0])
                self.custom_height.set(page_size[1])

                file_name_with_format = os.path.split(str(filename))[1]
                file_name = file_name_with_format.split('.pdf')
                self.filename.set(file_name[0] + '_HPBooklet'+'.pdf')

                print(f'title:{self.title.get()}\nfile:{filename}')
                self.Generate_button.config(state=tk.ACTIVE)
                
            else:
                print(f"Not a vaild PDF file: file ({filename})")
                self.Generate_button.config(state=tk.DISABLED)
        return 0
    def open_output_directory(self):
        directory = filedialog.askdirectory(
            initialdir= "~", 
            title="Select Directory",
        )
        self.output_entry.delete(0, tk.END)
        self.output_entry.insert(0, directory)
        
        return 0
    def logo_display(self, logo, row=0, column=0):
        self.logo = logo
        self.canvas = tk.Canvas(self.window, width = self.window_width, height = 170)
        self.canvas.create_image(self.window_width - 220, 10, anchor=NW, image= self.logo)
        
        self.canvas.grid(row=row, column=column, sticky="e")
        return 0

    # Tab Basic
    def basic_inputbox(self, row, column, padx, pady, width, height, relief, padding, entry_width =41):

        self.Frame_input = ttk.LabelFrame(
            master  = self.tab_basic,
            text    = "Manuscript",
            width   = width,
            height  = height,
            relief  = relief,
            padding = padding
        )

        #self.input_text = ttk.Label(self.Frame_input, text="Manuscript", justify=tk.LEFT, anchor='w')
        #self.input_text.grid(row=0, column=0, sticky = tk.W, padx =3)
        self.input_entry = ttk.Entry(self.Frame_input, width = entry_width)
        self.input_entry.grid(row=1, column=0, columnspan=3, padx =3, ipadx=5)
        ttk.Button(self.Frame_input, text="...", width = 3, command=partial(self.open_file)).grid(row=1, column = 3)


        title_value     = ttk.Label(self.Frame_input,      textvariable=self.title, wraplengt=200)
        author_value    = ttk.Label(self.Frame_input,      textvariable=self.author, wraplengt=200)
        page_n_value    = ttk.Label(self.Frame_input,      textvariable=self.page_n, wraplengt=200)
        page_for_value  = ttk.Label(self.Frame_input,      textvariable=self.page_format, wraplengt=200)

        title_label     = ttk.Label(self.Frame_input, text=f"Title")
        author_label    = ttk.Label(self.Frame_input, text=f"Author(s)")
        page_n_label    = ttk.Label(self.Frame_input, text=f"Pages")
        page_for_label  = ttk.Label(self.Frame_input, text=f"Format")

        
        title_label.grid(row=2, column = 0,  pady=self.text_pady)
        author_label.grid(row=3, column = 0,  pady=self.text_pady)
        page_n_label.grid(row=4, column = 0,  pady=self.text_pady)
        page_for_label.grid(row=5, column = 0,  pady=self.text_pady)

        title_value.grid(row=2, column = 1, pady=self.text_pady)
        author_value.grid(row=3, column = 1, pady=self.text_pady)
        page_n_value.grid(row=4, column = 1, pady=self.text_pady)
        page_for_value.grid(row=5, column = 1, pady=self.text_pady)


        self.Frame_input.grid(row=row, column=column, padx=padx, pady=pady, sticky="nsew")

        return 0

    def basic_outputbox(self,row, column, padx, pady, width, height, relief, padding, entry_width =41):

        self.Frame_output = ttk.LabelFrame(
            master  = self.tab_basic, 
            text    = "Output",
            width   = width, 
            height  = height, 
            relief  = relief, 
            padding = padding
        )


        #self.output_text = ttk.Label(self.Frame_output, text="Output", justify=tk.LEFT, anchor='w')
        #self.output_text.grid(row=0, column=0, sticky = tk.W, padx =3)
        self.output_entry = ttk.Entry(self.Frame_output, width = entry_width)
        self.output_entry.grid(row=1, column=0, columnspan=3, padx =3, ipadx=5)
        ttk.Button(self.Frame_output, text="...", width = 3, command=partial(self.open_output_directory)).grid(row=1, column = 3)


        self.filename_label = ttk.Label(self.Frame_output, text="File name")
        self.filename_entry = ttk.Entry(self.Frame_output, textvariable=self.filename, width = int(entry_width/2))

        self.text_leaves = ttk.Label(self.Frame_output, text="Leaves", justify=tk.LEFT, anchor='w') 
        self.lvalues = [f"{4*(i+1)}" if (i+1)%2 else f"{4*(i+1)}f" for i in range(0,8)] + ["1"]
        self.leaves = ttk.Combobox(self.Frame_output, value= self.lvalues, state='readonly')
        self.leaves.current(0)
        self.addblankpages_label = ttk.Label(self.Frame_output, textvariable=self.addBlankpages)
       

        self.text_format = ttk.Label(self.Frame_output, text="Book Format", justify=tk.LEFT, anchor='w') 
        self.format_list = [x for x in textdata.PaperFormat.keys()]
        self.format = ttk.Combobox(self.Frame_output, value= self.format_list, state='readonly')
        self.format.current(0)
        self.format.bind("<<ComboboxSelected>>", self.set_format_values)

        self.text_fold = ttk.Label(self.Frame_output, text="Fold", justify=tk.LEFT, anchor='w') 
        self.fold = ttk.Checkbutton(self.Frame_output, variable=self.foldvalue, state= tk.DISABLED)
        self.leaves.bind("<<ComboboxSelected>>", self.fold_enable)

        self.text_riffle = ttk.Label(self.Frame_output, text="Riffling direction", justify=tk.LEFT, anchor='w') 
        self.riffle = ttk.Combobox(self.Frame_output, values=["right", "left"], state='readonly')
        self.riffle.current(0)

        self.filename_label.grid(   row=2 , column=0, pady=self.text_pady)
        self.filename_entry.grid(   row=2 , column=1, pady=self.text_pady)

        self.text_leaves.grid(   row=3, column=0, pady=self.text_pady)
        self.leaves.grid(        row=3, column=1, pady=self.text_pady)
        self.addblankpages_label.grid(row=3, column=2, pady=self.text_pady)

        self.text_format.grid(   row=4, column=0, pady=self.text_pady)
        self.format.grid(        row=4, column=1, pady=self.text_pady)

        self.text_fold.grid(     row=5, column=0, pady=self.text_pady)
        self.fold.grid(          row=5, column=1, pady=self.text_pady)

        self.text_riffle.grid(   row=6, column=0, pady=self.text_pady)
        self.riffle.grid(        row=6, column=1, pady=self.text_pady)


        self.Frame_output.grid(row=row, column=column, padx=padx, pady=pady, sticky="we")
    
    # Tab Advanced
    def advanced_imposition(self, icons:dict, row, column, padx, pady, width, height, relief, padding, entry_width =41):
        
        self.Frame_ad_imposition =ttk.LabelFrame(
            master  = self.tab_advance, 
            text    = "Sheet Work",
            width   = width, 
            height  = height, 
            relief  = relief, 
            padding = padding
        )
        imposition_icon = ImageTk.PhotoImage(icons["imposition"], master=self.Frame_ad_imposition)
        split_icon = ImageTk.PhotoImage(icons["split"], master=self.Frame_ad_imposition)

        #self.FrameText_impositon = ttk.Label(self.Frame_ad_imposition, text="Sheet work setting",justify=tk.LEFT, anchor='w')

        self.blankpage_label = ttk.Label(self.Frame_ad_imposition, text = "Blank page(s)",justify=tk.LEFT, anchor='w')
        self.bp_modes = ["back", "front", "both"]
        self.blankpage = ttk.Combobox(self.Frame_ad_imposition, value = self.bp_modes, state='readonly')
        self.blankpage.current(0)
        self.blankpage_label2 = ttk.Label(self.Frame_ad_imposition, text = "back > front \nfor odd in \'both\' mode",justify=tk.LEFT, anchor='w')

        self.pagerange_label = ttk.Label(self.Frame_ad_imposition, text="Page range",justify=tk.LEFT, anchor='w')
        self.pagerange = ttk.Entry(self.Frame_ad_imposition, textvariable=self.pagerange_var, width = int(entry_width/2))
        self.pagerange_example = ttk.Label(self.Frame_ad_imposition, text="1, 3-5, 10",justify=tk.LEFT, anchor='w') 

        self.foldcomposition_label = ttk.Label(self.Frame_ad_imposition, text="Fold composition",justify=tk.LEFT, anchor='w')
        self.foldcomposition_nn_combo = ttk.Combobox(self.Frame_ad_imposition)
        #self.foldcomposition_nn_combo.current(0)
        self.foldcomposition_ns_label = ttk.Label(self.Frame_ad_imposition, text=self.ns)
        self.foldcomposition_example = ttk.Label(self.Frame_ad_imposition, text="nn x ns",justify=tk.LEFT, anchor='w')

        self.customformat_label = ttk.Label(self.Frame_ad_imposition, text="Custom format",justify=tk.LEFT, anchor='w')
        self.customformat_width_entry = ttk.Entry(self.Frame_ad_imposition, textvariable = self.custom_width, width = int(entry_width/8))
        self.customformat_times = ttk.Label(self.Frame_ad_imposition, text="x",justify=tk.LEFT, anchor='w')
        self.customformat_height_entry = ttk.Entry(self.Frame_ad_imposition, textvariable = self.custom_height, width = int(entry_width/8))
        self.customformat_check = ttk.Checkbutton(self.Frame_ad_imposition, variable = self.customformatbool, command=self.customformat_entry_enable_f)
        self.customformat_example = ttk.Label(self.Frame_ad_imposition, text="(mm)x(mm)",justify=tk.LEFT, anchor='w')
        self.customformat_width_entry.config(state=tk.DISABLED)
        self.customformat_height_entry.config(state=tk.DISABLED)


        self.imposition_label = ttk.Label(self.Frame_ad_imposition, text="Imposition",justify=tk.LEFT, anchor='w')
        self.imposition = ttk.Checkbutton(self.Frame_ad_imposition, variable=self.impositionbool)
        self.imposition_icon = ttk.Label(self.Frame_ad_imposition, image= imposition_icon)
        self.imposition_icon.photo = imposition_icon

        self.splitpersig_label = ttk.Label(self.Frame_ad_imposition, text="Split per sig",justify=tk.LEFT, anchor='w')
        self.splitpersig = ttk.Checkbutton(self.Frame_ad_imposition, variable=self.splitpersigbool)
        self.splitpersig_icon = ttk.Label(self.Frame_ad_imposition)
        self.splitpersig_icon.config(image= split_icon)
        self.splitpersig_icon.photo = split_icon

        #Grid
        #self.FrameText_impositon.grid(row=0, column=0, pady=2*self.text_pady)

        self.blankpage_label.grid(          row=1, column=0, pady=self.text_pady)
        self.blankpage.grid(                row=1, column=1, columnspan=4, pady=self.text_pady)
        self.blankpage_label2.grid(         row=1, column=5, columnspan=2, ipadx = self.text_pady, pady=self.text_pady)

        self.pagerange_label.grid(          row=2, column = 0, pady=self.text_pady)
        self.pagerange.grid(                row=2, column = 1, columnspan=4, pady=self.text_pady)
        self.pagerange_example.grid(        row=2, column = 5, columnspan=2, pady=self.text_pady)

        self.customformat_label.grid(       row=3, column=0, pady=self.text_pady)
        self.customformat_check.grid(       row=3, column=1, pady=self.text_pady)
        self.customformat_width_entry.grid( row=3 ,column=2, pady=self.text_pady)
        self.customformat_times.grid(       row=3 ,column=3, pady=self.text_pady)
        self.customformat_height_entry.grid(row=3, column=4, pady=self.text_pady)
        self.customformat_example.grid(     row=3, column=5, columnspan=2, pady=self.text_pady)

        self.imposition_label.grid(         row=4, column = 0, pady=self.text_pady)
        self.imposition.grid(               row=4, column=1, columnspan=4, pady=self.text_pady)
        self.imposition_icon.grid(          row=4, column=5, columnspan=2, pady=self.text_pady)

        self.splitpersig_label.grid(        row=5, column = 0, pady=self.text_pady)
        self.splitpersig.grid(              row= 5, column=1, columnspan=4, pady=self.text_pady)
        self.splitpersig_icon.grid(         row=5, column=5, columnspan=2, pady= self.text_pady)

        self.Frame_ad_imposition.grid(row=row, column=column,ipadx =padx, padx=(4*padx,4*padx), pady=pady, sticky="ns")
    
    def advanced_printing(self, icons:dict, row, column, padx, pady, width, height, relief, padding, entry_width =41):
        self.Frame_ad_printing =ttk.LabelFrame(
            master  = self.tab_advance, 
            text    = "Printing",
            width   = width, 
            height  = height, 
            relief  = relief, 
            padding = padding
        )

        #Imagesetting
        sigproof_icon = ImageTk.PhotoImage(icons["proof"], master=self.Frame_ad_printing)
        trim_icon = ImageTk.PhotoImage(icons["trim"], master=self.Frame_ad_printing)
        registration_icon =  ImageTk.PhotoImage(icons["registration"], master=self.Frame_ad_printing)
        cmyk_icon = ImageTk.PhotoImage(icons["cmyk"], master=self.Frame_ad_printing)

        self.sigproof_label = ttk.Label(self.Frame_ad_printing, text="Signature proof", justify=tk.LEFT, anchor="w")
        self.sigproof_checkbox = ttk.Checkbutton(self.Frame_ad_printing, variable=self.sigproofbool)
        self.sigproof_button = tk.Button(self.Frame_ad_printing, width=3 , height =1 , text='  ', bg=self.sig_color.get(), command=self.sig_color_set)
        self.sigproof_icon = ttk.Label(self.Frame_ad_printing, image=sigproof_icon)
        self.sigproof_icon.photo = sigproof_icon

        self.trim_label = ttk.Label(self.Frame_ad_printing, text="Trim", justify=tk.LEFT, anchor="w")
        self.trim_checkbox = ttk.Checkbutton(self.Frame_ad_printing, variable=self.trimbool)
        self.trim_icon = ttk.Label(self.Frame_ad_printing, image= trim_icon)
        self.trim_icon.photo = trim_icon

        self.registration_label = ttk.Label(self.Frame_ad_printing, text="Registration", justify=tk.LEFT, anchor="w")
        self.registration_checkbox = ttk.Checkbutton(self.Frame_ad_printing, variable=self.registrationbool)
        self.registration_icon = ttk.Label(self.Frame_ad_printing, image=registration_icon)
        self.registration_icon.photo = registration_icon

        self.cmyk_label = ttk.Label(self.Frame_ad_printing, text="CYMK(mark)", justify=tk.LEFT, anchor="w")
        self.cmyk_checkbox = ttk.Checkbutton(self.Frame_ad_printing, variable=self.cymkbool)
        self.cmyk_icon = ttk.Label(self.Frame_ad_printing, image=cmyk_icon)
        self.cmyk_icon.photo = cmyk_icon


        self.sigproof_label.grid(   row=0, column=0, pady=self.text_pady)
        self.sigproof_checkbox.grid(row=0, column=1, columnspan=2, pady=self.text_pady)
        self.sigproof_button.grid(  row=0, column=3,  padx =self.text_pady*6, pady=self.text_pady*6, sticky = 'n')
        self.sigproof_icon.grid(    row=0, column=4, pady=self.text_pady)

        self.trim_label.grid(       row=1, column= 0, pady=self.text_pady)
        self.trim_checkbox.grid(    row=1, column= 1, columnspan =2, pady=self.text_pady)
        self.trim_icon.grid(        row=1, column= 3,  columnspan =4, pady=self.text_pady)

        self.registration_label.grid(   row=2, column= 0, pady=self.text_pady)
        self.registration_checkbox.grid(row=2, column= 1,columnspan =2,  pady=self.text_pady)
        self.registration_icon.grid(    row=2, column= 3,  columnspan =4,  pady=self.text_pady)

        self.cmyk_label.grid(           row=3, column= 0, pady=self.text_pady)
        self.cmyk_checkbox.grid(        row=3, column= 1, columnspan =2, pady=self.text_pady)
        self.cmyk_icon.grid(            row=3, column= 3, columnspan =4, pady=self.text_pady)

        self.Frame_ad_printing.grid(row=row, column=column, ipadx =padx,  padx=(2*padx,2*padx), pady=pady, sticky="ns")


    def fold_enable(self, event):
        if 'f' in self.leaves.get():
            self.fold.config(state=tk.NORMAL)
        else:
            self.fold.config(variable=False, state=tk.DISABLED)

    def customformat_entry_enable_f(self):
        if self.customformatbool.get():
            self.customformat_width_entry.config(state=tk.ACTIVE)
            self.customformat_height_entry.config(state=tk.ACTIVE)
        else:
            self.customformat_width_entry.config(state=tk.DISABLED)
            self.customformat_height_entry.config(state=tk.DISABLED)


    def sig_color_set(self, event):
        color = askcolor()
        if color != None:
             self.sig_color = color[1]
             self.sigproof_button.configure(bg=color[1])
             return 0
        return 1

    def set_format_values(self, event):
        formatname = self.format.get()
        if formatname =="Default":
            return 1
        else:
            width, height = textdata.PaperFormat[formatname].split("x")

            self.custom_width.set(width)
            self.custom_height.set(height)

            return 0


    def genbutton(self, row, column, width, height, padding, columnspan=1):
        self.Frame_button = ttk.Frame(
            master = self.window,
            width = width,
            height = height,
            borderwidth = 0, 
            padding = padding
        )

        self.Generate_button = ttk.Button(self.Frame_button, text="Generate", width = 25, command=partial(self.gen_button_action))
        self.Generate_button.pack(side=tk.RIGHT, pady=18, anchor="e")
        self.Generate_button.config(state=tk.DISABLED)

        self.Frame_button.grid(row=row, column=column, columnspan= columnspan)
    
    #Pass to parameters to PDF routine
    def gen_button_action(self):
        

        input_file = self.input_entry.get()
        
        filename = self.filename.get()
        if ".pdf" not in filename:
            filename = filename+".pdf"
        
        output_path = os.path.join(self.output_entry.get(), filename)
        
        #Leaves and sub signature---------------------------------------------------------------
        leaves = (self.leaves.get()).split('f')
        nl = int(leaves[0])
        nn = self.nn.get()
        ns = self.ns.get()

        #Format----------------------------------------------------------------------------------
        formatbool = False
        format_width = 0.0
        format_height = 0.0
        if self.custom_format.get():
            formatbool = True
            format_width = self.custom_format_width.get()
            format_height = self.custom_format_height.get()
        else:
            formatname = self.format.get()
            if formatname == "Default":
                formatbool = False
            else:
                formatbool = True
                wh = textdata.PaperFromat[formatname].split('x')
                format_width = int(wh[0])
                format_height = int(wh[1])
        #Fold----------------------------------------------------------------------------------
        foldbool = (len(leaves) == 2)  and self.fold.get() 
        fold = self.foldvalue.get()

        #Riffle direction----------------------------------------------------------------------
        rifflebool = True if self.riffle.get() == "right" else False
        #Imposition----------------------------------------------------------------------------
        impositionbool = self.imposition.get()
        #Split---------------------------------------------------------------------------------
        splitbool = self.split.get()
        #Signature Proof-----------------------------------------------------------------------
        sigproofbool = self.sigproof.get()
        #sig_color = hex
        #Trim Mark-----------------------------------------------------------------------------
        trimbool = self.trim.get()
        #Registration Mark---------------------------------------------------------------------
        registrationbool = self.registration.get()
        #CYMK Mark-----------------------------------------------------------------------------
        cymkbool = self.cymk.get()

        

        print(f'Document:{filename}\n signature leaves: {nl} \n direction: {self.riffle.get()}')

        status = routines.gen_signature(
            input_file, 
            output_path,
            leaves = [nl, nn, ns], 
            fold = fold, 
            riffle = rifflebool,
            format = [formatbool, format_width , format_height],
            imposition = impositionbool,
            split = splitbool,
            sigproof = [sigproofbool, sig_color],
            trim = trimbool,
            registration = registrationbool,
            cymk = cymkbool
            )

        if status == 0:
            done_text = f'{filename} is done'
            self.popup_window(250,100, done_text, "Done", align="center", button_text = "Ok")
        else:
            self.popup_window(250, 100, routines.status_code[status], "Error", align = "center", button_text= "Ok")
        return 0




        
if __name__ == "__main__":
    text_pady = 3

    icon_name = 'hp_booklet.ico'
    icon_path = routines.resource_path(icon_name, 'resource')

    #resources image names
    imposition_icon_names = [
        "imposition",
        "split"
    ]
    printing_icon_names = [
        "proof",
        "cmyk",
        "registration",
        "trim"
    ]
    
    logo_data_byte = base64.b64decode(logo)
    logo_data = BytesIO(logo_data_byte)
    logo_image = Image.open(logo_data)
    
    logo_height = 150
    logo_width = int(logo_height*1.380952380952381)
    resize_logo = logo_image.resize((logo_width, logo_height), Image.Resampling(1))

    hpbooklet = HP_Booklet(
        icon_path, 
        homepage= textdata.homepage, 
        source = textdata.git_repository, 
        tutorial = textdata.git_repository, 
        textpady= text_pady
    )
    
    logo = ImageTk.PhotoImage(resize_logo, master = hpbooklet.window)
    hpbooklet.logo_display(logo)
    hpbooklet.basic_inputbox( row=1, column=0, padx = 5, pady =10, width = 370, height = 160, relief="solid", padding="4 4 10 10")
    hpbooklet.basic_outputbox( row=1, column=1, padx = 5, pady =10, width = 370, height = 200, relief="solid", padding="4 4 10 10")

    imposition_iconpaths =  { name: routines.resource_path(f"{name}.png", 'resource') for name in imposition_icon_names}
    imposition_icons = { name: Image.open(imposition_iconpaths[name]) for name in imposition_icon_names}

    hpbooklet.advanced_imposition(imposition_icons, row= 1, column=0, padx = 5, pady= 10, width = 450, height = 220, relief = "solid", padding="4 4 10 10")
    
    printing_iconpaths =  { name: routines.resource_path(f"{name}.png", 'resource') for name in printing_icon_names}
    printing_icons = { name: Image.open(printing_iconpaths[name]) for name in printing_icon_names}
    hpbooklet.advanced_printing(printing_icons, row= 1, column=1, padx = 5, pady= 10, width = 450, height = 140, relief = "solid", padding="4 4 10 10")
    
    hpbooklet.genbutton(row=2, column=0, columnspan =2 ,width = 370, height = 50, padding="2 2 2 2")

    hpbooklet.window.mainloop()
    