import sys

from tkinter import Button as tk_Button
from tkinter import W, E, N, S, BOTH, LEFT, RIGHT, CENTER
from tkinter import StringVar, IntVar, DoubleVar, BooleanVar
from tkinter import DISABLED, ACTIVE
from tkinter import filedialog, Canvas

from tkinter.ttk import Button, Label, Frame, Entry, Treeview, Scrollbar
if sys.platform.startswith("darwin"):
    from tkmacosx import Button