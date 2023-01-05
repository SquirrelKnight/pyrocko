# http://pyrocko.org - GPLv3
#
# The Pyrocko Developers, 21st Century
# ---|P------/S----------~Lg----------

from pyrocko.guts import Float

from .base import DelayMethod
from pyrocko.gato.grid.location import distances_3d


class SphericalWaveDM(DelayMethod):
    velocity = Float.T()

    def calculate(self, source_grid, receiver_grid):
        return distances_3d(source_grid, receiver_grid) / self.velocity


__all__ = [
    'SphericalWaveDM',
]
