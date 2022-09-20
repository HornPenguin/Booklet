==================
Imposition
==================


The imposition is locating works of pages to paper and the result of them.
Unless you bining book in old Asia style (their method can use single paper as a basic signature), 
you must print the signature considering fold action for efficiency.
This is why the manuscript for a book should have page range which is a divisor of 4.

Since, imposition is implicitly considering fold action in post stage.
Calculating its layout on single page is not an easy task. 
However, for standard page numbers, 4, 8, 16, ... 32, 64,
their layouts have been well known in printing area.

Stadard pages unit
--------------------



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

