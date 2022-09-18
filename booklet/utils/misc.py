# Copyright (c) 2022, Hyunseong Kim <qwqwhsnote@gm.gist.ac.kr>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os, sys
from pathlib import Path
from typing import Union, Tuple, NoReturn
from tempfile import _TemporaryFileWrapper as TempFile
import tempfile

import webbrowser


# system related routine
def resources_path(rel_path: str, dir: str) -> str:
    """Get absolute resource path to use temper directory.

    :param rel_path: Relative path that used inside of codes
    :type rel_path: str
    :param dir: Subdirectory in project directory
    :type dir: str
    :return: Absolute path in execution environment for resource
    :rtype: str
    """
    # Get absolute path to resources, works for dev and for PyInstaller
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, dir, rel_path)


# Open webbrowser with a given url
def open_url(url: str) -> NoReturn:
    """Open the website of the given url with system default browser.

    :param url: URL
    :type url: str
    :return: Nothing
    :rtype: NoReturn
    """
    return webbrowser.open(url)


class NamedTempFile:
    """NamedTemporary file IO warpper for reading and writing"""

    def __init__(self, tempfile, mode=None, delete: bool = False):
        if tempfile.delete:
            raise ValueError("Named Temporary File must be in non-delete mode.")
        self.path = Path(tempfile.name)
        self.mode = tempfile.mode if mode == None else mode
        self.delete = delete if type(delete) == bool else False
        tempfile.close()
        # os.unlink(self.path)
        self.stream = open(self.path, self.mode)

    def __del__(self, *args):
        self.stream.close()
        if self.delete:
            try:
                os.unlink(self.path)
            except:
                pass

    def __exit__(self, *args):
        self.stream.close()
        if self.delete:
            try:
                os.unlink(self.path)
            except:
                pass

    @classmethod
    def from_temp_setting(cls, *args, **kwargs):
        kwargs["delete"] = False
        return cls(
            tempfile.NamedTemporaryFile(*args, **kwargs), mode="wb+", delete=True
        )

    @property
    def closed(self):
        return self.stream.closed

    def fileno(self):
        return self.stream.fileno()

    def truncate(self):
        return self.stream.truncate()

    def tell(self):
        return self.stream.tell()

    def isatty(self):
        return self.stream.isatty()

    def flush(self):
        return self.stream.flush()

    def seek(self, *args, **kwargs):
        return self.stream.seek(*args, **kwargs)

    def close(self):
        return self.stream.close()

    def readable(self):
        return self.stream.readable()

    def read(self, *args, **kwargs):
        return self.stream.read(*args, **kwargs)

    def readline(self, *args, **kwargs):
        return self.stream.readline(*args, **kwargs)

    def readlines(self, *args, **kwargs):
        return self.stream.readlines(*args, **kwargs)

    def writeable(self):
        return self.stream.writable()

    def write(self, *args, **kwargs):
        return self.stream.write(*args, **kwargs)

    def writeline(self, *args, **kwargs):
        return self.stream.writeline(*args, **kwargs)

    def writelines(self, *args, **kwargs):
        return self.stream.writelines(*args, **kwargs)


# Maybe deprecation is wise for further code.
def get_page_range(page_range_string: str) -> list:
    """Calculate exact range of pages for given formatted string.

        * All pages connected with comma, \',\'.
        * Each pages can be a single page number.
        * Multiple consequence pages can be represented with start page, hypen, and end page.

        Example:
            input: 1-5, 15, 19, 40-46
            return: 1,2,3,4,5,15,19,40,41,42,43,44,45,46

    :param page_range_string: Formatted string represent page range.
    :type page_range_string: str
    """
    page_range = page_range_string.replace(" ", "")

    rlist = []

    for st in page_range.split(","):
        if "-" in st:
            i, l = st.split("-")
            i = int(i)
            l = int(l)
            r = l - i + 1

            rlist = rlist + [i + d for d in range(0, r)]
        else:
            rlist.append(int(st))

    return rlist
