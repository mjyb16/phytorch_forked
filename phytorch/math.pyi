from numbers import Number
from typing import overload

from torch import Tensor


@overload
def realise(x: Number) -> Number: ...
@overload
def realise(x: Tensor) -> Tensor: ...

@overload
def complexify(x: Number) -> Number: ...
@overload
def complexify(x: Tensor) -> Tensor: ...

@overload
def where(cond: bool, x: Number, y: Number) -> Number: ...
@overload
def where(cond: Tensor, x: Tensor, y: Tensor) -> Tensor: ...

@overload
def sinc(x: Number) -> Number: ...
@overload
def sinc(x: Tensor) -> Tensor: ...

@overload
def csinc(x: Number, eps: Number = 1e-8) -> Number: ...
@overload
def csinc(x: Tensor, eps: Number = 1e-8) -> Tensor: ...

@overload
def exp(x: Number) -> Number: ...
@overload
def exp(x: Tensor) -> Tensor: ...

@overload
def log10(x: Number) -> Number: ...
@overload
def log10(x: Tensor) -> Tensor: ...

@overload
def sin(x: Number) -> Number: ...
@overload
def sin(x: Tensor) -> Tensor: ...

@overload
def asinh(x: Number) -> Number: ...
@overload
def asinh(x: Tensor) -> Tensor: ...
