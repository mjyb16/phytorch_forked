from dataclasses import dataclass
from functools import cache, cached_property
from typing import Sequence, TypeVar, Union

from more_itertools import always_iterable
# from mpmath import elliprc, elliprf, elliprj, elliprd
from phytorch.special import elliprf, elliprc, elliprj, elliprd


_T = TypeVar('_T')
_t = float


@dataclass(frozen=True)
class OneIndexedSequence(Sequence[_T]):
    seq: Sequence[_T]

    def __len__(self) -> int:
        return len(self.seq)

    def __getitem__(self, item):
        return self.seq[item-1]


@dataclass(frozen=True)
class OneIndexedFormula:
    a: OneIndexedSequence[_T]
    b: OneIndexedSequence[_T]

    def formula(self, *args):
        raise NotImplementedError

    @cache
    def __getitem__(self, item):
        return self.formula(*always_iterable(item))


class d(OneIndexedFormula):
    def formula(self, i, j):
        return (
            -self.formula(j, i) if j<i else
            self.b[j] if i==0 else
            self.a[i] * self.b[j] - self.a[j] * self.b[i]
        )


@dataclass(frozen=True)
class XorY(OneIndexedFormula):
    def formula(self, i):
        return 1 if i == 0 else (self.a[i] + self.b[i]*self.xory)**0.5

    xory: _t


@dataclass(unsafe_hash=True)
class EllipticReduction:
    x: _t
    y: _t
    a: Union[OneIndexedSequence[_t], Sequence[_t]]
    b: Union[OneIndexedSequence[_t], Sequence[_t]]
    h: int = 4

    @cached_property
    def n(self):
        return len(self.a)

    def __post_init__(self):
        if not isinstance(self.a, OneIndexedSequence):
            self.a = OneIndexedSequence(self.a)
        if not isinstance(self.b, OneIndexedSequence):
            self.b = OneIndexedSequence(self.b)

    @cached_property
    def d(self):
        return d(self.a, self.b)

    @cached_property
    def X(self):
        return XorY(self.a, self.b, self.x)

    @cached_property
    def Y(self):
        return XorY(self.a, self.b, self.y)

    @cache
    def U2(self, i: int, j: int):
        if j < i:
            return self.U2(j, i)
        elif i==3 and j==4:
            return self.U2(1, 2)
        elif i==1 and j==2:
            k, l = 3, 4
            return ((self.X[i]*self.X[j] * self.Y[k]*self.Y[l] + self.Y[i]*self.Y[j] * self.X[k]*self.X[l]) / (self.x - self.y))**2
        else:
            k, l = {1, 2, 3, 4} - {i, j}
            return self.d[i, l]*self.d[j, k] + self.U2(i, k)

    @cache
    def U2nu(self, i: int, nu: int):
        j, k, l = {1, 2, 3, 4} - {i}
        return self.U2(i, j) - self.d[i, k] * self.d[i, l] * self.d[j, nu] / self.d[i, nu]

    @cache
    def S2(self, i, nu):
        j, k, l = {1, 2, 3, 4} - {i}
        return ((self.X[j]*self.X[k]*self.X[l] / self.X[i] * self.Y[nu]**2 + self.Y[j]*self.Y[k]*self.Y[l] / self.Y[i] * self.X[nu]**2) / (self.x - self.y))**2

    @cache
    def Q2(self, i, nu):
        return self.X[nu]**2 * self.Y[nu]**2 / (self.X[i]**2 * self.Y[i]**2) * self.U2nu(i, nu)

    @cache
    def Ie(self, i: int):
        if abs(i) > self.n:
            raise ValueError(f'-{self.n} <= i <= {self.n}')
        if i < -self.h:
            i, j, k, l, nu = (1, 2, 3, 4, -i)
            return (2 * self.b[nu] * (self.d[i, j]*self.d[i, k]*self.d[i, l] / self.d[i, nu] / 3 * elliprj(self.U2(1, 2), self.U2(1, 3), self.U2(2, 3), self.U2nu(i, nu)) + elliprc(self.S2(i, nu), self.Q2(i, nu))) - self.b[i]*self.Ie(0)) / self.d[i, nu]
        elif i < 0:
            i = -i
            j, k, l = {1, 2, 3, 4} - {i}
            return (2*self.b[i] * (self.d[j, k]*self.d[j, l]/3 * elliprd(self.U2(i, k), self.U2(j, k), self.U2(i, j)) + self.X[j]*self.Y[j] / (self.X[i]*self.Y[i]*self.U2(i, j)**0.5)) - self.b[j] * self.Ie(0)) / self.d[j, i]
        elif i==0:
            return 2*elliprf(self.U2(1, 2), self.U2(1, 3), self.U2(2, 3))
        elif i <= self.h:
            j, k, l = {1, 2, 3, 4} - {i}
            return 2 * (
                self.d[i, j] * self.d[i, k] * self.d[l, i] * elliprj(self.U2(1, 2), self.U2(1, 3), self.U2(2, 3), self.U2nu(i, 0)) / 3 / self.b[i]
                + elliprc(self.S2(i, 0), self.Q2(i, 0))
            )
        elif i <= self.n:
            return (self.b[i] * self.Ie(1) + self.d[i, 1] * self.Ie(0)) / self.b[1]

