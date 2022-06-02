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
    def __init__(self, icon_path, homepage, source, textpady):
        self.url_homepage = homepage
        self.url_source = source

        self.window = tk.Tk()
        self.window.call('source', routines.resource_path('azure.tcl','resource'))
        self.window.call("set_theme", "light")
        self.window.title('HornPenguin Booklet')

        self.window_width = 404 #px
        self.window_height = 720

        # Tab: basic, Advanced
        self.Tabwindow = ttk.Notebook(self.window)

        self.tab_basic = ttk.Frame(self.Tabwindow)
        self.tab_advance = ttk.Frame(self.Tabwindow)
        
        self.Tabwindow.add(self.tab_basic, text='basic')
        self.Tabwindow.add(self.tab_advance, text='advanced')


        self.initiate_window()

        self.icon_path = icon_path
        self.window.iconbitmap(self.icon_path)
       
        self.menu = tk.Menu(self.window)
        self.menu_help = tk.Menu(self.menu, tearoff=0)
        self.initiate_menu()
        self.window.configure(menu=self.menu)

        #Text pad
        self.text_pady =textpady

        #input_file info

        self.title = tk.StringVar()
        self.author = tk.StringVar()
        self.page_n = tk.IntVar()
        self.page_format = tk.StringVar()
        self.filename = tk.StringVar()

        #Advanced variables
        # Paper size: h x w
        # Page range: []
        # Fold option: Sheet num = n1 x n2 <- ratio modification
        # Imposition option: On, Off
        # Sig Proof: color option
        # Attachement PDF: Cover and back: front, back, none

        self.page_size = {"width": tk.IntVar(), "height": tk.IntVar()}
        self.page_range = tk.StringVar()

        self.sig_n1 = tk.IntVar()
        self.sig_n2 = tk.IntVar()

        self.imposition = tk.BooleanVar()
        self.sig_proof = tk.StringVar()

        self.att_front = tk.BooleanVar()
        self.att_back = tk.BooleanVar()

        


    def initiate_window(self):
        x = int((self.window.winfo_screenwidth() - self.window_width)/2)
        y = int((self.window.winfo_screenheight() - self.window_height)/2)

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
        destorybutton.pack(pady=int(2*tpady))

        if fix:
            sub_window.transient(self.window)
            sub_window.grab_set()
            self.window.wait_window(sub_window)
        return 0

# Popup table routines
#    def popup_window_table(self, width, height, column_names, data, tpadx=10, tpady=2.5, fix=False, align = 'center' , button_text='Ok'):
#        sub_window = tk.Toplevel(self.window)
#        sub_window.title = title
#        sub_window.geometry(f'{width}x{height}')
#        if fix:
#            sub_window.resizable(False,False)
#        else:
#            sub_window.resizable(True,True)
#        
#        table = ttk.Treeview(sub_window)
#        table['column'] = column_names
#
#        for i, x in enumerate(column_names):
#            if i ==0:
#                table.column("#0", width=0, st)
#            else:
#                table.column(x, anchor=CENTER)
#        destroybutton = ttk.Button(sub_window, text=button_text, width = 15, comman=sub_window.destroy)
#        destroybutton.pack(pady=int(2*tpady))
            


    def initiate_menu(self):
        self.menu.add_cascade(label = "Help", menu=self.menu_help)

        about_window = partial(self.popup_window, 400, 220, textdata.about_text, "About HornPenguin Booklet", 10, 2.5, True)
        self.menu_help.add_command(label="About", command=about_window)
        
        format_window = partial(self.popup_window, 300, 300, textdata.format_table, "Paper Format", 30, 2.5, False)
        self.menu_help.add_command(label="Paper Format", command=format_window)

        self.menu_help.add_command(label="Homepage", command=partial(routines.open_url,self.url_homepage))
        self.menu_help.add_command(label="Source", command=partial(routines.open_url,self.url_source))

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
                self.page_format.set(f'{page_size[0]}x{page_size[1]}')
                textdata.PaperFormat["Default"] = f'{page_size[0]}x{page_size[1]}'

                file_name_with_format = os.path.split(str(filename))[1]
                file_name = file_name_with_format.split('.')
                self.filename.set(file_name[0] + '_HPBooklet'+'.'+file_name[1])

                print(f'title:{self.title.get()}\nfile:{filename}')
            else:
                print(f"Not a vaild PDF file: file ({filename})")
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
        
        self.canvas.grid(row=row, column=column)
        return 0

    def inputbox(self, row, column, padx, pady, width, height, relief, padding, entry_width =41):

        self.Frame_input = ttk.Frame(
            master  = self.tab_basic,
            width   = width,
            height  = height,
            relief  = relief,
            padding = padding
        )

        self.input_text = ttk.Label(self.Frame_input, text="Manuscript", justify=tk.LEFT, anchor='w')
        self.input_text.grid(row=0, column=0, sticky = tk.W, padx =3)
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


        self.Frame_input.grid(row=row, column=column, padx=padx, pady=pady)

        return 0

    def outputbox(self,row, column, padx, pady, width, height, relief, padding, entry_width =41):

        self.Frame_output = ttk.Frame(
            master  = self.tab_basic, 
            width   = width, 
            height  = height, 
            relief  = relief, 
            padding = padding
        )


        self.output_text = ttk.Label(self.Frame_output, text="Output", justify=tk.LEFT, anchor='w')
        self.output_text.grid(row=0, column=0, sticky = tk.W, padx =3)
        self.output_entry = ttk.Entry(self.Frame_output, width = entry_width)
        self.output_entry.grid(row=1, column=0, columnspan=3, padx =3, ipadx=5)
        ttk.Button(self.Frame_output, text="...", width = 3, command=partial(self.open_output_directory)).grid(row=1, column = 3)


        self.filename_label = ttk.Label(self.Frame_output, text="File name")
        self.filename_entry = ttk.Entry(self.Frame_output, textvariable=self.filename, width = int(entry_width/2))

        self.text_leaves = ttk.Label(self.Frame_output, text="Leaves", justify=tk.LEFT, anchor='w') 
        self.lvalues = [f"{4*(i+1)}" if (i+1)%2 else f"{4*(i+1)}f" for i in range(0,8)]
        self.leaves = ttk.Combobox(self.Frame_output, value= self.lvalues, state='readonly')
        self.leaves.current(0)
       

        self.text_format = ttk.Label(self.Frame_output, text="Book Format", justify=tk.LEFT, anchor='w') 
        self.format_list = [x for x in textdata.PaperFormat.keys()]
        self.format = ttk.Combobox(self.Frame_output, value= self.format_list, state='readonly')
        self.format.current(0)

        self.text_fold = ttk.Label(self.Frame_output, text="Fold", justify=tk.LEFT, anchor='w') 
        self.foldvalue = tk.IntVar()
        self.fold = Checkbutton(self.Frame_output, variable=self.foldvalue, state= tk.DISABLED)
        self.leaves.bind("<<ComboboxSelected>>", self.fold_enable)

        self.text_riffle = ttk.Label(self.Frame_output, text="Riffling direction", justify=tk.LEFT, anchor='w') 
        self.riffle = ttk.Combobox(self.Frame_output, values=["right", "left"], state='readonly')
        self.riffle.current(0)

        self.filename_label.grid(   row=2 , column=0, pady=self.text_pady)
        self.filename_entry.grid(   row=2 , column=1, pady=self.text_pady)

        self.text_leaves.grid(   row=3, column=0, pady=self.text_pady)
        self.leaves.grid(        row=3, column=1, pady=self.text_pady)
        self.text_format.grid(   row=4, column=0, pady=self.text_pady)
        self.format.grid(        row=4, column=1, pady=self.text_pady)

        self.text_fold.grid(     row=5, column=0, pady=self.text_pady)
        self.fold.grid(          row=5, column=1, pady=self.text_pady)

        self.text_riffle.grid(   row=6, column=0, pady=self.text_pady)
        self.riffle.grid(        row=6, column=1, pady=self.text_pady)


        self.Frame_output.grid(row=row, column=column, padx=padx, pady=pady)
        
    def genbutton(self, row, column, width, height, padding):
        self.Frame_button = ttk.Frame(
            master = self.window,
            width = width,
            height = height,
            borderwidth = 0, 
            padding = padding
        )

        self.Generate_button = ttk.Button(self.Frame_button, text="Generate", width = 25, command=partial(self.gen_button_action))
        self.Generate_button.pack(side=tk.RIGHT, pady=18, anchor="e")

        self.Frame_button.grid(row=row, column=column)
    
    def gen_button_action(self):
        input_file = self.input_entry.get()
        filename = self.filename.get()
        if ".pdf" not in filename:
            filename = filename+".pdf"
        output_path = os.path.join(self.output_entry.get(), filename)
        leaves = int((self.leaves.get()).split('f')[0])
        format = self.format.get() 
        fold = self.foldvalue.get() 
        riffle = True if self.riffle.get() == "right" else False

        print(f'Document:{filename}\n{riffle}')

        status = routines.gen_signature(input_file, output_path, leaves, format, fold, riffle=riffle)

        if status == 0:
            done_text = f'{filename}'
            self.popup_window(250,100,done_text,"popup", align="center", button_text = "Done")

        return 0
    def fold_enable(self, event):
        if 'f' in self.leaves.get():
            self.fold.config(state=tk.NORMAL)
        else:
            self.fold.config(state=tk.DISABLED)


        
if __name__ == "__main__":
    text_pady = 3

    icon_name = 'hp_booklet.ico'
    icon_path = routines.resource_path(icon_name, 'resource')
    
    logo_data_byte = base64.b64decode(logo)
    logo_data = BytesIO(logo_data_byte)
    logo_image = Image.open(logo_data)
    
    logo_height = 150
    logo_width = int(logo_height*1.380952380952381)
    resize_logo = logo_image.resize((logo_width, logo_height), Image.Resampling(1))

    hpbooklet = HP_Booklet(icon_path, homepage= textdata.homepage, source = textdata.git_repository, textpady= text_pady)
    
    logo = ImageTk.PhotoImage(resize_logo, master = hpbooklet.window)
    hpbooklet.logo_display(logo)

    hpbooklet.inputbox( row=1, column=0, padx = 5, pady =10, width = 390, height = 160, relief="solid", padding="4 4 10 10")
    hpbooklet.outputbox(row=2, column=0, padx = 5, pady =10, width = 390, height = 200, relief="solid", padding="4 4 10 10")
    hpbooklet.genbutton(row=3, column=0, width = 390, height = 50, padding="2 2 2 2")

    hpbooklet.window.mainloop()
    