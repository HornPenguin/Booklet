Imposition
==================

.. _imposition:

Calculating layout and case of signature is not an easy task. 
It is a research topic in computational geometric field.
However, for standard page numbers, 4, 8, 16, ... 32, 64,
their layouts have been well known in printing area.


The imposition is locating works of pages to paper and the result of them.
Unless you bining book in old Asia style (their method can use single paper as a basic signature), 
you must print the signature considering fold action for efficiency.
This is why the manuscript for a book should have page range which is a divisor of 4.

Since, imposition is implicitly considering fold action in post stage.
Calculating its layout on single page is not an easy task. 

Folding 
--------------------



Standard Type
--------------------

This type signature alternately changes folding direction in each step. 
:math:`2, 4, 8, \dots, 2^n` leaves signatures are included in.  

Algorithm
^^^^^^^^^^^^^

It will be worth to describe folding layout update process.

* :math:`n` sheets signature contains :math:`n` number of pages.
* Imposition of :math:`n` sheets signatures are divided into two sections, the front page and the back page.

This process covers next signatures.

.. math:: 

    a_0 = 4 \\\\

    a_n = 2 \cdot a_{n-1}


Let's start from :math:`4` sheets signature, its page layout is a :math:`(1,2)`.

Front page: :math:`[4, 1]`

Back page: :math:`[2, 3]`

from these two matrix, we will get page imposition of :math:`8` sheets signature.

Imagine the folding process of :math:`4` sheets signature to make :math:`8` sheets signature.
We rotate 90 degrees and split them into :math:`2` sub-sections.
Interesting point is that, the :math:`k`-th page of :math:`2n` sheets signature always exists in :math:`k`-th page of :math:`n` sheets signature, :math:`1 \leq k \leq n`.
In addition, the two pages, :math:`a, b`, seperated by the creasing line have next relationship, :math:`a+b = n+1`. 

These are all we need. The remains are just following them.


Rotating
"""""""""""

Rotating elements of matrix can be divided into two steps, transpose and flip.
See rotation of the elements of 90 degree in counter-clockwise direction,

*Transpose*:

.. math:: 

    [4, 1] \rightarrow \begin{bmatrix} 4 \\ 1 \end{bmatrix}

*Flip*:

.. math:: 

    \begin{bmatrix} 4 \\ 1 \end{bmatrix} \rightarrow \begin{bmatrix} 1 \\ 4 \end{bmatrix}

Expanding
"""""""""""

Now expand each line using :math:`a+b = n+1`.
Basically, in a single number case, an additional number is left of the previous number. 

.. math:: 

    8 = 8 + 1 -1, [1] \rightarrow [8 ,1] \\\\

    5 = 8 +1 -4,  [4] \rightarrow [5, 4]

Then, we get a front layout matrix of the :math:`8` sheets signature.
In the same way, let's get a front layout matrix of the :math:`16` sheets signature.

*Rotating*:

.. math:: 

    \begin{bmatrix}
        8& 1 \\
        5& 4
    \end{bmatrix} \rightarrow 
    \begin{bmatrix}
        1& 4 \\
        8& 5
    \end{bmatrix}


*Expanding*:

.. note:: 

    There is a little different in :math:`n>4` case. 
    In expanding steps, you must divide row numbers into sub-groups whose length is :math:`2`.
    The prior number process is the same with :math:`n=4` case but the second number is remained at right in expanding progress.
    For example, if we have :math:`[13, 12, 4, 5, 1, 8, ...]` row then, :math:`[[13, 12], [4, 5], [1, 8], ...]` and expand them.

.. math:: 

    [1, 4] \rightarrow 
    [ [16 , 1 ], [4, 13] ] 

.. math:: 

    [8, 5] \rightarrow 
    [ [ 9 , 8 ], [ 5 , 12 ] ]

See update steps of front matrix:

.. math:: 

    \begin{bmatrix} 4& 1\end{bmatrix} \rightarrow 
    \begin{bmatrix} 
        8& 1 \\
        5& 4
    \end{bmatrix} \rightarrow 
    \begin{bmatrix} 
        16& 1& 4& 13 \\
        9& 8& 5& 12
    \end{bmatrix}

Rotating Page
""""""""""""""""""""""

Imposition work includes folding work. 
That is, pages must be rotated in the right direction to match the direction of each page after the fold. 
In imposition layout, it is simple. Just rotating :math:`2, 4, 6, ..., 2k, ...` rows of 180 degrees.



..
    Algorithm
    ^^^^^^^^^^^

    Character arguments of :math:`n` page signature imposition.

    * page number per signature
    * page order of signature
    * layout on imposition page.

    For example, :code:`n = 4, 8` page signatures are determineded as 

    * :code:`n = 4`: 4 , [[4, 1], [2, 3]], (1,2)
    * :code:`n = 8` : 8, [[8, 1, 5, 4], [2, 7, 3, 6]], (2, 2)  

    Now defines page matrix 

    .. math:: 

        P = [F, B] \\

        F, B \in \mathbb{M}_{r, c}(\mathbb{Z})

    Dimension
    """"""""""
    :math:`\text{dim}(F) = \text{dim}(B) = (r, c)`

    .. math:: 

        i_n = \floor(\log_2(\frac{n}{4}))
        k_n = 
            \begin{array} 
                \floor(\frac{(i_n + 1)}{2}) & if i_n is even.\\
                \floor(\frac{i_n}{2}) & if i_n is odd.
            \end{array}
        {kp}_n = 
            \begin{array} 
                k_n & if i_n is even.\\
                k_n +1 & if i_n is odd.
            \end{array}

        r_n = 2^{k_n}
        c_n = 2^{{kp}_n}



    .. math:: 

        \{p_i\}_{i=0}^{n} := 
        p_0 = 4 \\

        p_k = 2 \cdot p_{k-1} 


Deep Type
--------------

Deep type is applying arcodian folding in one step in fold process.
This allow as more flexible layout than standard folding.
For example, 12, 24 leaves imposition was impossible, but here we can acheieve 
right ordered page signature.



Composition of multiple Signature
------------------------------------

Example
-----------


Implementation
-----------------


Further readings
--------------------



