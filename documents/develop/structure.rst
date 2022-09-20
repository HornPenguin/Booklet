=============
Structure 
=============

.. _structure:


The core routines are implemented with :class:`Manuscript` class and :class:`Modifier`.
The :class:`Modifier` class acts as a filter of data. It combines, rearranges, deletes, adds new objects to pages.
The features in this project, (Signature, Toimage, Imposition, PrintingMark, Note), are implemented with single class which are children of :class:`Modifier`.
Those class are categorized two types, :class:`Converter` and :class:`Template`. These two class are children class of :class:`Modifier`.

* :class:`Converter`: This class is about the conversion of file and page. Rearrange, delete, transformation, change page type are example. Major difference with :class:`Template` is that this class does not contain *merge* and additional template pdfs.
* :class:`Template`: This class is about the template imposition of manuscript. There are two direction of merging, imposing the manuscript on template or vice verse.

Core structure
----------------

.. code-block:: 
    :caption: Bone structure

    from booklet.manuscript import Manuscript
    from booklet.modifiers import *

    manuscript = Manuscript(file, output_directory, file_name)

    modifier1 = ToImage()
    modifier2 = Signature()
    modifier3 = Imposition()

    modifiern = PrintingMark()

    modifiers = [modifier1, modifier2, modifier3, ..., modifiern]

    for modifier in modifiers:
        manuscript.register_modifier(modifier)
    
    manuscript.update("all")
    manuscript.save_to_file()


Implemented modifiers are 

* Signature(Converter)
* ToImage(Converter)
* Imposition(Template)
* Printing Mark(Template)


Template class
-------------------

It was intended to load external pdf file in inital stage of class object.
However, with external libraries, like reportlab, we can combine template pdf generation code in class.




See details in :ref:`API reference <api_reference>` and source `repository <https://github.com/HornPenguin/Booklet>`_.
