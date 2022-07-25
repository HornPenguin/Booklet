.. _usage_label:

Usage
===============


Basic
------------

Select PDF file to modulate
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. image:: _static/select_file001.png

Click the grey button with :code:`...` notation on right of intputbox to choose manuscript.
Otherwise, you can type file path directly to input box including file name, but it is not recommended. 


.. image:: _static/select_file002.png

In this example, we chose :code:`test.pdf` file. 
HornPenguin Booklet automatically detects meta datas, title, authors, and pages, of the given pdf files.
In cui, just typing path of selected pdf file.

Basic Settings
^^^^^^^^^^^^^^^^

.. image:: _static/output_setting001.png

*Output path* is a directory path that output file wil be saved, Default value is the path of original file.
You can modify it with clicking grey button, :code:`...`, or directly modify path string in inputbox.


*File name* is a name of output file. Default value is :code:`{original file name}_HP_BOOKLET.pdf`. 
You can modify it, but beaware that it does not check existence of given file. 
If there is same file in output path, it will be overwritten by the new file. 

.. image:: _static/output_setting002.png

*Leaves* is a number of sheets per each signatures. 
When you choose specific number of sheets, additional blank pages will be shown right to selection box.
In this case, manuscript file has 32 number of sheets, so it will be 0 for 4, 8, 16, 32 number of sheets.
In the list of sheet numbers, you can see some numbers have a subfix :code:`f`.
:code:`f` indicates fold support numbers. if you select one of those numbers, the fold check will be activated.


* Book Format: Page dimension of output file. Default: original page size. See dimension(mm) in above `Help` -> `Paper Format` reference.
* Fold: Fold option is restricted to some special sheet numbers and they are notated "{number}f"
* Riffling: Riffle direction of output file. Default: `right`. `left` is for old Asian, Arabic, and Hebrew manuscript.


.. image::_static/output_setting001.png



 
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
