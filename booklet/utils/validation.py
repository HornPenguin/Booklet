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

from __future__ import annotations

from typing import Union, NoReturn
from pathlib import Path
from numbers import Number 


def check_path(_path:Union[str, Path], mode:str) -> bool:
    """_summary_

    :param _path: _description_
    :type _path: Union[str, Path]
    :param mode: _description_
    :type mode: str
    :return: :code:`True` or :code:`False`
    :rtype: bool
    """
    try:
        path(_path, mode)
        return True
    except:
        return False
def path(_path:Union[str, Path], mode:str="f") -> NoReturn:
    """_summary_

    :param _path: _description_
    :type _path: Union[str, Path]
    :param mode: _description_, defaults to "f"
    :type mode: str, optional
    :raises TypeError: The given argument is not a string and path object
    :raises ValueError: No such file or directory exists.
    :raises ValueError: Invaild file path, not a file.
    :raises ValueError: Invaild directory path, not a directory.
    :return: _description_
    :rtype: NoReturn
    """
    if type(_path) == str:
        _path = Path(_path)
     # type check--------------------------
    if not isinstance(_path, Path): 
        raise TypeError("The given argument is not a string and path object")
    # file, directory check---------------
    if not _path.exists:
        raise ValueError(f"No such file or directory exists. {str(_path)}")
    if mode=='f' and not _path.is_file():
        raise ValueError(f"Invaild file path, not a file. {str(_path)}")
    elif mode =='d' and not _path.is_dir():
        raise ValueError(f"Invaild directory path, not a directory. {str(_path)}")
def check_integer(i:int, positive:bool=False) -> bool:
    """_summary_

    :param i: _description_
    :type i: int
    :param positive: _description_, defaults to False
    :type positive: bool, optional
    :return: :code:`True` or :code:`False`
    :rtype: bool
    """
    try: 
        integer(i, positive)
        return True
    except:
        return False
def integer(i:Union[str, Number], positive:bool=False) -> NoReturn:
    """_summary_

    :param i: Unknown value
    :type i: int
    :param positive: Additional check, whether the given value is positive or not, defaults to False
    :type positive: bool, optional
    :raises TypeError: Not an integer object or integer string.
    :raises ValueError: Not a positive value.
    :return: None
    :rtype: NoReturn
    """
    if type(i) == str:
            try:
                i = int(i)
            except:
                raise TypeError(f"Not an integer object or integer string. {type(i)}_{i}")
    if type(i) == int:
        if i<0 and positive:
            raise ValueError(f"Not a positive value. {i}")

def check_number(i:Union[str, Number], positive=False) -> bool:
    """Validate the type of the given value and its sign whether positive or negative. Return boolean value.

    :param i: Unknown value
    :type i: Union[str, Number]
    :param positive: Additional check, whether the given value is positive or not, defaults to False
    :type positive: bool, optional
    :return: :code:`True` or :code:`False`
    :rtype: bool
    """
    try:
        number(i, positive)
        return True
    except:
        return False
def number(i:Union[str, Number], positive=False) -> NoReturn:
    """Validate the type of the given value and its sign whether positive or negative. Raise error.

    :param i: Unknown value
    :type i: Union[str, Number]
    :param positive: Additional check, whether the given value is positive or not, defaults to False
    :type positive: bool, optional
    :raises ValueError: Invaild string, not even a float number
    :raises ValueError: Invaild string, not an integer
    :raises TypeError: Invaild type
    :raises ValueError: Not a positive value.
    :return: None
    :rtype: NoReturn
    """
    if type(i) == str:
        if '.' in i:
            try:
                i = float(i)
            except:
                raise ValueError("Invaild string, not even a float number")
        else:
            try:
                i = int(i)
            except:
                raise ValueError("Invaild string, not an integer")
    if not isinstance(i, Number):
        raise TypeError(f"Invaild type: {type(i)}_{i}")
    
    if i<0 and positive == False:
        raise ValueError(f"Not a positive value. {i}")


if __name__ == "__main__":

    tests = ["1230", "12.30", "2123.d0", 1231, int(210), "214s12"]
    for test in tests:
        print(f"{test}, {type(test)}")
        print(f"result:{check_number(test, True)}")



