# HornPenguin Booklet

**Version** 0.0.2

<p align="center">
  <img src="./documents/_static/main.png">
</p>

**HornPenguin Booklet** is a simple software generating booklet and signature for bookbinding from your pdf files.
You can print your own book signatures and simple pamplet with your home printer.

* Support diffence signature size from 4 to 32.
* Imposition layouts are supported for each type of signature.
* Change page size during generating signature.
* Left riffling direction is supported for old asian bookbinding.
* Printing markers; trim, CMYK, signature proof, ... .

See further details and usage examples in project [documents](https://docs.hornpenguin.com/projects/booklet/). 

[![Download HornPenguin Booklet](https://a.fsdn.com/con/app/sf-download-button)](https://sourceforge.net/projects/hornpenguinbooklet/files/latest/download)



## Quick Usage

See detailed descriptions in [Documentation](https://docs.hornpenguin.com/projects/booklet/en/latest/) 

### Execution

The executable files are in `dist` directory. 

There are two options *onefile* execution file and the compressed *onedir* file. The project supports for Windows, Linux, and OSX.
You must notice that the *onefile* files requires some time to execute at initial stage. To inform the executation, there is a splash window in the each *onefile* files, thanks to splash routine in [pyinstaller](https://pyinstaller.org/en/stable/).

* **Windows**

  ```
  booklet.exe # console program
  bbokletw.exe # GUI program
  ```

* **Linux**
  ```
  booklet # console program
  bbokletw # GUI program
  ```
* OSX

  No, but you can excute python source code.

or you can directly execute `main.py` or `mainw.py` with your python environment. Just check the prerequists in **Dependencies** section.
It is recommended if there are some errors in the execution files or you are using OSX. (I don't have Mac yet.)


### UI

<p align="center">
  <img src="images/ui_windows.png">
  <img src="images/ui__advanced_windows.png">
</p>


## Dependencies

* [reportlab](https://www.reportlab.com/)
* [PyPDF2](https://pypdf2.readthedocs.io/)
* [Pillow](https://pillow.readthedocs.io/en/stable/)
* [simpleaudio](https://simpleaudio.readthedocs.io/en/latest/)
* [tkmacosx](https://pypi.org/project/tkmacosx/) : Mac only

Install them with next command

```
pip install PyPDF2 reportlab Pillow simpleaudio
```

For `simpleaudio`, it requires compilers, build tools and prerequest library `libasound2-dev` to install the module. 
If you are using Ubuntu you can install `build-essential` from repository.

```
sudo apt install build-essential libasound2-dev
```

## Contribution

See guides and rules in [Developer guide document](https://docs.hornpenguin.com/projects/booklet/en/latest/develop/guide.html)

## Further routines

Further routines for next version

**Simple**

* Add more color markers - Done
* Precious setting of rectangle object -Done

**Little troublesome**

* Converting PDF with image before transformation.(some pdfs are broken in their fonts or positions of elements during transformation) -Done
  Additional libraries are too heavy...

**Annoying**

1. Dealing multiple PDFs at once.
2. PDF preview for original and signature(UI.... :<).

## License

This program distributed under BSD 3-clause license
See detail license text in [LICENSE](LICENSE) file in repository.
