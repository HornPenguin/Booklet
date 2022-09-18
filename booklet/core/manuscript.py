# Copyright (c) 2022, Hyunseong Kim <qwqwhsnote@gm.gist.ac.kr>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# Python standard 
import io, tempfile
from datetime import datetime
from pathlib import Path
import sys, os
sys.path.insert(1, os.getcwd()) 
sys.path.append("..")

# Type hint
from io import BytesIO, FileIO
from typing import Union, Tuple, NoReturn, Callable
from tempfile import _TemporaryFileWrapper as TempFile
from types import FunctionType
from numbers import Number 

# PDF
import PyPDF2 as pypdf

# Project modules
from booklet.utils.misc import *
from booklet.utils import validation

class Modifier:
    __type__ = "modifier" # 0
    __external_file__:bool = False #1
    __job__ = "" # 2nd
    __name__ = "" # name and description are for 2nd deep class 
    __desciprtion__ = ""

    def __init__(self, *args, **kwargs): 
        """:code:`kwargs` are additional arguments for the inside 'do' function.
           Example:
           Next function can be converted to `Modifier` class 
            `example(cls, a, b, c)` 
           as
            example = Modifier(a, b, c)
            example.do()
        """
        self.args = args
        self.kwargs = kwargs
    def file_requirement(self, on:bool = False):
        self.__external_file__ = on if type(on) == bool else False
    def get_new_pdf(self, index, manuscript, filemode="safe"):
        if filemode == "safe":
            new_file = NamedTempFile.from_temp_setting(
                mode= "wb+",
                prefix=f"{index}_{self.__name__}_", 
                suffix=".pdf", 
                dir=manuscript.tem_directory.name,
                delete=False
            )
        else:
            new_file = io.BytesIO()
        new_pdf = pypdf.PdfFileWriter()
        return new_pdf, new_file
    def kwargs_check(self):
        pass
    def do(self, index, cls):
        pass
class Converter(Modifier): 
    __type__ = "converter"
    # Using internal routines only
    __external_file__ = False
    @property
    def type(self):
        return Converter.__type__
class Template(Modifier):
    __type__ = "template"
    __external_file__ = True
    @property
    def type(self):
        return Template.__type__
    # Requiring additional file
    def __init__(
        self, 
        file:Union[None, str, io.BytesIO, io.FileIO, TempFile]=None,
        direction:bool=True, # True: manuscript to template e.g: Imposition, False: Template to Manuscript
        rule:Union[ None, Callable]= None,
        position:Union[ None, Callable]= None
    ):
        if file != None:
            self.file = file if type(file)  != str else self.__get_path(file, mode='f')
            self.pdf = pypdf.PdfFileReader(file)
            page = self.pdf.getPage(0)
            self.paper_format = (
                float(page.mediaBox.width),
                float(page.mediaBox.height)
                )
            self.pdf_origin = (page.mediabox[0], page.mediabox[1])
        self.direction = direction
        self.custom_rule = rule
        self.custom_position = position

    @classmethod
    def from_generator(cls, direction, generator:Callable, *args, **kwargs):
        file, rule, position = generator(*args, **kwargs)
        return cls(file, direction, rule, position)

    # Internal routines   
    def __validate_page_num(self, cls, page_num, range=None):
        if not validation.check_integer(page_num):
            #print(page_num)
            #print(type(page_num))
            raise ValueError("Invalid value it must be integer")
        if self.direction: # manuscript to template
            ran = len(self.pdf.pages) if range == None else range
            if page_num > ran:
                raise ValueError(f"Exceed total page range. {page_num}>{len(self.pdf.pages)}")
        if page_num > cls.file_pages: # template to manuscript
            raise ValueError(f"Exceed total page range. {page_num}>{len(cls.page_range)}")
    # Define below two method in child class
    # def rule(self, x): 
    #     pass
    # def position(self, x):
    #     pass
    # Basic routines
    def index_mapping(self, cls, pagenum:int, range=None) -> list: #number of page in manuscript 
        self.__validate_page_num(cls, pagenum, range)
        return self.rule(pagenum) if self.custom_rule == None else self.custom_rule(pagenum)
    def position_mapping(self, cls, pagenum:int, range=None) -> Tuple[float, float]:
        self.__validate_page_num(cls, pagenum, range)
        return self.position(pagenum) if self.custom_position == None else self.custom_position(pagenum)

#--------------------------------------------------
       
class Manuscript:
    @property
    def pages(self) -> list[pypdf.PageObject]:
        pages = []
        for i in range(0, len(self.page_range)):
            page_num = self.page_range[i]-1
            pages.append(self.pdf.pages[page_num])
        return pages
    @property
    def modifier_infos(self) -> dict:
        info = []
        for modifier in self.modifiers:
            info.append(
                {
                    modifier.name: {
                        "type": modifier.type, 
                        "description":modifier.description
                        }
                })
        return info
    def __del__(self, *args):
        try: 
            self.file.close()
            del(self.file)
        except:
            pass  
    def __init__(
        self, 
        input:Union[str, Path, BytesIO, FileIO], 
        output:Union[str, Path], 
        filename:Union[None, str, Tuple[bool, bool, str]] = None,
        page_range:Union[None, int, str, list]= None, 
        ):

        self.tem_directory = tempfile.TemporaryDirectory()
        self.temp_manu = None #Use for temporary manuscript in update process
        self.file_path = self.__get_path(input, mode='f')
        self.file_name = self.file_path.stem
        self.file_format = self.file_path.suffix
        self.pdf = pypdf.PdfFileReader(self.file_path)
        self.meta = {}
        for key in self.pdf.metadata.keys():
            val = self.pdf.metadata.raw_get(key)
            self.meta[key] = str(val)

        self.file_pages, self.file_paper_format = self.__get_file_info(self.file_path)
        self.pdf_origin = (self.pdf.pages[0].mediabox[0], self.pdf.pages[0].mediabox[1])

        self.page_range = self.__get_page_range(page_range)

        self.output_path = self.__get_path(output,mode='d')
        self.basic_output_file_name = self.file_name + "_HP_BOOKLET"

        if filename != None and len(filename) ==3:
            use_as_name = filename[0]
            use_as_suffix = filename[1]
            string = filename[2]
            if use_as_name:
                self.basic_output_file_name = string
            # suffix    
            elif use_as_suffix:
                self.basic_output_file_name = self.file_name + string
            else:
                self.basic_output_file_name = string + self.file_name
        elif type(filename) == str:
            if "." in filename:
                name, file_format = filename.split(".")
            else:
                name = filename
            self.basic_output_file_name = name
        self.modifiers = []
        self.modifier_index = 0
    
    # Internal routines
    def __get_path(self, _path:Union[str, Path, BytesIO], mode='f') -> Path:
        if isinstance(_path, BytesIO):
            return None
        if type(_path) == str:
            _path = Path(_path)
        validation.path(_path, mode)
        return _path
    def __get_page_range(self, page_range:Union[None, str, int]) -> list[int]:
        if page_range == None:
            return list(range(1, self.file_pages+1))
        if type(page_range) == int:
            if page_range >0 and page_range<self.file_pages:
                pages = [page_range]
            else:
                raise ValueError(f"Given pages, {page_range}, exceed file page range, {self.file_pages}.")
        if type(page_range) == str:
            page_range = page_range.replace(" ", "")
            pages = []
            for st in page_range.split(","):
                if "-" in st:
                    i, l = st.split("-")
                    i = int(i)
                    l = int(l)
                    r = l-i +1
                    pages += [i + d for d in range(0,r)]
                elif validation.check_integer(st, positive = True):
                    pages.append(int(st))
        return pages 
    def __get_file_info(self, path:Union[str, Path, io.BytesIO, TempFile]) -> Tuple[int, Tuple[Number, Number]]:
        """Extract basic pdf info from the given file path.
        """
        pdf = pypdf.PdfFileReader(path)
        page_num = len(pdf.pages)
        paper_format = (
            float(pdf.getPage(0).mediaBox.width),
            float(pdf.getPage(0).mediaBox.height)
        )
        return page_num, paper_format
    def __vaildate_index(self, i:int, li:list):
        if i >= len(li):
            raise ValueError(f"Exceed iterable index, {i} >= {len(li)}")
    
    # Modifier list routines
    def modifier_order_reverse(self)-> NoReturn:
        self.modifiers.reverse()
    def modifier_order_change(self, i:int, j:int)-> NoReturn: # from i to j
        if not (validation.check_integer(i, True) and validation.check_integer(j, True)):
            raise ValueError(f"Invaild index value, {i} {j}")
        self.__vaildate_index(i, self.modifiers)
        self.__vaildate_index(j, self.modifiers)

        if i != j:
            m_i = self.modifiers[i]
            self.modifer_del(i)
            self.modifiers.insert(j, m_i)
    def modifier_order_exchange(self, i:int, j:int)-> NoReturn:
        if not (validation.check_integer(i, True) and validation.check_integer(j, True)):
            raise ValueError(f"Invaild index value, {i} {j}")
        self.__vaildate_index(i, self.modifiers)
        self.__vaildate_index(j, self.modifiers)
        if i != j:
            self.modifiers[i], self.modifiers[j] = self.modifiers[j], self.modifiers[i] # Swap
    def modifier_del(self, i:int)-> NoReturn:
        self.__vaildate_index(i, self.modifiers)
        del(self.modifiers[i])
    def modifier_register(self, modifier:Modifier, to:bool=False) -> NoReturn:
        if not hasattr(modifier, '__type__'):
            raise ValueError("Invaild modifier")
        if type(to) == bool:
            self.modifiers.append(modifier)
        elif validation.check_integer(to, True) and to < len(self.modifiers):
            self.modifiers.insert(to, modifier)         
    # Routines
    def pdf_update(self, 
        pdf:Union[None, pypdf.PdfFileReader], 
        file:Union[str, Path, TempFile, BytesIO, FileIO, NamedTempFile], 
        page_range:Union[None, str, list] = None
        )-> NoReturn: # Change the original manuscript
            
        if type(file) == str:
            file = Path(file)
        # str -> Path, remain [Path, BytesIO, TempFile, FileIO]

        if isinstance(file, Path):
            self.file_path = self.__get_path(file, mode='f')
            
        else:
            try:
                self.file.close()
                del(self.file)
            except:
                pass
            self.file = file
            self.file_path = self.file
            

        
        self.pdf = pdf if isinstance(pdf, pypdf.PdfReader) else pypdf.PdfFileReader(self.file_path)
        self.file_pages, self.file_paper_format = self.__get_file_info(file)
        self.page_range = self.__get_page_range(page_range)
    def update(self, 
        do:Union[str, int]="all", 
        file_mode:str="safe", 
        rule:Callable[[int], int]=None
        )->str: #Update the manuscript by the registrated modifiers.
        if len(self.modifiers) == 0:
            return 0
        if do == "all":
            for index, modifier in enumerate(self.modifiers):
                print(f"{index+1}, {modifier.name} : {modifier.description}")
                modifier.do(index, self, file_mode)
            return "all"
        if rule != None and isinstance(rule, FunctionType): #Apply specific modifiers by the given rule
            for i in range(0, len(self.modifiers)):
                j = rule(i)
                modifier = self.modifiers[j]
                print(f"{index+1}, {modifier.name} : {modifier.description}")
                modifier.do(i, self, file_mode)
            return "rule"

        if type(do) == str:
            try:
                do = int(do)
            except:
                raise ValueError("Not an integer string.")
        if type(do) == int:
            if do <0 or do >= len(self.modifiers):
                raise ValueError("Invaild index.")
            else:
                modifier = self.modifiers[self.modifier_index]
                print(f"{index+1}, {modifier.name} : {modifier.description}") 
                modifier.do(1, self, file_mode)
                self.modifier_index +=1
                return f"{do}"
        else:
            raise TypeError(f"Invaild type, {type(do)}, it must be integer, integer string or \'all\'.")
    def save_to_file(
        self, 
        file:Union[None, str, Path, TempFile, FileIO, BytesIO]=None, 
        name:str = None, 
        split:Union[None,int]=None,
        check:Callable[[Path, Union[None, list]],bool]=lambda x, args: True,
        **checkargs
        ) -> NoReturn:

        if name == None:
            name = self.basic_output_file_name
        elif type(name) != str:
            raise ValueError(f"The given name must be str type. Current: {type(name)}")
        
        filepath = ""
        if file == None:
            filename = name
            filepath = self.output_path
        else:
            filepath = self.__path_check(file, mode='f')
            filename = filepath.stem
            filepath = filepath.parent

        if not check(filepath, checkargs): 
            # Additional check steps.
            # Example: file existence check
            return 1
         
        self.meta["/Producer"] = "HornPenguin Booklet"

        dt = (datetime.now()-datetime.utcnow())
        sec = dt.seconds
        time = str(int(sec/3600)).zfill(2)
        min = str(int(sec%3600)).zfill(2)
        sign = "+" if dt.days == 0 else "-"
        utcstring = sign+f"{time}'{min}'"
        current = datetime.now().strftime(r"%Y%m%d%H%M%S")

        self.meta["/ModDate" ] = f"D:{current}{utcstring}"
        
        #Save
        if split != None and split:
            pages_num = len(self.pages)
            repeat = int(pages_num/split) + (1 if pages_num%split else 0)
            for i in range(0, repeat):
                suffix_num = i+1
                filename_i = filename + f"{suffix_num}" + self.file_format
                filepath_i = filepath.joinpath(filename_i)
                pdf = pypdf.PdfFileWriter()
                with open(filepath_i, "wb") as f:
                    for j in range(0, split):
                        p = i*split + j
                        page = self.pages[p]
                        pdf.add_page(page)
                    pdf.write(f)
        else:
            filepath =filepath.joinpath(filename + self.file_format)
            with open(filepath, "wb") as f:
                pdf = pypdf.PdfFileWriter()
                pdf.append_pages_from_reader(self.pdf)
                pdf.add_metadata(self.meta)
                pdf.write(f)
        
        return 0

if __name__ == "__main__":
    pass