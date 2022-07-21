=========================
Terms and basic infos
=========================

This document describes about basic expressions of printing and press and their introductions.


Shape and Structure of Book
==================================

Signature
-----------

The **signature** is a contents block of book, pamplet or booklet. 
That is, *a group of sheets* not seperated by its contents, but prefixed number of sheets. 
There are some synonyms, **section**, and **gathering**. This document will use **signature**.

Pages compose signature and the signatures compose book, booklet, ..., et cetera.
Single page can become a signature and single singnature can compose single book or booklet, (usually booklet).

Signature composition
^^^^^^^^^^^^^^^^^^^^^^^^^
As wrote the above, signature is governed by its number of sheets. 
Single paper signature is a :math:`2` sheets signature with dual side printing.
The number of sheets of signature must be a multiple of :math:`4`, practically considering *fold*.
Therefore, permitted numbers are :math:`4, 8, 16, 32, 64` and :math:`12, 24`.
:math:`12, 24` signatures are differ in its fold progress with :math:`4, 8, 16, 32, 64`.
Bigger sheets can be used :math:`>64` to make single signature, but it is not practical.

There are two types of methods to combine signatures, 
**inserting** and **gathering**. They are same after cutting the edges, but its order of pages are differ by types.
The *gathering* does not affect to order of each siganature but *inserting* does to match the correct ordering of pages. 

The :math:`n` sheets signature is composed of :math:`i` time inserted :math:`f` sheets signature.

.. math:: 
    n = i \times f.

If :math:`i = 1`, the signautre is an uninserted fold signature. 

For example, :math:`16` sheets signature has next variation.

* :math:`1 \times 16`
* :math:`2 \times 8`
* :math:`4 \times 4`

See graphical examples.



Riffle direction
--------------------

**Riffle direction** is a direction of riffling while you read contents of book.
It depends on reading direction of language. The most common direction is a horizontal, from left top to right bottom(HLTRB) direction.
There were various reading direction by the language system. Most of them are not used in recent era, but from left to right reading direction
frequently used in many situations more than the people think. 

Belows are uncommon example languages in reading direction.

* Old asian: East asians used VRTLB(vertical, from right top to left bottom) system. 
    Now, vertical writing is rarely seem in modern texts in asia (it is differ by the countries), but as a design or a research works, they are still adopted in many works.
    For example, some Japan mangas using vertical writing in their speech bubbles. There is a good different point in speech bubble by the writing direction in Japan and Korea. 
    Japan's speech bubbles are vertically long while the Korea's are horizontally long. 
    Korea also use vertical writing sometimes but not as popular as Japan. This difference are affecting to their speech bubble shape in comics.
    It is one example that how the curtural difference, in case writing direction, are visually expressed.
* Hebrew and Arabic: RL system
* Ancient Egyt: Very special they used both direction LR and RL. The same characters can written symmetrically by the direction.
* Elder Island script, Ogham scripts: It also has abnormal direction very rare. It direction is vertically from bottom to top.


From top to bottom, or from bottom to top are not affected by the order of pages.
However, whether the reading direction is LR or RL affects the page ordering considering reading efficiency.

The default setting of HornPenguin Booklet is a LR direction and support *RL*.

Supporting *RL* is not complicate. Just reverse order the pages before applying rearrange transformation to the pages.


Imposition
-------------

Printing markers
================================

Signature proof
-----------------

**Signature proof** is a ordering proof makrer on spine of signatures. It helps for people to arrange the signatures in right order
and check missing signatures.

Trim marker
-----------------

Trim location indicator.


Registration marker
-----------------------

Registration marker is added to check the registration of color printing of printing machine. 
It's color looks like normal black color (CMYK(0, 0, 0, 100)) but actually it is a special color called
*registration black*, CMYK code is (100, 100, 100, 0). If they are perpectly fitted, it will look like normal black color.



