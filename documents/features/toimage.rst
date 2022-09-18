=================
ToImage
=================


Some PDF files could be broken for their page contents during the rotation of pages.
To avoid such a situation, *toimage* routine is presented. 
This routine converts all pages in the manuscript to single images per page.
However, it increases file size and makes converting speed slow more than 10 times.



**Converter**


Class
==========

.. 
    .. autoclass:: booklet.core.converters.toimage.ToImage
   