===============
Installation
===============

HPBooklet provides 3 types of executable files for Windows, Linux(Ubuntu), and OSX.
Basically, we offer two types of program, *command line* interface and *GUI* interface.

Command interface
====================



Windows, Linux
------------------

Download executable file from `Sourceforge <https://sourceforge.net/projects/hornpenguinbooklet/>`_.

.. raw:: html

    <a href="https://sourceforge.net/projects/hornpenguinbooklet/files/latest/download"><img alt="Download HornPenguin Booklet" src="https://a.fsdn.com/con/app/sf-download-button" width=276 height=48 srcset="https://a.fsdn.com/con/app/sf-download-button?button_size=2x 2x"></a>

**Windows**

.. code-block:: 

    booklet.exe # command line interface
    bookletw.exe # graphic interface


**Linux**

.. code-block:: 

    booklet
    bookletw

OSX
------

The developer does not have a Mac computer. (ㅜㅜ, :<)
Please build yourself or directly execute from sources. 
See the below section.

.. warning:: 

    Python is compatible for major three OSs, however, the implementations of tkinter in those OSs are different in details.
    For example, there is a :code`iconbitmap` issue in Linux environment and basic tkiner Label and Button are not work properly in OSX of color routines.
    The developer tested and saw those bugs and fixed them with best efforts (`tkmacosx` module was useful), but there can be some bugs in Linux and Mac environments.
    Please notice the developer those bugs to fix.



From source
--------------------

This section describes the execution and build process with
source directory.

Structure of project directory
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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
* `tkmacosc <https://pypi.org/project/tkmacosx/>`_: OSX specific dependency

Install above dependencies with next command. 

.. code-block:: 

    pip install PyPDF2 reportlab Pillow simpleaudio

For :code:`simpleaudio` in Ubuntu, it requires compilers, build tools, and prerequisite library :code:`libasound2-dev` to install. 
If you are using Ubuntu you can install :code:`build-essential` from repository.

.. code-block:: 
    
    sudo apt install build-essential libasound2-dev

In Mac, they are automatically installed. 


Execution with python 
^^^^^^^^^^^^^^^^^^^^^^^^

From the root of project directory,

**Command line**

.. code-block:: 

    python ./booklet/main_console.py {INPUT} {OUTPUTPAHT} {options}

See :ref:`usage <usage_label>` for options and basic usages.

**GUI**

.. code-block:: 

    python ./booklet/main.py 

Build
^^^^^^^^^^^^^^^^^^^^^^^^

This project uses pyinstaller as a build tool to generate a standalone executable files.
In the root, there is a :code:`build.py`. It is a simple python script to initiate the build process.

It needs *pyinstaller*. You can install it with next command,

.. code-block::

    pip install pyinstaller

There are prefixed arguments in `build.py` and you can use additional pyinstaller arguments.

Build with command line interface

.. code-block:: 

    python build.py --console --onefile


.. code-block:: 

    python build.py --console --onedir

Build with graphic user interface *with splash image*.

.. code-block:: 

    python build.py --onefile --splash=resources\\splash.png
     
.. code-block:: 

    python build.py --onedir 

The :code:`--onedir` option automatically add platform name to its directory name.


If you add arguments with :code:`--sphinx` option, :code:`build.py` automatically build project documents with sphinx.

Example
.. code-block:: 

    python build.py --onedir --sphinx=html