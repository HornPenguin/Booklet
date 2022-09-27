=============
Structure 
=============

.. _structure:


Overview
------------

The overall structure of HP Booklet program is setting a filter in pipe-filter progress. 

The core routines are implemented with :class:`Manuscript <booklet.core.manuscript.Manuscript>` class and :class:`Modifier <booklet.core.manuscript.Modifier>`.
The :class:`Modifier <booklet.core.manuscript.Modifier>` class acts as a filter of data. 
It combines, rearranges, deletes, adds new objects to pages and return manuscript.
The features in this project, (Signature, Toimage, Imposition, PrintingMark, Note), are implemented with single class which are children of :class:`Modifier <booklet.core.manuscript.Modifier>`.
Those class are categorized two types, :class:`Converter <booklet.core.manuscript.Converter>` and :class:`Template <booklet.core.manuscript.Template>`.

* :class:`Converter <booklet.core.manuscript.Converter>`: This class is about the conversion of file and page. Rearrange, delete, transformation, change page type are example. Major difference with :class:`Template` is that this class does not contain *merge* and additional template pdfs.
* :class:`Template <booklet.core.manuscript.Template>`: This class is about the template imposition of manuscript. There are two direction of merging, imposing the manuscript on template or vice verse.

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


Modifier
--------------

Converter Class
^^^^^^^^^^^^^^^^^^^

There is nothing to describe about this class. It is just an warrper of :class:`Modifier <booklet.core.manuscript.Modifier>` to match a children layer with :class:`Template <booklet.core.manuscript.Template>`.

Template Class
^^^^^^^^^^^^^^^^^^^

It was intended to load external pdf file in inital stage of class object.
However, with external libraries, like reportlab, we can combine template pdf generation code in class.

All the variables and calculations must be prepared after :code:`__init__` method is called.
New features are needed to implement 3 methods

* :code:`rule(self, i:int)`: Return imposed manuscript pages of the given template page. For example, if :code:`k` th template page cotains :code:`2, 4, 7, 9` pages of manuscript. 
   
   .. code-block:: python3

    rule(k) # [2, 4, 7, 9] 

* :code:`position(self, i:int)`: Return position of the given manuscript page on template page. :code:`tuple[float, float]`.

* :code:`generate_template(self, manuscript:Manuscript)` : Return template pdf and its connected tempfile object.

Template :code:`do` method
""""""""""""""""""""""""""""""""

.. code-block:: python3

    def do(self, index:int, manuscript: Manuscript, file_mode:str = "safe"):

        if not self.on:
            pass
        else:
            new_pdf, new_file = self.get_new_pdf(index, manuscript.tem_directory.name, file_mode)
            try:
                getattr(self, "pdf")
                template_pdf = self.pdf
            except:
                template_pdf, tem_byte = self.generate_template(manuscript)
            for i, template in enumerate(template_pdf.pages):
                manu_pages = self.index_mapping(manuscript, i, len(template_pdf.pages))
                for j in manu_pages:
                    page = manuscript.pages[j]
                    x, y = self.position_mapping(manuscript, j, manuscript.file_pages)
                    page.addTransformation(
                        pypdf.Transformation().translate(tx=x, ty=y)
                    )
                    upper = float(page.mediaBox[2])
                    right = float(page.mediaBox[3])
                    page.mediaBox.setUpperRight((upper + x, right + y))

                    template.merge_page(page)
                    new_pdf.add_page(template)
            
            new_pdf.write(new_file)
            manuscript.pdf_update(new_pdf, new_file)


Example feature :class:`Imposition <booklet.core.templates.imposition.Imposition>`
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

.. code-block:: python3

    def rule(
        self, i: int
    ) -> list:  # i = template page, list = manuscript pages unordered
        _i = i * self.pages_per_template
        _f = (i + 1) * self.pages_per_template
        return list(range(_i, _f))

    def position(self, i: int) -> tuple[float, float]:  # manuscript page
        index = i % self.pages_per_template
        column = self.layout[1]
        row = self.layout[0]

        x = (index) % column
        y = row - floor((index) / column) - 1
        x_pos = (self.manuscript_format[0] + self.gap) * x - (
            self.gap if x > column - 1 else 0
        )
        y_pos = (self.manuscript_format[1] + self.gap) * y - (
            self.gap if y > row - 1 else 0
        )

        return (x_pos, y_pos)



See details in :ref:`API reference <api_reference>` and source `repository <https://github.com/HornPenguin/Booklet>`_.
