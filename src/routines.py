from __future__ import annotations

import PyPDF2 as pypdf
import webbrowser
from datetime import datetime
import textdata
import sys, os

from itertools import permutations


class Permutation:
    @classmethod
    def get_permutations(cls, n, per=False): # get list of permutations for given 'n'
        per = permutations(range(1, n+1), n)
        if per:
            return [cls(n, p) for p in per]
        else:
            return [ p for p in per]
    @classmethod
    def reverse_permutation(cls, n):
        return cls(n, range(n, 0, -1)) 

    def __init__(self, n, plist):
        if len(plist) != n:
            raise ValueError(f"{n} must be same with len(plist) = {len(plist)}")

        if sum(plist) != int(n* (n+1)/2):
            raise ValueError(f"plist does not satisfy permutation proeprty.\n All [0, n-1] values must be in plist. \n {plist}")

        self.n = n
        self.plist = plist
    def __getitem__(self, key):
        if type(key) != int:
            raise ValueError(f"key must be an integer type element: {key}")
        if key < 1 or key > self.n:
            raise IndexError(f"{key} must be in [1, {self.n}] range.")
        
        return self.plist[key-1]
    def __mul__(self, other: Permutation) -> Permutation:
        if self.n != other.n:
            raise ValueError(f"{self.n} and {other.n} are not same.")
        
        rlist = [other[x] for x in self.plist]
        return Permutation(self.n, rlist)
    
    def inverse(self)-> Permutation:
        ilist= [self.plist.index(x)+1 for x in range(1, self.n+1)]
        return Permutation(self.n, ilist)
    
    def notation_cauchy(self):
        return f"{list(range(1, self.n+1))}\n{self.plist}"

    
    def __canocial_order(self, cyclist):
        c_clist_1 = []
        c_clist_2 = []
        for li in cyclist:
            n = len(li)
            nmax = li.index(max(li))
            c_clist_1.append([li[x] for x in range(nmax-n, nmax)])
        maxindex = [x[0] for x in c_clist_1]
        s_index = sorted(maxindex)

        for i in s_index:
            c_clist_2.append(c_clist_1[maxindex.index(i)])
        
        return c_clist_2

    def notation_cyclic(self, canonical=False, string= False, sep=''):
        cycliclist = []
        index = list(range(1, self.n+1))
        i =1

        while True:
            ilist = []
            ilist.append(i)
            index.remove(i)
            
            sig_i = self[i]
            while sig_i in index:
                ilist.append(sig_i)
                index.remove(sig_i)
                sig_i = self[sig_i]
            
            cycliclist.append(ilist)

            if len(index) > 0:
                i = min(index)
            else: 
                break
        if canonical:
            cycliclist = self.__canocial_order(cycliclist)
        
        if string:
            cycstr = ''
            for li in cycliclist:
                cycstr = cycstr+ '('+f'{sep}'.join(map(str,li))+')'
            return cycstr
        else:
            return cycliclist

def resource_path(relative_path, directory):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, directory, relative_path)

def open_url(url):
        return webbrowser.open(url)

def get_pdf_info(pdf_path):
        pdf = pypdf.PdfFileReader(pdf_path)
        page_num = pdf.getNumPages()
        
        if page_num != 0:
            pdfinfo = pdf.metadata

            title = pdfinfo['/Title'] if '/Title' in pdfinfo.keys() else 'None'
            authors = pdfinfo['/Author'] if '/Author' in pdfinfo.keys() else 'Unkown'
            page_size=  pdf.getPage(0).mediaBox[2:]
            return title, authors, page_num, page_size
        return False, False, False, False


# Reverse -> Signature gen -> fold permutation


def sig_permutation(n):
        per = [n,1]
        for i in range(1, int(n/2)):
            per.extend([1+i, n-i])
        return per


def signature_permutation(n, fold, riffle=True):
    per_riffle = Permutation(n, range(1, n+1)) if riffle else  Permutation.reverse_permutation(n)
    per_sig = Permutation(n, sig_permutation(n))

    return per_sig * per_riffle

def gen_signature(input_file, output_file, leaves, format, fold, riffle = True):

        pdf = pypdf.PdfFileReader(str((input_file)))
        pdf_sig = pypdf.PdfFileWriter()

        #Copy metadata and add 'producer' and 'moddata'
        meta = {}
        for key in pdf.metadata.keys():
            val = pdf.metadata.raw_get(key)
            meta[key] = str(val) 
        pdf_sig.add_metadata(meta)
        pdf_sig.add_metadata({"/Producer": "HornPenguin Booklet"})
        pdf_sig.add_metadata({"/ModDate": f"{datetime.now()}"})

        
        page_n = pdf.getNumPages()
        per_n = sig_permutation(leaves, riffle)

        re_n = int(page_n /leaves) + (1 if page_n%leaves else 0)

        f_dim = textdata.PaperFormat[format].split("x")
        width = float(f_dim[0])
        height = float(f_dim[1])
        scale_x = scale_y = 1.0

        if format != "Default":
            fd_dim = textdata.PaperFormat["Default"].split("x")
            
            scale_x = width/float(fd_dim[0])
            scale_y = height/float(fd_dim[1])

        
        for i in range(0, re_n):
            for j in range(0, leaves):
                l  =  leaves* i + per_n[j] -1
                if l >= page_n:
                    pdf_sig.addBlankPage(width = width, height= height)
                else:
                    page =pdf.pages[l]
                    page.scale(scale_x, scale_y)
                    pdf_sig.addPage(pdf.pages[l])
        

        output = open(output_file, "wb")
        pdf_sig.write(output)
        output.close()

        return 0


