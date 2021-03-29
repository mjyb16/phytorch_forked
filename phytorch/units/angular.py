from math import pi

from ._utils import AutoCleanupGlobalScope
from .prefixes import micro_, milli_
from .Unit import Unit


with AutoCleanupGlobalScope():
    radian = rad = Unit(name='rad')
    steradian = sr = (rad**2).set_name('sr')

    degree = deg = (180/pi * rad).set_name('deg')
    arcmin = (deg / 60).set_name('arcmin')
    arcsec = (arcmin / 60).set_name('arcsec')
    milliarcsec = mas = milli_(arcsec).set_name('mas')
    microarcsec = uas = μas = micro_(arcsec).set_name('uas')

    cycle = (2*pi * rad).set_name('cycle')
    spat = (4*pi * sr).set_name('spat')
