.. HornPenguin Booklet documentation master file, created by
   sphinx-quickstart on Sun Jul 10 15:39:22 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

HornPenguin Booklet
===============================================

.. image:: _static/main.png


HornPenguin Booklet is a free and open source booklet generating program. 
It can reorder the pages, rotate and transform for fold signature, 
and add printing markers for color printing.

You can print your book signatures and a simple pamphlet with your home printer.

* Support difference signature size from 4 to 64.
* Imposition.
* Change page size during generating a signature.
* Left riffling direction is supported for old Asian, Hebrew, and Arabic bookbindings.
* Printing markers: trim, CMYK, signature proofs are supported.

You can see basic and advanced tutorials in `Usage <user/usage>`_.
Please read a `License` if you want to use, contribute, or distribute to other place.

If you want to contribute to this project see `Development Guide <develop/guide>`.


.. toctree::
   :maxdepth: 1
   :caption: User Guide

   user/about
   user/installation
   user/usage
   user/terms

.. toctree::
   :maxdepth: 1
   :caption: Features

   features/signature
   features/imposition
   features/toimage
   features/printingmark
   features/note

.. toctree::
   :maxdepth: 1
   :caption: Development Guide

   develop/guide
   develop/news
   develop/license

.. toctree::
   :maxdepth: 1
   :caption: Api Reference

   modules

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
