from __future__ import annotations
import sys
from typing import Union, Tuple, NoReturn

sys.path.append("..")
sys.path.append(".")


from itertools import permutations

from booklet.utils import split_list

# Permutations and generating functions for signature routines-------------------------
class Permutation:
    @classmethod
    def get_permutations(
        cls, n: int, per=False
    ) -> list:  # get list of permutations for given 'n'
        per = permutations(range(1, n + 1), n)
        if per:
            return [cls(n, p) for p in per]
        else:
            return [p for p in per]

    @classmethod
    def reverse_permutation(cls, n: int) -> Permutation:
        return cls(n, range(n, 0, -1))

    @classmethod
    def subpermutation_to_list_index(cls, per: Permutation, li: list) -> list:
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

    def __mul__(self, other: Permutation) -> Permutation:
        if self.n != other.n:
            raise ValueError(f"{self.n} and {other.n} are not same.")

        rlist = [other[x] for x in self.plist]
        return Permutation(self.n, rlist)

    def index_mul(self, other: Permutation, oper=False) -> Union[list, Permutation]:

        rlist = [self[x] for x in other.plist]
        if oper:
            self.plist = rlist
        else:
            return Permutation(self.n, rlist)

    def index_mul_partial(
        self, sub_permutation: Permutation, oper: bool = False
    ) -> Union[list, Permutation]:  # Work on indexing
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

    def permute_to_list_index(self, li: list) -> list:
        if not hasattr(li, "__iter__"):
            li = [li]
        if len(li) != self.n:
            raise ValueError(f"{len(li)} ! = {self.n}")

        rlist = [li[x - 1] for x in self.plist]
        return rlist

    def inverse(self) -> Permutation:
        ilist = [self.plist.index(x) + 1 for x in range(1, self.n + 1)]
        return Permutation(self.n, ilist)

    def notation_cauchy(self) -> str:
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
    ) -> Union[str, list]:
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
