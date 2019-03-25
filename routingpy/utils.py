# -*- coding: utf-8 -*-
# Copyright (C) 2019 GIS OPS UG. All rights reserved.
#
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
#


def _trans(value, index):
    """
    Copyright (c) 2014 Bruno M. Custódio
    Copyright (c) 2016 Frederick Jansen

    https://github.com/hicsail/polyline/commit/ddd12e85c53d394404952754e39c91f63a808656
    """
    byte, result, shift = None, 0, 0

    while byte is None or byte >= 0x20:
        byte = ord(value[index]) - 63
        index += 1
        result |= (byte & 0x1f) << shift
        shift += 5
        comp = result & 1

    return ~(result >> 1) if comp else (result >> 1), index


def _decode(expression, precision=5, is3d=False):
    """
    Copyright (c) 2014 Bruno M. Custódio
    Copyright (c) 2016 Frederick Jansen

    https://github.com/hicsail/polyline/commit/ddd12e85c53d394404952754e39c91f63a808656
    """
    coordinates, index, lat, lng, z, length, factor = [], 0, 0, 0, 0, len(expression), float(10 ** precision)

    while index < length:
        lat_change, index = _trans(expression, index)
        lng_change, index = _trans(expression, index)
        lat += lat_change
        lng += lng_change
        if not is3d:
            coordinates.append((lng / factor, lat / factor))
        else:
            z_change, index = _trans(expression, index)
            z += z_change
            coordinates.append((lng / factor, lat / factor, z / 100))

    return coordinates


def decode_polyline5(polyline, is3d=False):
    """Decodes an encoded polyline string which was encoded with a precision of 5. Output will be in [Lon, Lat] order.

    :param polyline: An encoded polyline, only the geometry.
    :type polyline: str

    :param is3d: Specifies if geometry contains Z component. Currently only GraphHopper and OpenRouteService
        support this. Default False.
    :type is3d: bool

    :returns: List of decoded coordinates with precision 5 in [Lon, Lat] order.
    :rtype: list
    """

    return _decode(polyline, precision=5, is3d=is3d)


def decode_polyline6(polyline, is3d=False):
    """Decodes an encoded polyline string which was encoded with a precision of 6. Output will be in [Lon, Lat] order.

    :param polyline: An encoded polyline, only the geometry.
    :type polyline: str

    :param is3d: Specifies if geometry contains Z component. Currently only GraphHopper and OpenRouteService
        support this. Default False.
    :type is3d: bool

    :returns: List of decoded coordinates with precision 6 in [Lon, Lat] order.
    :rtype: list
    """

    return _decode(polyline, precision=6, is3d=is3d)