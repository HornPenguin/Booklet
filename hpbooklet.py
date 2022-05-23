
__author__ = "Hyunseong Kim"
__version__ = "1.0.0"
__license__ = "BSD license"

import tkinter as tk
from tkinter import NW, Checkbutton, ttk, filedialog
import webbrowser
import PyPDF2 as pypdf
import TKinterModernThemes as TKMT
from PIL import Image, ImageTk
from functools import partial
import os


git_repository = r"https://github.com/HornPenguin/Booklet"
homepage = r"https://www.hornpenguin.com/"
about_text= r'''
Copyright (c) 2022 Kim, Hyunseong
All right reserved.

This program is using PyPDF2 library which is ditributed under
BSD-3 license.
See details of license in LICENSE file in repository.
'''

PaperFormat = {
    "A4": "210x297",
    "A5": "148x210",
    "B5": "176x250",
    "B6": "125x176",
    "JIS B5": "182x257",
    "JIS B6": "128x182",
    "Letter" : "216x279",
    "Legal" : "215x275"
}

#Routines--------------------------------------------------------------------------------

class routines:
    def __init__(self):
        pass
    
    @classmethod
    def get_pdf_info(cls, pdf_path):
        pdf = (pypdf.PdfFileReader(pdf_path))
        pdfinfo = pdf.documentInfo


        title = pdfinfo['/Title'] if '/Title' in pdfinfo.keys() else ''
        authors = pdfinfo['/Author'] if '/Author' in pdfinfo.keys() else ''
        page_num = int(pdf.getNumPages())
        page_format = pdf.pageLayout
        return title, authors, page_num, page_format

    @classmethod
    def open_url(cls, url):
        return webbrowser.open(url)
    @classmethod
    def sig_permutation(cls, n , direction=True):
        if direction: #right
            per = [n,1]
            for i in range(1, int(n/2)):
                per.extend([1+i, n-i])
        else:
            per = [1, n]
            for i in range(1, int(n/2)):
                per.extend([n-i, 1+i])
        return per
    @classmethod
    def gen_signature(cls, input_file, output_file, leaves, format, fold, riffle = True):

        pdf = pypdf.PdfFileReader(input_file)
        page_n = pdf.getNumPages()
        per_n = cls.sig_permutation(leaves, riffle)

        re_n = int(page_n / leaves)

        pdf_sig = pypdf.PdfFileWriter()

        if riffle:
            for i in range(0, re_n):
                for j in range(0, leaves):
                    l  =  leaves* i + per_n[j] -1
                    if l >= page_n:
                        pdf_sig.addBlankPage()
                    else:
                        pdf_sig.addPage(pdf.pages[l])
        else:
            pass
        
        output = open(output_file, "wb")
        pdf_sig.write(output)
        output.close()

        return 0


#UI--------------------------------------------------------------------------------------------
class HP_Booklet:
    def __init__(self, icon_path, homepage, source, textpady):
        self.url_homepage = homepage
        self.url_source = source

        self.window =  TKMT.ThemedTKinterFrame("HornPenguin Booklet","azure","light").root
        self.window.title('HornPenguin Booklet')

        self.window_width = 404 #px
        self.window_height = 720

        self.initiate_window()

        self.window.iconbitmap(icon_path)

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


    def initiate_window(self):
        x = int((self.window.winfo_screenwidth() - self.window_width)/2)
        y = int((self.window.winfo_screenheight() - self.window_height)/2)

        self.window.geometry(f'{self.window_width}x{self.window_height}+{x}+{y}')
        self.window.resizable(False,True)

        #Stack top of windows arrangement at beginning of program 
        self.window.attributes('-topmost', True)
        self.window.update()
        self.window.attributes('-topmost', False)
    
    def about_window(self, text):
        sub_window = tk.Toplevel(self.window)
        sub_window.title("About Horn Penguin Booklet")
        sub_window.geometry(f'400x250')
        sub_window.resizable(False, True)
        sub_window.iconbitmap('./images/HornPengunPavicon.ico')


        version = ttk.Label(sub_window, text = f"Version. {__version__}")
        version.pack(pady=10)
        copytext = ttk.Label(sub_window, text=text, justify=tk.LEFT)
        copytext.pack(padx=10, pady=2.5)

        destorybutton = ttk.Button(sub_window, text="OK", width=15, comman=sub_window.destroy)
        destorybutton.pack(pady=5)

        sub_window.transient(self.window)
        sub_window.grab_set()
        self.window.wait_window(sub_window)
        return 0


    def initiate_menu(self):
        self.menu.add_cascade(label = "Help", menu=self.menu_help)
        self.menu_help.add_command(label="About", command=partial(self.about_window, about_text))
        self.menu_help.add_command(label="Homepage", command=partial(routines.open_url,self.url_homepage))
        self.menu_help.add_command(label="Source", command=partial(routines.open_url,self.url_source))

    def open_file(self):
        filename = filedialog.askopenfilename(
            initialdir= "~", 
            title="Select Manuscript", 
            filetypes= (("PDF", "*.pdf"),)
        )

        self.input_entry.delete(0, tk.END)
        self.input_entry.insert(0, filename)
        title, author, page_num, page_format = routines.get_pdf_info(filename)

        self.title.set(title)
        self.author.set(author)
        self.page_n.set(int(page_num))
        self.page_format.set(page_format)

        file_name = os.path.split(str(filename))[1]
        self.filename.set(file_name)

        print(self.title.get())
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

    def inputbox(self,row, column, padx, pady, width, height, relief, padding, entry_width =41):

        self.Frame_input = ttk.Frame(
            master  = self.window,
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
            master  = self.window, 
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
        self.format_list = [x for x in PaperFormat.keys()]
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

        self.Generate_button = ttk.Button(self.Frame_button, text="Generate", width = 25, command=partial(self.button_action))
        self.Generate_button.pack(side=tk.RIGHT, pady=18, anchor="e")

        self.Frame_button.grid(row=row, column=column)
    
    def button_action(self):
        input_file = self.input_entry.get()
        filename = self.filename.get()
        if ".pdf" not in filename:
            filename = filename+".pdf"
        output_path = os.path.join(self.output_entry.get(), filename)
        leaves = int((self.leaves.get()).split('f')[0])
        format = self.format.get() 
        fold = self.foldvalue.get() 
        riffle = True if self.riffle.get() == "right" else False

        routines.gen_signature(input_file, output_path, leaves, format, fold, riffle)

        return 0
    def fold_enable(self, event):
        if 'f' in self.leaves.get():
            self.fold.config(state=tk.NORMAL)
        else:
            self.fold.config(state=tk.DISABLED)




        




if __name__ == "__main__":
    text_pady = 3

    icon_path = 'images/HornPengunPavicon.ico'
    logo_path = 'images/HP_Booklet.png'
    logo_img = (Image.open(logo_path))
    logo_height = 150
    logo_width = int(logo_height*1.380952380952381)
    resize_logo = logo_img.resize((logo_width, logo_height), Image.ANTIALIAS)

    hpbooklet = HP_Booklet(icon_path=icon_path, homepage= homepage, source = git_repository, textpady= text_pady)
    
    logo = ImageTk.PhotoImage(resize_logo, master = hpbooklet.window)
    hpbooklet.logo_display(logo)

    hpbooklet.inputbox(     row=1, column=0, padx = 5, pady =10, width = 390, height = 160, relief="solid", padding="4 4 10 10")
    hpbooklet.outputbox(    row=2, column=0, padx = 5, pady =10, width = 390, height = 200, relief="solid", padding="4 4 10 10")
    hpbooklet.genbutton(    row=3, column=0, width = 390, height = 50, padding="2 2 2 2")

    hpbooklet.window.mainloop()
    