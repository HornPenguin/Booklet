Section
==================


Example
-----------


Implementation
-----------------

.. rubric:: :class:`Signature <booklet.core.converters.signature.Signature>`
    parent: :class:`Converter <booklet.core.manuscript.Converter>`
    related class: :class:`SigComposition <booklet.core.converters.signature.SigComposition>` 

It is just a simple 

It is hardly interwinded with :ref:`Imposition <imposition>` feature.


Custom
----------------

Custom routine of section allow users to make custom 
order and imposing map. 

Layout
^^^^^^^^^^^^

If you make custom map or brochure not included in standard
brochure type, you can use custom layout routine.
This routine requires imposing layout and page map of front.
Since, the pages share same region of paper, front and back, must be 
simultaneously arranged, back map is specified with front map.

However, if you want to make custom section for making book section.
This routine requires too much calculation and experiment for users.
In those cases, you can use *Fcode* routine below.

Fcode
^^^^^^^^^^^^^^^^^^^^^^

Fcode is an abbreivation of *Fold code* which describes fold sequence and type of 
paper. HornPenguin Booklet generate detailed page imposition, creasing level 
and layout from Fcode. Each mapping guarantees that right order of pages after you finishing fold or imposed paper.
With Fcode description, users can make a desired imposition
map from a custom section configuration. 

Pros:

1. You can make 

Assumption
"""""""""""""""""

* Couting order: from top to bottom (:math:`y` direction), from left to right (:math:`x` direction) 
* 1st page must be shown in front of paper for all steps of folding. 

Grammar
"""""""""""""""""

* Folding direction in every steps is perpendicular to previous direction.
* Parallel folding can be achieved in single step.
* Each fold line is specified with *M,V* code and order number.
* Last step must be a :code:`1, M1`, if you intend to make a book.

Example,

.. code-block:: 

    x <- initial direction
    3, M1 V2 M3
    4, M2 V4 M3 V1
    1, M1

* :code:`\[#\]` : Number of folding in step
* :code:`M#1 V#2 M#3`: Specifying each fold order and type.

For example, 12 page section can be described as 

**12**

.. code-block:: 

    x
    2, M2 V1
    1, M1

for standard section, description is simple. About :math:`16` page section.

**16**

.. code-block:: 

    y
    1, M1
    1, M1
    1, M1



