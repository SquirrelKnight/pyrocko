# http://pyrocko.org - GPLv3
#
# The Pyrocko Developers, 21st Century
# ---|P------/S----------~Lg----------
from __future__ import annotations

import math

import numpy as num
from pyrocko import orthodrome
from pyrocko.guts import Float, Object

guts_prefix = 'pf'

d2r = math.pi / 180.
r2d = 1.0 / d2r
km = 1000.


def latlondepth_to_cartesian(lat, lon, depth):
    return orthodrome.geodetic_to_ecef(lat, lon, -depth)


class Location(Object):
    '''
    Geographical location.

    The location is given by a reference point at the earth's surface
    (:py:attr:`lat`, :py:attr:`lon`, :py:attr:`elevation`) and a cartesian
    offset from this point (:py:attr:`north_shift`, :py:attr:`east_shift`,
    :py:attr:`depth`). The offset corrected lat/lon coordinates of the location
    can be accessed though the :py:attr:`effective_latlon`,
    :py:attr:`effective_lat`, and :py:attr:`effective_lon` properties.
    '''

    lat = Float.T(
        default=0.0,
        optional=True,
        help='latitude of reference point [deg]')

    lon = Float.T(
        default=0.0,
        optional=True,
        help='longitude of reference point [deg]')

    north_shift = Float.T(
        default=0.,
        optional=True,
        help='northward cartesian offset from reference point [m]')

    east_shift = Float.T(
        default=0.,
        optional=True,
        help='eastward cartesian offset from reference point [m]')

    elevation = Float.T(
        default=0.0,
        optional=True,
        help='surface elevation, above sea level [m]')

    depth = Float.T(
        default=0.0,
        help='depth, below surface [m]')

    def __init__(self, **kwargs):
        Object.__init__(self, **kwargs)
        self._latlon = None

    def __setattr__(self, name, value):
        if name in ('lat', 'lon', 'north_shift', 'east_shift'):
            self.__dict__['_latlon'] = None

        Object.__setattr__(self, name, value)

    @property
    def effective_latlon(self):
        '''
        Property holding the offset-corrected lat/lon pair of the location.
        '''

        if self._latlon is None:
            if self.north_shift == 0.0 and self.east_shift == 0.0:
                self._latlon = self.lat, self.lon
            else:
                self._latlon = tuple(float(x) for x in orthodrome.ne_to_latlon(
                    self.lat, self.lon, self.north_shift, self.east_shift))

        return self._latlon

    @property
    def effective_lat(self):
        '''
        Property holding the offset-corrected latitude of the location.
        '''

        return self.effective_latlon[0]

    @property
    def effective_lon(self):
        '''
        Property holding the offset-corrected longitude of the location.
        '''

        return self.effective_latlon[1]

    def same_origin(self, other):
        '''
        Check whether other location object has the same reference location.
        '''

        return self.lat == other.lat and self.lon == other.lon

    def distance_to(self, other):
        '''
        Compute surface distance [m] to other location object.

        :param other: Other location.
        :type other: :py:class:`~pyrocko.model.location.Location`

        :return: Distance to another location in [m].
        :rtype: float
        '''

        if self.same_origin(other):
            other_north_shift, other_east_shift = get_offset(other)

            return math.sqrt((self.north_shift - other_north_shift)**2 +
                             (self.east_shift - other_east_shift)**2)

        else:
            slat, slon = self.effective_latlon
            rlat, rlon = get_effective_latlon(other)

            return float(orthodrome.distance_accurate50m_numpy(
                slat, slon, rlat, rlon)[0])

    def distance_3d_to(self, other):
        '''
        Compute 3D distance [m] to other location object.

        All coordinates are transformed to cartesian coordinates if necessary
        then distance is:

        .. math::

            \\Delta = \\sqrt{\\Delta {\\bf x}^2 + \\Delta {\\bf y}^2 + \
                      \\Delta {\\bf z}^2}

        :param other: Other location.
        :type other: :py:class:`~pyrocko.model.location.Location`

        :return: 3D distance to another location in [m].
        :rtype: float
        '''

        if self.same_origin(other):
            other_north_shift, other_east_shift = get_offset(other)
            return math.sqrt((self.north_shift - other_north_shift)**2 +
                             (self.east_shift - other_east_shift)**2 +
                             (self.depth - other.depth)**2)

        else:
            slat, slon = self.effective_latlon
            rlat, rlon = get_effective_latlon(other)

            sx, sy, sz = latlondepth_to_cartesian(slat, slon, self.depth)
            rx, ry, rz = latlondepth_to_cartesian(rlat, rlon, other.depth)

            return math.sqrt((sx-rx)**2 + (sy-ry)**2 + (sz-rz)**2)

    def crosstrack_distance_to(self, path_begin, path_end):
        '''
        Compute distance to a great-circle arc.

        :param path_begin: Location of the start of the arc.
        :param path_end: Location of the end of the arc.
        :type path_begin: :py:class:`~pyrocko.model.location.Location`
        :type path_end: :py:class:`~pyrocko.model.location.Location`

        :return: Distance to a great circle arc in [deg].
        :rtype: float
        '''
        return orthodrome.crosstrack_distance(
            *path_begin.effective_latlon,
            *path_end.effective_latlon,
            *self.effective_latlon
        )

    def alongtrack_distance_to(self, path_begin, path_end, meter=False):
        '''
        Compute distance along a great-circle arc.

        :param path_begin: Location of the start of the arc.
        :param path_end: Location of the end of the arc.
        :param meter: Return [m] instead of [deg].
        :type path_begin: :py:class:`~pyrocko.model.location.Location`
        :type path_end: :py:class:`~pyrocko.model.location.Location`

        :return: Distance from the start of the great circle arc
            in [deg] or [m].
        :rtype: float
        '''
        if meter:
            return orthodrome.alongtrack_distance_m(
                *path_begin.effective_latlon,
                *path_end.effective_latlon,
                *self.effective_latlon
            )
        return orthodrome.alongtrack_distance(
            *path_begin.effective_latlon,
            *path_end.effective_latlon,
            *self.effective_latlon
        )

    def offset_to(self, other):
        if self.same_origin(other):
            other_north_shift, other_east_shift = get_offset(other)
            return (
                other_north_shift - self.north_shift,
                other_east_shift - self.east_shift)

        else:
            azi, bazi = self.azibazi_to(other)
            dist = self.distance_to(other)
            return dist*math.cos(azi*d2r), dist*math.sin(azi*d2r)

    def azibazi_to(self, other):
        '''
        Compute azimuth and backazimuth to and from other location object.

        :param other: Other location.
        :type other: :py:class:`~pyrocko.model.location.Location`

        :return: Azimuth and back-azimuth to the location in [deg].
        :rtype: tuple[float, float]
        '''

        if self.same_origin(other):
            other_north_shift, other_east_shift = get_offset(other)
            azi = r2d * math.atan2(other_east_shift - self.east_shift,
                                   other_north_shift - self.north_shift)

            bazi = azi + 180.
        else:
            slat, slon = self.effective_latlon
            rlat, rlon = get_effective_latlon(other)
            azi, bazi = orthodrome.azibazi_numpy(slat, slon, rlat, rlon)

        return float(azi), float(bazi)

    def set_origin(self, lat, lon):
        lat = float(lat)
        lon = float(lon)
        elat, elon = self.effective_latlon
        n, e = orthodrome.latlon_to_ne_numpy(lat, lon, elat, elon)
        self.lat = lat
        self.lon = lon
        self.north_shift = float(n)
        self.east_shift = float(e)
        self._latlon = elat, elon  # unchanged

    @property
    def coords5(self):
        return num.array([
            self.lat, self.lon, self.north_shift, self.east_shift, self.depth])


def filter_azimuths(
    locations: list[Location],
    center: Location,
    azimuth: float,
    azimuth_width: float,
) -> list[Location]:
    """Filter locations by azimuth swath.

    Args:
        locations (list[Location]): List of Locations.
        center (Location): Relative center location.
        azimuth (float): Azimuth in [deg]. -180 to 180 or 0 to 360.
        azimuth_width (float): Width of the swath.

    Returns:
        list[Location]: Filtered locations.
    """
    OFFSET = 720.0
    filt_locations = []

    azimuth_min = azimuth + OFFSET - azimuth_width
    azimuth_max = azimuth + OFFSET + azimuth_width
    for loc in locations:
        azimuth, _ = center.azibazi_to(loc)
        if (azimuth_min <= azimuth + OFFSET <= azimuth_max) or (
            azimuth_min <= azimuth % 360.0 + OFFSET <= azimuth_max
        ):
            filt_locations.append(loc)
    return filt_locations


def filter_distance(
    locations: list[Location],
    reference: Location,
    distance_min: float,
    distance_max: float,
) -> list[Location]:
    """Filter location by distance to a reference point.

    Args:
        locations (list[Location]): Locations to filter.
        reference (Location): Reference location.
        distance_min (float): Minimum distance in [m].
        distance_max (float): Maximum distance in [m].

    Returns:
        list[Location]: Filtered locations.
    """
    return [
        loc
        for loc in locations
        if distance_min <= loc.distance_to(reference) <= distance_max
    ]


def filter_crosstrack_distance(
    locations: list[Location],
    start_path: Location,
    end_path: Location,
    distance_max: float
) -> list[Location]:
    """Filter location by distance to a great-circle path.

    Args:
        locations (list[Location]): Locations to filter.
        start_path (Location): Start of the great circle path.
        end_path (Location): End of the great circle path.
        distance_max (float): Distance to the great-circle in [deg].

    Returns:
        list[Location]: Filtered locations.
    """
    return [
        loc
        for loc in locations
        if abs(loc.crosstrack_distance_to(
            start_path, end_path)) <= distance_max
    ]


def get_offset(obj):
    try:
        return obj.north_shift, obj.east_shift
    except AttributeError:
        return 0.0, 0.0


def get_effective_latlon(obj):
    try:
        return obj.effective_latlon
    except AttributeError:
        return obj.lat, obj.lon
