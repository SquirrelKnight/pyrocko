# http://pyrocko.org - GPLv3
#
# The Pyrocko Developers, 21st Century
# ---|P------/S----------~Lg----------

import numpy as num
from .base import DelayMethod


class PlaneWaveDM(DelayMethod):
    def calculate(self, source_grid, receiver_grid):
        slownesses = source_grid.get_nodes('ned')
        ned = receiver_grid.get_nodes('ned')
        return num.sum(
            slownesses[:, num.newaxis, :] * ned[num.newaxis, :, :], axis=2)


__all__ = [
    'PlaneWaveDM',
]
