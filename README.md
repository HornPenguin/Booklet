# HornPenguin Booklet

![HornPenguinBooklet](images/Logo.svg)

HornPenguin Booklet is a simple software that generates booklet and signature for bookbinding from your pdf files.
You can print your own book signatures and simple pamplet with your home printer.

* Support diffence signature size from 4 to 32.
* Fold signature is supported for special number of leaves (8, 16, 32).
* Change page size during generating signature.
* Left riffling direction is supported for old asian bookbinding.

## Layout of signatue

The signature in bookbing is a collection of sheets that is an unit of contents.
Book can consists of single signature or multiple signatures. 

For single sheet binding, for example traditional asian binding, you just print manuscript with double side print option
and bind them. However, for folded signature, you need to rearrange the pages of the pdf.

The order of the pages depend on the number of sheet per each signature. 
See layout of signatures for 4, 6, 8

## UI and Usage

Version 1.0.0

### Manuscript Frame

1. File selector: Choose original file.
2. Title, Author(s), Pages, Format: Automatically detect metadata of the selected pdf file. They will be remianed in generated signature or booklet file. 

### Output Frame

1. Output directory: Generated file location.
2. File name: Choose file name of output. Initial value is original file. 
3. Leaves: Number of leabes per signature. 'f' suffix means fold support number.
4. Book Format: Output page size. 'Default' value remains original size. See other ISO dimensions of format in 'Help' -> 'Format' above menu.
5. Fold: Option for fold signature. Pages will be rotated and rearranged for folding. (Not supported yet)
6. Riffling direction: Default is 'right' value. 'left' value is for an traditional asian bookbinding which riffles from right to left. 

<p align="center">
  <img width="300" height="470" src="images/ui.PNG">
</p>


## Dependency

Configurtion

* UI: Tkinter
* PDF manipulation: PyPDF2(external library, BSD-3 licensed, )


## License

This program distributed under BSD-3 license
See detail license text in "LICENSE" file in repository.
