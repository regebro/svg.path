from __future__ import division
from math import sqrt, cos, sin, acos, degrees, radians, log, pi
from bisect import bisect
import re

try:
    from collections.abc import MutableSequence
except ImportError:
    from collections import MutableSequence

# This file contains classes for the different types of SVG path segments as
# well as a Path object that contains a sequence of path segments.

MIN_DEPTH = 5
ERROR = 1e-12

COMMANDS = set("MmZzLlHhVvCcSsQqTtAa")
UPPERCASE = set("MZLHVCSQTA")

COMMAND_RE = re.compile(r"([MmZzLlHhVvCcSsQqTtAa])")
FLOAT_RE = re.compile(r"[-+]?[0-9]*\.?[0-9]+(?:[eE][-+]?[0-9]+)?")


def segment_length(curve, start, end, start_point, end_point, error, min_depth, depth):
    """Recursively approximates the length by straight lines"""
    mid = (start + end) / 2
    mid_point = curve.point(mid)
    length = abs(end_point - start_point)
    first_half = abs(mid_point - start_point)
    second_half = abs(end_point - mid_point)

    length2 = first_half + second_half
    if (length2 - length > error) or (depth < min_depth):
        # Calculate the length of each segment:
        depth += 1
        return segment_length(
            curve, start, mid, start_point, mid_point, error, min_depth, depth
        ) + segment_length(
            curve, mid, end, mid_point, end_point, error, min_depth, depth
        )
    # This is accurate enough.
    return length2


class Linear(object):
    """A straight line

    The base for Line() and Close().
    """

    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __ne__(self, other):
        if not isinstance(other, Line):
            return NotImplemented
        return not self == other

    def point(self, pos):
        distance = self.end - self.start
        return self.start + distance * pos

    def length(self, error=None, min_depth=None):
        distance = self.end - self.start
        return sqrt(distance.real ** 2 + distance.imag ** 2)


class Line(Linear):
    def __repr__(self):
        return "Line(start=%s, end=%s)" % (self.start, self.end)

    def __eq__(self, other):
        if not isinstance(other, Line):
            return NotImplemented
        return self.start == other.start and self.end == other.end


class CubicBezier(object):
    def __init__(self, start, control1, control2, end):
        self.start = start
        self.control1 = control1
        self.control2 = control2
        self.end = end

    def __repr__(self):
        return "CubicBezier(start=%s, control1=%s, control2=%s, end=%s)" % (
            self.start,
            self.control1,
            self.control2,
            self.end,
        )

    def __eq__(self, other):
        if not isinstance(other, CubicBezier):
            return NotImplemented
        return (
            self.start == other.start
            and self.end == other.end
            and self.control1 == other.control1
            and self.control2 == other.control2
        )

    def __ne__(self, other):
        if not isinstance(other, CubicBezier):
            return NotImplemented
        return not self == other

    def is_smooth_from(self, previous):
        """Checks if this segment would be a smooth segment following the previous"""
        if isinstance(previous, CubicBezier):
            return self.start == previous.end and (self.control1 - self.start) == (
                previous.end - previous.control2
            )
        else:
            return self.control1 == self.start

    def point(self, pos):
        """Calculate the x,y position at a certain position of the path"""
        return (
            ((1 - pos) ** 3 * self.start)
            + (3 * (1 - pos) ** 2 * pos * self.control1)
            + (3 * (1 - pos) * pos ** 2 * self.control2)
            + (pos ** 3 * self.end)
        )

    def length(self, error=ERROR, min_depth=MIN_DEPTH):
        """Calculate the length of the path up to a certain position"""
        start_point = self.point(0)
        end_point = self.point(1)
        return segment_length(self, 0, 1, start_point, end_point, error, min_depth, 0)


class QuadraticBezier(object):
    def __init__(self, start, control, end):
        self.start = start
        self.end = end
        self.control = control

    def __repr__(self):
        return "QuadraticBezier(start=%s, control=%s, end=%s)" % (
            self.start,
            self.control,
            self.end,
        )

    def __eq__(self, other):
        if not isinstance(other, QuadraticBezier):
            return NotImplemented
        return (
            self.start == other.start
            and self.end == other.end
            and self.control == other.control
        )

    def __ne__(self, other):
        if not isinstance(other, QuadraticBezier):
            return NotImplemented
        return not self == other

    def is_smooth_from(self, previous):
        """Checks if this segment would be a smooth segment following the previous"""
        if isinstance(previous, QuadraticBezier):
            return self.start == previous.end and (self.control - self.start) == (
                previous.end - previous.control
            )
        else:
            return self.control == self.start

    def point(self, pos):
        return (
            (1 - pos) ** 2 * self.start
            + 2 * (1 - pos) * pos * self.control
            + pos ** 2 * self.end
        )

    def length(self, error=None, min_depth=None):
        a = self.start - 2 * self.control + self.end
        b = 2 * (self.control - self.start)
        a_dot_b = a.real * b.real + a.imag * b.imag

        if abs(a) < 1e-12:
            s = abs(b)
        elif abs(a_dot_b + abs(a) * abs(b)) < 1e-12:
            k = abs(b) / abs(a)
            if k >= 2:
                s = abs(b) - abs(a)
            else:
                s = abs(a) * (k ** 2 / 2 - k + 1)
        else:
            # For an explanation of this case, see
            # http://www.malczak.info/blog/quadratic-bezier-curve-length/
            A = 4 * (a.real ** 2 + a.imag ** 2)
            B = 4 * (a.real * b.real + a.imag * b.imag)
            C = b.real ** 2 + b.imag ** 2

            Sabc = 2 * sqrt(A + B + C)
            A2 = sqrt(A)
            A32 = 2 * A * A2
            C2 = 2 * sqrt(C)
            BA = B / A2

            s = (
                A32 * Sabc
                + A2 * B * (Sabc - C2)
                + (4 * C * A - B ** 2) * log((2 * A2 + BA + Sabc) / (BA + C2))
            ) / (4 * A32)
        return s


class Arc(object):
    def __init__(self, start, radius, rotation, arc, sweep, end):
        """radius is complex, rotation is in degrees,
           large and sweep are 1 or 0 (True/False also work)"""

        self.start = start
        self.radius = radius
        self.rotation = rotation
        self.arc = bool(arc)
        self.sweep = bool(sweep)
        self.end = end

        self._parameterize()

    def __repr__(self):
        return "Arc(start=%s, radius=%s, rotation=%s, arc=%s, sweep=%s, end=%s)" % (
            self.start,
            self.radius,
            self.rotation,
            self.arc,
            self.sweep,
            self.end,
        )

    def __eq__(self, other):
        if not isinstance(other, Arc):
            return NotImplemented
        return (
            self.start == other.start
            and self.end == other.end
            and self.radius == other.radius
            and self.rotation == other.rotation
            and self.arc == other.arc
            and self.sweep == other.sweep
        )

    def __ne__(self, other):
        if not isinstance(other, Arc):
            return NotImplemented
        return not self == other

    def _parameterize(self):
        # Conversion from endpoint to center parameterization
        # http://www.w3.org/TR/SVG/implnote.html#ArcImplementationNotes
        if self.start == self.end:
            # This is equivalent of omitting the segment, so do nothing
            return

        if self.radius.real == 0 or self.radius.imag == 0:
            # This should be treated as a straight line
            return

        cosr = cos(radians(self.rotation))
        sinr = sin(radians(self.rotation))
        dx = (self.start.real - self.end.real) / 2
        dy = (self.start.imag - self.end.imag) / 2
        x1prim = cosr * dx + sinr * dy
        x1prim_sq = x1prim * x1prim
        y1prim = -sinr * dx + cosr * dy
        y1prim_sq = y1prim * y1prim

        rx = self.radius.real
        rx_sq = rx * rx
        ry = self.radius.imag
        ry_sq = ry * ry

        # Correct out of range radii
        radius_scale = (x1prim_sq / rx_sq) + (y1prim_sq / ry_sq)
        if radius_scale > 1:
            radius_scale = sqrt(radius_scale)
            rx *= radius_scale
            ry *= radius_scale
            rx_sq = rx * rx
            ry_sq = ry * ry
            self.radius_scale = radius_scale
        else:
            # SVG spec only scales UP
            self.radius_scale = 1

        t1 = rx_sq * y1prim_sq
        t2 = ry_sq * x1prim_sq
        c = sqrt(abs((rx_sq * ry_sq - t1 - t2) / (t1 + t2)))

        if self.arc == self.sweep:
            c = -c
        cxprim = c * rx * y1prim / ry
        cyprim = -c * ry * x1prim / rx

        self.center = complex(
            (cosr * cxprim - sinr * cyprim) + ((self.start.real + self.end.real) / 2),
            (sinr * cxprim + cosr * cyprim) + ((self.start.imag + self.end.imag) / 2),
        )

        ux = (x1prim - cxprim) / rx
        uy = (y1prim - cyprim) / ry
        vx = (-x1prim - cxprim) / rx
        vy = (-y1prim - cyprim) / ry
        n = sqrt(ux * ux + uy * uy)
        p = ux
        theta = degrees(acos(p / n))
        if uy < 0:
            theta = -theta
        self.theta = theta % 360

        n = sqrt((ux * ux + uy * uy) * (vx * vx + vy * vy))
        p = ux * vx + uy * vy
        d = p / n
        # In certain cases the above calculation can through inaccuracies
        # become just slightly out of range, f ex -1.0000000000000002.
        if d > 1.0:
            d = 1.0
        elif d < -1.0:
            d = -1.0
        delta = degrees(acos(d))
        if (ux * vy - uy * vx) < 0:
            delta = -delta
        self.delta = delta % 360
        if not self.sweep:
            self.delta -= 360

    def point(self, pos):
        if self.start == self.end:
            # This is equivalent of omitting the segment
            return self.start

        if self.radius.real == 0 or self.radius.imag == 0:
            # This should be treated as a straight line
            distance = self.end - self.start
            return self.start + distance * pos

        angle = radians(self.theta + (self.delta * pos))
        cosr = cos(radians(self.rotation))
        sinr = sin(radians(self.rotation))
        radius = self.radius * self.radius_scale

        x = (
            cosr * cos(angle) * radius.real
            - sinr * sin(angle) * radius.imag
            + self.center.real
        )
        y = (
            sinr * cos(angle) * radius.real
            + cosr * sin(angle) * radius.imag
            + self.center.imag
        )
        return complex(x, y)

    def length(self, error=ERROR, min_depth=MIN_DEPTH):
        """The length of an elliptical arc segment requires numerical
        integration, and in that case it's simpler to just do a geometric
        approximation, as for cubic bezier curves.
        """
        if self.start == self.end:
            # This is equivalent of omitting the segment
            return 0

        if self.radius.real == 0 or self.radius.imag == 0:
            # This should be treated as a straight line
            distance = self.end - self.start
            return sqrt(distance.real ** 2 + distance.imag ** 2)

        if self.radius.real == self.radius.imag:
            # It's a circle, which simplifies this a LOT.
            radius = self.radius.real * self.radius_scale
            return abs(radius * self.delta * pi / 180)

        start_point = self.point(0)
        end_point = self.point(1)
        return segment_length(self, 0, 1, start_point, end_point, error, min_depth, 0)


class Move(object):
    """Represents move commands. Does nothing, but is there to handle
    paths that consist of only move commands, which is valid, but pointless.
    """

    def __init__(self, to):
        self.start = self.end = to

    def __repr__(self):
        return "Move(to=%s)" % self.start

    def __eq__(self, other):
        if not isinstance(other, Move):
            return NotImplemented
        return self.start == other.start

    def __ne__(self, other):
        if not isinstance(other, Move):
            return NotImplemented
        return not self == other

    def point(self, pos):
        return self.start

    def length(self, error=ERROR, min_depth=MIN_DEPTH):
        return 0


class Close(Linear):
    """Represents the closepath command"""

    def __eq__(self, other):
        if not isinstance(other, Close):
            return NotImplemented
        return self.start == other.start and self.end == other.end

    def __repr__(self):
        return "Close(start=%s, end=%s)" % (self.start, self.end)


class Path(MutableSequence):
    """A Path is a sequence of path segments"""

    def __init__(self, *segments, **kwargs):
        if len(segments) >= 1:
            if isinstance(segments[0], str):
                if len(segments) >= 2:
                    current_pos = segments[1]
                elif 'current_pos' in kwargs:
                    current_pos = kwargs['current_pos']
                else:
                    current_pos = 0j
                self._segments = list()
                self._parse_path(segments[0], current_pos)
            else:
                self._segments = list(segments)
        else:
            self._segments = list()
        self._length = None
        self._lengths = None
        # Fractional distance from starting point through the end of each segment.
        self._fractions = []

    def __getitem__(self, index):
        return self._segments[index]

    def __setitem__(self, index, value):
        self._segments[index] = value
        self._length = None

    def __delitem__(self, index):
        del self._segments[index]
        self._length = None

    def insert(self, index, value):
        self._segments.insert(index, value)
        self._length = None

    def reverse(self):
        # Reversing the order of a path would require reversing each element
        # as well. That's not implemented.
        raise NotImplementedError

    def __len__(self):
        return len(self._segments)

    def __repr__(self):
        return "Path(%s)" % (", ".join(repr(x) for x in self._segments))

    def __eq__(self, other):

        if not isinstance(other, Path):
            return NotImplemented
        if len(self) != len(other):
            return False
        for s, o in zip(self._segments, other._segments):
            if not s == o:
                return False
        return True

    def __ne__(self, other):
        if not isinstance(other, Path):
            return NotImplemented
        return not self == other

    def _calc_lengths(self, error=ERROR, min_depth=MIN_DEPTH):
        if self._length is not None:
            return

        lengths = [
            each.length(error=error, min_depth=min_depth) for each in self._segments
        ]
        self._length = sum(lengths)
        self._lengths = [each / self._length for each in lengths]
        # Calculate the fractional distance for each segment to use in point()
        fraction = 0
        for each in self._lengths:
            fraction += each
            self._fractions.append(fraction)

    def point(self, pos, error=ERROR):

        # Shortcuts
        if pos == 0.0:
            return self._segments[0].point(pos)
        if pos == 1.0:
            return self._segments[-1].point(pos)

        self._calc_lengths(error=error)
        # Find which segment the point we search for is located on:
        i = bisect(self._fractions, pos)
        if i == 0:
            segment_pos = pos / self._fractions[0]
        else:
            segment_pos = (pos - self._fractions[i - 1]) / (
                self._fractions[i] - self._fractions[i - 1]
            )
        return self._segments[i].point(segment_pos)

    def length(self, error=ERROR, min_depth=MIN_DEPTH):
        self._calc_lengths(error, min_depth)
        return self._length

    def d(self):
        current_pos = None
        parts = []
        previous_segment = None
        end = self[-1].end

        for segment in self:
            start = segment.start
            # If the start of this segment does not coincide with the end of
            # the last segment or if this segment is actually the close point
            # of a closed path, then we should start a new subpath here.
            if isinstance(segment, Close):
                parts.append("Z")
            elif (
                isinstance(segment, Move)
                or (current_pos != start)
                or (start == end and not isinstance(previous_segment, Move))
            ):
                parts.append("M {0:G},{1:G}".format(start.real, start.imag))

            if isinstance(segment, Line):
                parts.append("L {0:G},{1:G}".format(segment.end.real, segment.end.imag))
            elif isinstance(segment, CubicBezier):
                if segment.is_smooth_from(previous_segment):
                    parts.append(
                        "S {0:G},{1:G} {2:G},{3:G}".format(
                            segment.control2.real,
                            segment.control2.imag,
                            segment.end.real,
                            segment.end.imag,
                        )
                    )
                else:
                    parts.append(
                        "C {0:G},{1:G} {2:G},{3:G} {4:G},{5:G}".format(
                            segment.control1.real,
                            segment.control1.imag,
                            segment.control2.real,
                            segment.control2.imag,
                            segment.end.real,
                            segment.end.imag,
                        )
                    )
            elif isinstance(segment, QuadraticBezier):
                if segment.is_smooth_from(previous_segment):
                    parts.append(
                        "T {0:G},{1:G}".format(segment.end.real, segment.end.imag)
                    )
                else:
                    parts.append(
                        "Q {0:G},{1:G} {2:G},{3:G}".format(
                            segment.control.real,
                            segment.control.imag,
                            segment.end.real,
                            segment.end.imag,
                        )
                    )
            elif isinstance(segment, Arc):
                parts.append(
                    "A {0:G},{1:G} {2:G} {3:d},{4:d} {5:G},{6:G}".format(
                        segment.radius.real,
                        segment.radius.imag,
                        segment.rotation,
                        int(segment.arc),
                        int(segment.sweep),
                        segment.end.real,
                        segment.end.imag,
                    )
                )

            current_pos = segment.end
            previous_segment = segment

        return " ".join(parts)

    def _tokenize_path(self, pathdef):
        for x in COMMAND_RE.split(pathdef):
            if x in COMMANDS:
                yield x
            for token in FLOAT_RE.findall(x):
                yield token

    def _parse_path(self, pathdef, current_pos=0j):
        # In the SVG specs, initial movetos are absolute, even if
        # specified as 'm'. This is the default behavior here as well.
        # But if you pass in a current_pos variable, the initial moveto
        # will be relative to that current_pos. This is useful.
        elements = list(self._tokenize_path(pathdef))
        # Reverse for easy use of .pop()
        elements.reverse()

        segments = self._segments
        start_pos = None
        command = None

        while elements:

            if elements[-1] in COMMANDS:
                # New command.
                last_command = command  # Used by S and T
                command = elements.pop()
                absolute = command in UPPERCASE
                command = command.upper()
            else:
                # If this element starts with numbers, it is an implicit command
                # and we don't change the command. Check that it's allowed:
                if command is None:
                    raise ValueError(
                        "Unallowed implicit command in %s, position %s"
                        % (pathdef, len(pathdef.split()) - len(elements))
                    )
                last_command = command  # Used by S and T

            if command == "M":
                # Moveto command.
                x = elements.pop()
                y = elements.pop()
                pos = float(x) + float(y) * 1j
                if absolute:
                    current_pos = pos
                else:
                    current_pos += pos
                segments.append(Move(current_pos))
                # when M is called, reset start_pos
                # This behavior of Z is defined in svg spec:
                # http://www.w3.org/TR/SVG/paths.html#PathDataClosePathCommand
                start_pos = current_pos

                # Implicit moveto commands are treated as lineto commands.
                # So we set command to lineto here, in case there are
                # further implicit commands after this moveto.
                command = "L"

            elif command == "Z":
                # Close path
                segments.append(Close(current_pos, start_pos))
                current_pos = start_pos
                start_pos = None
                command = None  # You can't have implicit commands after closing.

            elif command == "L":
                x = elements.pop()
                y = elements.pop()
                pos = float(x) + float(y) * 1j
                if not absolute:
                    pos += current_pos
                segments.append(Line(current_pos, pos))
                current_pos = pos

            elif command == "H":
                x = elements.pop()
                pos = float(x) + current_pos.imag * 1j
                if not absolute:
                    pos += current_pos.real
                segments.append(Line(current_pos, pos))
                current_pos = pos

            elif command == "V":
                y = elements.pop()
                pos = current_pos.real + float(y) * 1j
                if not absolute:
                    pos += current_pos.imag * 1j
                segments.append(Line(current_pos, pos))
                current_pos = pos

            elif command == "C":
                control1 = float(elements.pop()) + float(elements.pop()) * 1j
                control2 = float(elements.pop()) + float(elements.pop()) * 1j
                end = float(elements.pop()) + float(elements.pop()) * 1j

                if not absolute:
                    control1 += current_pos
                    control2 += current_pos
                    end += current_pos

                segments.append(CubicBezier(current_pos, control1, control2, end))
                current_pos = end

            elif command == "S":
                # Smooth curve. First control point is the "reflection" of
                # the second control point in the previous path.

                if last_command not in "CS":
                    # If there is no previous command or if the previous command
                    # was not an C, c, S or s, assume the first control point is
                    # coincident with the current point.
                    control1 = current_pos
                else:
                    # The first control point is assumed to be the reflection of
                    # the second control point on the previous command relative
                    # to the current point.
                    control1 = current_pos + current_pos - segments[-1].control2

                control2 = float(elements.pop()) + float(elements.pop()) * 1j
                end = float(elements.pop()) + float(elements.pop()) * 1j

                if not absolute:
                    control2 += current_pos
                    end += current_pos

                segments.append(CubicBezier(current_pos, control1, control2, end))
                current_pos = end

            elif command == "Q":
                control = float(elements.pop()) + float(elements.pop()) * 1j
                end = float(elements.pop()) + float(elements.pop()) * 1j

                if not absolute:
                    control += current_pos
                    end += current_pos

                segments.append(QuadraticBezier(current_pos, control, end))
                current_pos = end

            elif command == "T":
                # Smooth curve. Control point is the "reflection" of
                # the second control point in the previous path.

                if last_command not in "QT":
                    # If there is no previous command or if the previous command
                    # was not an Q, q, T or t, assume the first control point is
                    # coincident with the current point.
                    control = current_pos
                else:
                    # The control point is assumed to be the reflection of
                    # the control point on the previous command relative
                    # to the current point.
                    control = current_pos + current_pos - segments[-1].control

                end = float(elements.pop()) + float(elements.pop()) * 1j

                if not absolute:
                    end += current_pos

                segments.append(QuadraticBezier(current_pos, control, end))
                current_pos = end

            elif command == "A":
                radius = float(elements.pop()) + float(elements.pop()) * 1j
                rotation = float(elements.pop())
                arc = float(elements.pop())
                sweep = float(elements.pop())
                end = float(elements.pop()) + float(elements.pop()) * 1j

                if not absolute:
                    end += current_pos

                segments.append(Arc(current_pos, radius, rotation, arc, sweep, end))
                current_pos = end
