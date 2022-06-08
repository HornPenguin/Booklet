from __future__ import annotations

import PyPDF2 as pypdf
import webbrowser
from datetime import datetime
import textdata
import sys, os, math

from itertools import permutations

import numpy as np


status_code = {
    0: "Sucess",
    1: "Invaild page range"
}


# System directory
def resource_path(relative_path, directory):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, directory, relative_path)


#Utils===============================================================================
def open_url(url):
        return webbrowser.open(url)

def split_list(li:list, n:int)->list: #n: length of sub list
    if len(li) %n !=0:
        raise ValueError(f"The length of sublist, {n}, must be a divider of original list, {len(li)}. ")
    
    rlist =[]
    for i in range(0, int(len(li)/n)):
        ni = n*i
        rlist.append([li[ni: ni+n]][0])

    return rlist

#Permutations and generating functions for signature routines-------------------------
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

    def index_mul(self, other, oper=False):

        rlist = [self[x] for x in other.plist]
        if oper:
            self.plist= rlist
        else:
            return Permutation(self.n, rlist)

    def index_mul_partial(self, sub_permutation, oper = False): #Work on indexing
        if not isinstance( sub_permutation, Permutation):
            raise ValueError(f"Given parameter must be \'Permutation\' object. \n Current object:{type(sub_permutation)}")
        if self.n %sub_permutation.n != 0:
            raise ValueError(f"Sub permutation must have a divisor of main permuatain size as its size\n main:{self.n}, sub:{sub_permutation.n}")

        n = int(self.n / sub_permutation.n)
        m = sub_permutation.n
        
        rlist = []
        for i in range(0,n):
            tem_rlist = [self.plist[x+m*i -1] for x in sub_permutation.plist]
            rlist = rlist + tem_rlist
        
        if oper:
            self.plist = rlist
        else:
            return Permutation(self.n, rlist)

    def permute_to_list_index(self, li):
        if len(li) != self.n:
            raise ValueError(f"{len(li)} ! = {self.n}")
        
        rlist = [li[x-1] for x in self.plist ]
        return rlist

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


#PDF Utils=================================================================================

class PDFsig:
    _fold_arrange = {
        4: [
            [4,1],
            [2,3]
        ],
        8: [
            [8,1,5,4],
            [2,7,3,9]
        ],
        16: [
            [16,1,4,13,9,8,5,12],
            [10,7,6,11,15,2,3,14]
        ],
        32: [
            [44,21,28,37,40,25,24,41,53,12,5,60,57,8,9,56,52,13,4,61,64,1,16,49,45,20,29,36,33,32,17,48],
            [46,19,30,35,34,31,18,47,51,14,3,62,63,2,15,50,54,11,6,59,58,7,10,55,43,22,27,38,39,26,23,42]
        ]
    }

    def __fold_matrix_update(n, matrix):
        n_1 = np.flip(matrix.T, axis=0)
        len_n = len(n_1[0])
        l = int(len_n/2)

        rows =[]
        for row in n_1:
            r_split = np.split(row,l)
            row_appended = []

            for tu in r_split:
                tem = np.array([n-tu[0] +1,n-tu[1] +1])
                row_appended.append(np.insert(tem, 1, tu))    
            rows.append(np.concatenate(row_appended, axis=None))     
        return np.stack(rows)

    @staticmethod
    def get_info(path:str) -> tuple:
        pdf = pypdf.PdfFileReader(path)

        page_num = pdf.getNumPages()

        if page_num != 0:
            pdfinfo = pdf.metadata

            title = pdfinfo['/Title'] if '/Title' in pdfinfo.keys() else 'None'
            authors = pdfinfo['/Author'] if '/Author' in pdfinfo.keys() else 'Unkown'
            page_size=  pdf.getPage(0).mediaBox[2:]
            return title, authors, page_num, page_size
        
        return False, False, False, False
    @staticmethod
    def sig_layout(n:int) -> tuple:
        if type(n) != int or n<4 or n%4 !=0:
            raise ValueError(f"n:{n} must be a positive integer that multiple of 4.")
    
        i = int(math.log(n/4 ,2))
        if i%2 :
            k = kp = int((i+1)/2)
        else:
            k = int(i/2)
            kp = k+1
        return (int(2**k), int(2**kp))
    @classmethod
    def fold_arrange_n(cls,n: int) -> list:
        if n % 4 !=0:
            raise ValueError("Fold sheets must be 4*2^k for k= 0, 1, 2, .... \n Current value is {n}")
    
        if n <64:
            return cls._fold_arrange[n]
        else:
            n_iter = int(math.log(n/16,2))
            n_i = 32
            per_n_1 = [cls._fold_arrange[n_i][0], cls._fold_arrange[n_i][1]]
    
            #permutation to matrix
            layout_n_1 = cls.sig_layout(n_i)
            front_matrix = np.array(per_n_1[0]).reshape(layout_n_1)
            back_matrix = np.array(per_n_1[1]).reshape(layout_n_1)
            for i in range(0, n_iter):
                n_i = 2*n_i
                front_matrix = cls.__fold_matrix_update(n_i, front_matrix)
                back_matrix = cls.__fold_matrix_update(n_i, back_matrix)   
        per_fn = np.concatenate(front_matrix).tolist() 
        per_bn = np.concatenate(back_matrix).tolist()
    
        return [per_fn, per_bn]       
    @classmethod
    def fold_list_n(cls, n, per=False):
        if n % 4 !=0:
            raise ValueError("Fold sheets must be 4*2^k for k= 0, 1, 2, .... \n Current value is {n}")
        
        if n < 64:
            return cls._fold_arrange[n]
        else:
            n_iter = int(math.log(n/16,2))
            n_i = 32
            per_n_1 = [cls._fold_arrange[n_i][0], cls._fold_arrange[n_i][1]]

            #permutation to matrix
            layout_n_1 = cls.sig_layout(n_i)
            front_matrix = np.array(per_n_1[0]).reshape(layout_n_1)
            back_matrix = np.array(per_n_1[1]).reshape(layout_n_1)
            for i in range(0, n_iter):
                n_i = 2*n_i
                front_matrix = cls.__fold_matrix_update(n_i, front_matrix)
                back_matrix = cls.__fold_matrix_update(n_i, back_matrix)   
        per_fn = np.concatenate(front_matrix).tolist() 
        per_bn = np.concatenate(back_matrix).tolist()

        if per:
            Permutation(n, per_fn+per_bn )
        else:
            return [per_fn, per_bn]      
    @classmethod
    def sig_rearrange(cls, nn, ns): #1
        n_l = nn*ns

        nlist = [i+1 for i in range(0, n_l)]
        nlist_splited = split_list(nlist, int(ns/2))
        rlist=[]

        n_splited = 2*nn
        for i in range(0,nn):
            rlist = rlist + nlist_splited[i] + nlist_splited[n_splited-i-1]

        return rlist
    @classmethod
    def signature_permutation(cls, n, nn, ns, riffle=True):
        permutation_riffle = Permutation(n, range(1, n+1)) if riffle else  Permutation.reverse_permutation(n)
        permutation_signature = Permutation(n, cls.sig_rearrange(nn,ns)).index_mul_partial(cls.fold_list_n(ns, per=True))

        return permutation_riffle * permutation_signature

       


# Reverse -> Signature gen -> fold permutation
def sig_permutation(n):
        per = [n,1]
        for i in range(1, int(n/2)):
            per.extend([1+i, n-i])
        return per


def signature_permutation(n, fold, riffle=True): # riffle: right=True, left=False
    per_riffle = Permutation(n, range(1, n+1)) if riffle else  Permutation.reverse_permutation(n)
    per_sig = Permutation(n, sig_permutation(n))

    return per_sig * per_riffle

def gen_signature(input_file, output_file, **parameters):
        #Parameters
        # 1. filename(str): File name of output
        # 1. leaves(list(nl, nn, ns)) 
        #               nl(int): number of leaves per signature
        #               nn(int): number of sub signature
        #               ns(int): number of leaves per subsignature: nl = nn x ns
        # 2. fold(bool): determines n-fold book or not( fold more than 1 per each papaer)
        # 3. riffle(bool): determines reiffle direction of pages, default = False(left to right)
        # 4. format(list(formatbool, width, height)): paper format dimension
        # 5. imposition(bool):
        # 6. blank(list(mode, n))
        #               mode(str): determines distribution of additional blank page to its value(front, back, both(=equal)).
        #               n(int): number of additional blank page(s).
        # 7. split(bool): determines whether split each signatures as disfferent files or not.
        # 8. sigproof(list(sigproofbool sig_color)) 
        #               sigproofbool(bool): determines add sigproof or not
        #               sig_color: hex color code
        # 9. trim(bool): add trim or not
        # 10. registration(bool): add registration or not
        # 11. cymk(bool): add cymk proof or not  

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

        #Get number of pages
        page_n = pdf.getNumPages()

        #Generates signatures
        per_n = sig_permutation(leaves, riffle)
        #Calculate addtional pages
        re_n = int(page_n /leaves) + (1 if page_n%leaves else 0)

        #Format 
        f_dim = textdata.PaperFormat[format].split("x")
        width = float(f_dim[0])
        height = float(f_dim[1])
        scale_x = scale_y = 1.0


        scale_x = width/parameters["format"][0]
        scale_y = height/parameters["format"][1]

        
        for i in range(0, re_n):
            for j in range(0, leaves):
                l  =  leaves* i + per_n[j] -1
                if l >= page_n:
                    pdf_sig.add_blank_page(width = width, height= height)
                else:
                    page =pdf.pages[l]
                    page.scale(scale_x, scale_y)
                    pdf_sig.add_page(pdf.pages[l])
        

        output = open(output_file, "wb")
        pdf_sig.write(output)
        output.close()

        return 0

