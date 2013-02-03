svg.path
========

svg.path is a collection of objects that implement the different path
commands in SVG, and a parser for SVG path definitions.

Usage
-----

There are four path segment objects, ``Line``, ``Arc``, ``CubicBezier`` and
``QuadraticBezier``.`There is also a ``Path`` object that acts as a
collection of the path segment objects.

All of these objects have a ``.point()`` and a ``.length()`` function. 

All coordinate values for these functions are given as ``complex`` values,
where the ``.real`` part represents the X coordinate, and the ``.imag`` part
representes the Y coordinate.

The ``.point()`` function will return the X and Y coordinates of a point on
the path, where the point is given as a floating point value where ``0.0`` is
the start of the path and ``1.0`` is end end. 

The ``.length()`` function will return the path segment or paths length. This
is in some cases done by geometric approximation and for this reason **may be
very slow**.


Todo
----

This module should have a way to generate path definitions from a path, for
completeness.

Licence
-------

This module is under a CC0 1.0 Universal licence. 
http://creativecommons.org/publicdomain/zero/1.0/
