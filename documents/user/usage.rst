.. _usage_label:

Usage
===============




Basic
------------

Select PDF file to modulate
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. 
    .. image:: file_selection.png

Programs automatically detect meta datas, title, authors, and pages, of given pdf files.
In cui, just typing path of selected pdf file.

Settings
^^^^^^^^^^^^

* File name: Name of output file. You can modify it, but beaware that it does not check existence of given file. Default value: `{original file name}_HP_BOOKLET.pdf`
* Leaves: Number of sheets per each signature. When you choose specific number of sheets, additional blank pages will be shown right to selection box.
* Book Format: Page dimension of output file. Default: original page size. See dimension(mm) in above `Help` -> `Paper Format` reference.
* Fold: Fold option is restricted to some special sheet numbers and they are notated "{number}f"
* Riffling: Riffle direction of output file. Default: `right`. `left` is for old Asian, Arabic, and Hebrew manuscript.


 
Advanced options
--------------------

Click the above `advanced` tab to see advanced settings.
Basic settings are using prefixed advanced settings. 
You can modify more detailed options.

Sheet work
^^^^^^^^^^^^

* Blank pages: This options set mode of blank page. This mode indicates the location that additional blank pages are added. Supported options are `back`, `front`, `both`. Default: `back`.
* Page range: Page range to modulation. You can use selected pages of orginal file to generate signature. You can combine independent single pages and page ranges. Example: `1-20, 23, 25, 40-100`. The total pages in page range will be calulated and shown next to input box. Beaware that if the given range string is not vaild (pages must be in right order and must not exceed max page range) , it deactivates `Generate` button below. Default: `1-{total pages of original file}`.
* Custom format: You can set custom paper format that does not listed in `Paper format` table. 
* Sig composition: You can set number of inserting per given number of sheets in signature. 
* Imposition: Pages located in same pages are merged to single page. Single signatures will be composed of two sequential pages in output file.
* Split: Save the output file with sepration by each signatures.

Printing markers
^^^^^^^^^^^^^^^^^^

* Signature proof: Add color proofs to each signatures. Their vertical locations are different by order of signature. You can easily check missing or misordered signatures.
* Trim: Add trim marker indicates original pages 
* Registration: Add cross registration black markers to left, right, top, bottom side.
* CMYK: Add square Cyan, Magenta, Yellow, Key(black) color markers to left side.

Generation
^^^^^^^^^^^^^^

Click `Generation` button, progress popup windows will appear and *ping* sound will notice the job finihed.



Command line
-------------

Same with gui method, but all those options are passed by argument.

.. code-block::

    usage: booklet [-h] [--version] [--format-help] [-i INPUT] [-o OUTPUT] [-n NAME] [--page-range [PAGE_RANGE ...]]
               [--blank-mode {back,front,both}] [--sig-composition SIG_COMPOSITION SIG_COMPOSITION]
               [--riffle-direction {right,left}] [--fold]
               [--format {Default,A3,A4,A5,B3,B4,B5,B6,JIS B3,JIS B4,JIS B5,JIS B6,Letter,Legal,Tabloid,GOV Letter,GOV Legal,ANSI A,ANSI B,ARCH A,ARCH B} | --custom-format CUSTOM_FORMAT CUSTOM_FORMAT]
               [--imposition] [--split] [--trim] [-reg] [--cmyk] [--sigproof [SIGPROOF]] [-y]
               [inputfile] [outputpath]

For example, if we transform the given pdf `input.pdf` to `signature.pdf` with 16 sheets signature composed of 4 sheets subsignature, marking signature proof to brown (hexcode = `#964B00`),

.. code-block::

    booklet input.pdf signature.pdf -sig-composition 4 4 --sigproof #964B00
