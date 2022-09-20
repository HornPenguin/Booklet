============================
Terms of Book and Printing
============================

This document describes basic introduction to bookbinding and printing.

Shape and Structure of Book
==================================

Bookbinding is a work of binding materials to make a book. 
Including historical approach, rolled scroll can be included, but in this chapter common style of book will be treated.
It is called *Codex* style. Codex is 
In a view of bookbinding, book, codex, is an object which is composed of multiple *signature*.

Signature
-----------

The **signature** is a contents block of a book, pamphlet, or booklet. 
That is, *a group of sheets* not separated by its contents, but a prefixed number of sheets. 
There are some synonyms, **section**, and **gathering**. This document will use **signature**.

Pages compose a signature and the signatures compose a book, booklet, ..., et cetera.
A single page can become a signature and a single singnature can compose a single book or booklet, (usually booklet).

Why we need signature in bookbinding? 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you have made ring or stapler binding in home or local printing center, you might not think 
it is not needed to prepare content block by prefixed number of leaves.  
However, if pages exceeds more than hundreds, you cannot prepare all contents to bind at once.
With some efforts, it might be possible but

Signature composition
^^^^^^^^^^^^^^^^^^^^^^^^^

As written above, a signature is governed by its number of sheets. 
Single paper signature is :math:`2` sheets signature with dual side printing.
The number of sheets of signature must be a multiple of :math:`4`, practically considering *fold*.
Therefore, permitted numbers are :math:`4, 8, 16, 32, 64` and :math:`12, 24`.
:math:`12, 24` signatures differ in its fold progress with :math:`4, 8, 16, 32, 64`.
Bigger sheets can be used :math:`>64` to make a single signature, but it is not practical.


.. image:: ../_static/gathering_inserting.png

There are two types of methods to combine signatures, 
**inserting** and **gathering**. There are no differences among them after cutting their edges, but the order of pages are differ by type.
The *gathering* does not affect to order of each signature but *inserting* does to match the correct ordering of pages. 

The :math:`n` sheets signature is composed of :math:`i` time inserted :math:`f` sheets signature.

.. math:: 
    n = i \times f.

If :math:`i = 1`, the signautre is an uninserted fold signature. 

For example, :math:`16` sheets signature has next variation.

* :math:`1 \times 16`
* :math:`2 \times 8`
* :math:`4 \times 4`




Riffle direction
--------------------

.. image:: ../_static/riffle.png

**Riffle direction** is a direction of riffling while you read the contents of a book.
It depends on the reading direction of language. The most common direction is a horizontal, from left top to right bottom(HLTRB) direction.
There were various reading directions by the language system. Most of them are not used in the recent era, but from left to right reading direction
frequently used in many situations more than people think. 

Belows are uncommon example languages in reading direction.

* Asia, Korea, Japan, China ... etc 
    
    East Asians used **VRTLB** (vertical, from right top to left bottom) system. 
    Now, vertical writing is rarely seen in modern texts in Asia (it is different by the country), but as a design or a research work, they are still adopted in many works.
    For example, some Japanese mangas use vertical writing in their speech bubbles. There is a good different point in the speech bubble by the writing direction in Japan and Korea. 
    Japan's speech bubbles are vertically long while Korea's are horizontally long. 
    Korea also uses vertical writing once, but in the modern era is not as popular as in Japan. This difference is affecting to their speech bubble shape in comics.
    It is one example that how the cultural difference, in this case writing direction, is visually expressed.

* Hebrew and Arabic 
    
    RL system

* Ancient Egyt 
    
    Their system was very special. They used both direction LR and RL. 
    The same characters can be written symmetrically by the direction.

* Elder Island script, Ogham scripts 
    
    It also has an abnormal direction. Its direction is vertically from bottom to top.


From top to bottom, or from bottom to top are not affected by the order of pages if you riffle horizontally.
However, whether the reading direction is LR or RL affects the page ordering considering reading efficiency.

The default setting of HornPenguin Booklet is a LR direction and supports *RL*.

Supporting *RL* is not complicated. Just reverse order the pages before applying to rearrange transformation to the pages.


Imposition
-------------

The imposition means locating works of pages to paper and the result of those works.
Unless you binding book in old Asia style (their method can use single paper as a basic signature), 
you must print the signature considering fold action.
This is why the manuscript for a book should have a number of pages which is a multiple of 4.



Printing markers
================================

Signature proof
-----------------

.. image:: ../_static/proof.png

**Signature proof** is a ordering proof marker on the spine of signatures. It helps for people to arrange the signatures in right order
and check missing signatures.



Trim marker
-----------------

Trim location indicator.


Registration marker
-----------------------

**Registration marker** is added to check the registration of color printing of printing machine. 
Its color looks like the normal black color (CMYK(0, 0, 0, 100)) but actually, it is a special color called
*registration black*, CMYK code is (100, 100, 100, 0). If they are perfectly fitted, it will look like normal black color.






Further reading
--------------------


* Matt T. Roberts and Don Etherington, Bookbinding and the Conservation of books: A Dictionary of Descriptive Terminology, Drawings by Margaret R. Brown

`Online version <https://cool.culturalheritage.org/don/>`_ is available. 