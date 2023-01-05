# http://pyrocko.org - GPLv3
#
# The Pyrocko Developers, 21st Century
# ---|P------/S----------~Lg----------

import numpy as num

from pyrocko.guts import Object, Timestamp
from pyrocko.guts_array import Array

from pyrocko.gato.grid.base import Grid


class DelayMethod(Object):
    pass


class GenericDelayTable(Object):
    source_grid = Grid.T()
    receiver_grid = Grid.T()
    method = DelayMethod.T()
    reference_time = Timestamp.T(optional=True)
    source_delays = Array.T(optional=True, shape=(None,), dtype=num.float64)
    receiver_delays = Array.T(optional=True, shape=(None,), dtype=num.float64)

    def __init__(self, **kwargs):
        Object.__init__(self, **kwargs)
        self.clear_cached()

    def clear_cached(self):
        self._delays = None

    def get_delays(self):
        if self._delays is None:
            delays = self.method.calculate(
                self.source_grid, self.receiver_grid)

            if self.reference_time is not None:
                delays -= self.reference_time

            if self.receiver_delays is not None:
                delays += self.receiver_delays[num.newaxis, :]

            if self.source_delays is not None:
                delays += self.source_delays[:, num.newaxis]

            self._delays = delays

        return self._delays


__all__ = [
    'DelayMethod',
    'GenericDelayTable',
]
