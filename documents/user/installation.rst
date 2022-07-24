===============
Installation
===============

HPBooklet provides 3 types of executable files for Windows, Linux(Ubuntu), and OSX.
Basically, we offer two type of program, *command line* interface and *gui* interface.

Command interface
====================



Windows, Linux
------------------

Download executable file [SourceForge project page](https://sourceforge.net/projects/hornpenguinbooklet/).

**Windows**

.. code-block:: 

    booklet.exe # command line interface
    bookletw.zip # graphic interface


**Linux**

.. code-block:: 

    booklet
    bookletw

OSX
------
Dveloper does not have any Mac computer. (ㅜㅜ, :<)
Please build or ditectly execute from source.



From source
--------------------

This section describes execution and build process with
source directory.

**Directory**

- :code:`booklet`: python source codes.
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

Install above dependencies with next command. 

.. code-block:: 

    pip install PyPDF2 reportlab Pillow simpleaudio

For :code:`simpleaudio` in Ubuntu, it requires compilers, build tools and prerequest library :code:`libasound2-dev` to install. 
If you are using Ubuntu you can install :code:`build-essential` from repository.

.. code-block:: 
    
    sudo apt install build-essential libasound2-dev

In Mac, they are automatically installed. 

Execution with python 
^^^^^^^^^^^^^^^^^^^^^^^^

From the root of project directory,

**Command line**

.. code-block:: 

    python ./booklet/main_console.py 

See :ref:`usage <usage_label>` for options and basic usages.

**GUI**

.. code-block:: 

    python ./booklet/main.py 

Build
^^^^^^^^^^^^^^^^^^^^^^^^

This project uses pyinstaller as a build tool to generate standalone executable file.
In the root, there is a :code:`build.py`. It is a simple python script to initiate build process.

It needs *pyinstaller*. You can install it with next command,

.. code-block::

    pip install pyinstaller

There are prefixed arguments in `build.py` and you can use additional pyinstaller arguments.

Build with command line interface

.. code-block:: 

    python build.py --console --onefile


.. code-block:: 

    python build.py --console --onedir

Build with graphic user interface

*with splash image*.

.. code-block:: 

    python build.py --onefile --splash=resources/splash.png

.. code-block:: 

    python build.py --onedir 

The :code:`--onedir` option automatically add platform name to its directory name.


If you add arguments with :code:`--sphinx` option, :code:`build.py` automatically build project documents with sphinx.

Example
.. code-block:: 

    python build.py --onedir --sphinx=html