.. HornPenguin Booklet documentation master file, created by
   sphinx-quickstart on Sun Jul 10 15:39:22 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

HornPenguin Booklet
===============================================

HornPenguin Booklet is a free and open source booklet generating 
program. It can reorder the pages, rotate and transform for fold signature,
and add printing markers for color printing. 

You can print your own book signatures and simple pamplet with your home printer.

* Support diffence signature size from 4 to 32.
* Change page size during generating signature.
* Left riffling direction is supported for old Asian and Arabic bookbindings.
* Printing markers; trim, CMYK, signature proof are supported.


  

Structure of Program
--------------------------

+--------------+-----------------+---------------+
|  Interface   |PDF modulation   | PDF generation|
+--------------+-----------------+---------------+
|GUI(tkinter)  | PyPDF2          | reportlab     |
+--------------+                 |               |
|CUI(argparse) |                 |               |
+--------------+-----------------+---------------+



.. toctree::
   :maxdepth: 1
   :caption: User Guide

   user/installation
   user/usage
   user/terms
   
.. toctree::
   :maxdepth: 2
   :caption: Core

   booklet

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
