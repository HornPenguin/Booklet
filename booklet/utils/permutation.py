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
import sys
sys.path.append("..")
sys.path.append(".")
from typing import Union,  NoReturn


from itertools import permutations
from booklet.utils.matrix import split_list

# Permutations routine and utils
class Permutation:
    """Permutation implementation"""
    @classmethod
    def get_permutations(
        cls, n: int, per=False
    ) -> Union[list[Permutation], list[list[int]]]:  # get list of permutations for given 'n'
        """Return all permuation of length :math:`n`. Based on standard permutation routine in :code:`itertools`.

        :param n: Length of permuatation. Bigger than 0
        :type n: int
        :param per: Return type determinator. :code:`True`, :class:`booklet.permutation.Permutation` , :code:`False`, :code:`list`. Default = :code:`False`.
        :type per: bool, optional
        :return: list of length :math:`n` permutations.
        :rtype: Union[list[Permutation], list[list[int]]]
        """

        per = permutations(range(1, n + 1), n)
        if per:
            return [cls(n, p) for p in per]
        else:
            return [p for p in per]
    @classmethod
    def from_lists(cls, lists:Union[list[int], list[list[int]]]) -> Permutation:
        """Generate :class:`booklet.permutation.Permutation` from lists

        :param lists: list of integers or list of integer lists. In other words, 1-dim and 2-dim integer arrays are supported
        :type lists: Union[list[int], list[list[int]]]
        :return: Permutation defined from all element of the given list. Order is preserved and for 2-dim array, it follows row-major order.
        :rtype: Permutation
        """
        l = []
        for li in lists:
            if type(li) == list:
                l += li 
            else:
                l.append(li)  
        n = len(l)
        return cls(n, l)
    @classmethod
    def reverse_permutation(cls, n: int) -> Permutation:
        """Do not confuse with *inverse* permutation. 
        It only reverses order of 1 step increasing permutation. 
        For example, :code:`reverse_permutation(3) == Permutation(3,[3, 2, 1])`.

        :param n: length of permutation
        :type n: int
        :return: Reverse permutation of length :math:`n`. 
        :rtype: Permutation
        """
        return cls(n, range(n, 0, -1))

    @classmethod
    def subpermutation_to_list_index(cls, per: Permutation, li: list) -> list:
        """Applying permutation to larger length list literally.

        :param per: _description_
        :type per: Permutation
        :param li: _description_
        :type li: list
        :raises ValueError: _description_
        :raises ValueError: _description_
        :return: _description_
        :rtype: list
        """
        if per.n > len(li):
            raise ValueError(
                f"Permutation length is longer than list. {per.n}, {len(li)}"
            )

        if len(li) % per.n != 0:
            raise ValueError(
                f"Permutation length must be a divider of list length. {per.n}, {len(li)} "
            )

        split = split_list(li, per.n)
        rlist = []
        for subli in split:
            rlist = rlist + per.permute_to_list_index(subli)

        return rlist

    def __init__(self, n: int, plist: list) -> NoReturn:
        if len(plist) != n:
            raise ValueError(f"{n} must be same with len(plist) = {len(plist)}")

        if sum(plist) != int(n * (n + 1) / 2):
            raise ValueError(
                f"plist does not satisfy permutation proeprty.\n All [1, n] values must be in plist. \n {plist}"
            )

        self.n = n
        if type(plist) == int:
            self.plist = [1]
        else:
            self.plist = plist

    def __getitem__(self, key: int) -> list:
        if type(key) != int:
            raise ValueError(f"key must be an integer type element: {key}")
        if key < 1 or key > self.n:
            raise IndexError(f"{key} must be in [1, {self.n}] range.")

        return self.plist[key - 1]

    def __mul__(self, other: Permutation) -> Permutation: # p3 = p1*p2
        if self.n != other.n:
            raise ValueError(f"{self.n} and {other.n} are not same.")

        rlist = [other[x] for x in self.plist]
        return Permutation(self.n, rlist)

    def index_mul(self, other: Permutation, oper=False) -> Union[list, Permutation]: # Direction is reverse from `*`
        rlist = [self[x] for x in other.plist]
        if oper:
            self.plist = rlist
        else:
            return Permutation(self.n, rlist)

    def index_mul_partial(
        self, sub_permutation: Permutation, oper: bool = False
    ) -> Union[list, Permutation]:  # Same with `index_mul` but literally work by sub permutation
        if not isinstance(sub_permutation, Permutation):
            raise ValueError(
                f"Given parameter must be 'Permutation' object. \n Current object:{type(sub_permutation)}"
            )
        if self.n % sub_permutation.n != 0:
            raise ValueError(
                f"Sub permutation must have a divisor of main permuatain size as its size\n main:{self.n}, sub:{sub_permutation.n}"
            )

        n = int(self.n / sub_permutation.n)
        m = sub_permutation.n

        rlist = []
        for i in range(0, n):
            tem_rlist = [self.plist[x + m * i - 1] for x in sub_permutation.plist]
            rlist = rlist + tem_rlist

        if oper:
            self.plist = rlist
        else:
            return Permutation(self.n, rlist)

    def permute_to_list_index(self, li: list) -> list: # Applying permutation to the given list
        if not hasattr(li, "__iter__"):
            li = [li]
        if len(li) != self.n:
            raise ValueError(f"{len(li)} ! = {self.n}")

        rlist = [li[x - 1] for x in self.plist]
        return rlist

    def inverse(self) -> Permutation: # p * p.inverse() = identity permutation
        ilist = [self.plist.index(x) + 1 for x in range(1, self.n + 1)]
        return Permutation(self.n, ilist)

    def notation_cauchy(self) -> str: # Get Cauchy representation of permutation
        return f"{list(range(1, self.n+1))}\n{self.plist}"

    def __canocial_order(self, cyclist: list) -> list:
        c_clist_1 = []
        c_clist_2 = []
        for li in cyclist:
            n = len(li)
            nmax = li.index(max(li))
            c_clist_1.append([li[x] for x in range(nmax - n, nmax)])
        maxindex = [x[0] for x in c_clist_1]
        s_index = sorted(maxindex)

        for i in s_index:
            c_clist_2.append(c_clist_1[maxindex.index(i)])

        return c_clist_2

    def notation_cyclic(
        self, canonical: bool = False, string: bool = False, sep: str = ""
    ) -> Union[str, list]: # Get cyclic representation of permutation
        cycliclist = []
        index = list(range(1, self.n + 1))
        i = 1

        while True:
            ilist = []
            ilist.append(i)
            index.remove(i)

            sig_i = self[i]
            while sig_i in index:
                ilist.append(sig_i)
                index.remove(sig_i)
                sig_i = self[sig_i]

            cycliclist.append(ilist)

            if len(index) > 0:
                i = min(index)
            else:
                break
        if canonical:
            cycliclist = self.__canocial_order(cycliclist)

        if string:
            cycstr = ""
            for li in cycliclist:
                cycstr = cycstr + "(" + f"{sep}".join(map(str, li)) + ")"
            return cycstr
        else:
            return cycliclist
