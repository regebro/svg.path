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

There is also a ``parse_path()`` function that will take an SVG path definition
and return a ``Path`` object.

Classes
.......

These are the SVG path segment classes. See the `SVG specifications
<http://www.w3.org/TR/SVG/paths.html>`_ for more information on what each
parameter means.

* ``Line(start, end)``    

* ``Arc(start, radius, rotation, arc, sweep, end)``

* ``QuadraticBezier(start, control1, control2, end)``

* ``CubicBezier(start, control1, control2, end)``

In addition to that, there is the ``Path`` class, which is instantiated
with a sequence of path segments:

* ``Path(*segments)``
    
That ``Path`` class is a mutable sequence, so it behaves like a list.


Examples
........

This SVG path example draws a triangle:

    >>> from svg.path import parse_path, Path, Line, QuadraticBezier
    
    >>> path1 = parse_path('M 100 100 L 300 100 L 200 300 z')

You can format SVG paths in many different ways, all valid paths should be
accepted:

    >>> path2 = parse_path('M100,100L300,100L200,300z')
    
And these paths should be equal:

    >>> path1 == path2
    True

You can also build a path from objects:

    >>> path3 = Path(Line(100+100j,300+100j), Line(300+100j, 200+300j), Line(200+300j, 100+100j))
    
And it should again be equal to the first path:

    >>> path1 == path2
    True

Paths are mutable sequences, you can slice and append:

    >>> path1.append(QuadraticBezier(300+100j, 200+200j, 200+300j))
    >>> len(path1[2:]) == 2
    True


Todo
----

This module should have a way to generate path definitions from a path, for
completeness.

Licence
-------

This module is under a CC0 1.0 Universal licence. 
http://creativecommons.org/publicdomain/zero/1.0/
