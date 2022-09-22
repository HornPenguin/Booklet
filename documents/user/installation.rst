
Installation
==================

HPBooklet provides 2 types of executable files for Windows, Linux(Ubuntu).
All the resources are fully independent to OS, therefore supporting OSX is possible.
However, the developer does not have any Mac device, so it will be presented later.
If you are OSX user you can build project yourself see below :ref:`From Source <from_source>` section.


Executable bunldle
--------------------

Download executable file from `Sourceforge <https://sourceforge.net/projects/hornpenguinbooklet/>`_.

.. raw:: html

    <a href="https://sourceforge.net/projects/hornpenguinbooklet/files/latest/download"><img alt="Download HornPenguin Booklet" src="https://a.fsdn.com/con/app/sf-download-button" width=276 height=48 srcset="https://a.fsdn.com/con/app/sf-download-button?button_size=2x 2x"></a>

Repository provides two types of program one file version and one directory bundle.
The directory bundle version of each OS is presented with compressed file, :code:`zip` and :code:`tgz` which are common compressed file format in each OS. 

Windows
^^^^^^^^^^^^^^^^

.. code-block:: 

    booklet.exe # one file version
    booklet_Windows.zip # one directory bundle

Linux
^^^^^^^^^^^^^^^^

.. code-block:: 

    booklet # one file version
    booklet_Linux.tgz # one directory bundle

OSX
^^^^^

Please build yourself or directly execute from sources. 
See the below section.

.. warning:: 

    Python is compatible for major three OSs, however, the implementations of tkinter in those OSs are different in details.
    For example, there is a :code:`iconbitmap` issue in Linux environment and basic tkiner Label and Button are not work properly in OSX of color routines.
    The developer tested and saw those bugs and fixed them with best efforts (`tkmacosx <https://github.com/Saadmairaj/tkmacosx>`_ module was useful), but there can be some bugs in Linux and Mac environments.
    Please notice the developer those bugs to fix.

Older version
^^^^^^^^^^^^^^^^^^^^^^

The 0.0.1 version was seperated by user interface. The graphic interface version got :code:`w` suffix in file name.

**Windows**

.. code-block:: 

    booklet.exe # command line interface
    bookletw.exe # graphic interface


**Linux**

.. code-block:: 

    booklet
    bookletw


From source
--------------------

.. _from_source:

This section describes the execution and build process with
source directory.

Get a project
^^^^^^^^^^^^^^^^^^^

You can download the project with git. 

.. code-block::

    git clone https://github.com/HornPenguin/Booklet.git # github 
    git clone https://git.code.sf.net/p/hornpenguinbooklet/code hornpenguinbooklet-code # sourceforge

or download with zipped file from project `source repository <https://github.com/HornPenguin/Booklet>`_
..

    **Directory**

    - :code:`booklet`: Python source codes.
    - :code:`dist`: Standalone executable files for OSs.
    - :code:`documents`: Sphinx rst documents
    - :code:`images`: Miscellaneous images, in working images or original :code:`.odg` files.
    - :code:`resources`: Essential resources for program, voice, images, logo, ... . 
    - :code:`test`: Temper test directory.

    **File**

    - :code:`.readthedocs.yaml`: Readthedocs setting file.
    - :code:`build.py`: Build script for Pyinstaller and Sphinx.
    - :code:`Makefile, make.bat`: Sphinx build script.

Dependencies
^^^^^^^^^^^^^^

* `PyPDF2 <https://pypdf2.readthedocs.io/>`_
* `reportlab <https://www.reportlab.com/>`_
* `Pillow <https://pillow.readthedocs.io/en/stable/>`_
* `simpleaudio <https://simpleaudio.readthedocs.io/en/latest/>`_
* `fonttools <https://github.com/fonttools/fonttools>`_
* `tkmacosc <https://pypi.org/project/tkmacosx/>`_: OSX specific dependency

Install above dependencies with next command. 

.. code-block:: 

    pip install PyPDF2 reportlab Pillow simpleaudio fonttools

For :code:`simpleaudio` in Ubuntu, it requires compilers, build tools, and prerequisite library, :code:`libasound2-dev`, to install. 
If you are using Ubuntu, you can install :code:`build-essential` from Ubuntu repository and install :code:`libasound2-dev` with next command.

.. code-block:: 
    
    sudo apt install build-essential libasound2-dev

In Mac, they are automatically installed. 


Execution with python 
^^^^^^^^^^^^^^^^^^^^^^^^

From the root of project directory,

CUI
""""""""""""""""""

.. code-block:: 

    python ./booklet/main.py --console {INPUT} {OUTPUTPAHT} {options}

See :ref:`usage <usage_label>` for options and basic usages.

GUI
""""""""""""""""""

.. code-block:: 

    python ./booklet/main.py 

Build
^^^^^^^^^^^^^^^^^^^^^^^^

This project uses `PyInstaller <https://pyinstaller.org/en/stable/>`_ as a build tool to generate a standalone executable bundle.
In the root of the project directory, there is a :code:`build.py` file. 
It is a simple python script to initiate the proejct and document build process with pyinstaller and sphinx.
Install Pyinstaller, befroe you start to build.

.. code-block::

    pip install pyinstaller

There are prefixed arguments in `build.py` and you can use additional pyinstaller arguments.
See PyInstaller `documents <https://pyinstaller.org/en/stable/>`_.

.. code-block:: 

    python build.py --onefile # one file bundle
    python build.py --onedir # one directory bundle

Build with graphic user interface *with splash image*.

.. code-block:: 

    python build.py --onefile --splash=resources\\splash.png
     

The :code:`--onedir` option add platform name to its directory name.

If you add arguments with :code:`--sphinx` option, :code:`build.py` automatically build project documents with sphinx.

.. code-block:: 

    python build.py --onedir --sphinx=html