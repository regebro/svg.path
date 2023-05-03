import unittest

from svg import path, transform
from math import pi, tan, atan, sqrt
from cmath import polar, rect


class BaseTransformTests:
    def _confirm_transform(self, original):
        pass

    def notest_confirm_lines(self):
        for line in (
            path.Line(0, 100 + 100j),
            path.Line(0, 100),
            path.Line(0, 100j),
            path.Line(-100 + 50j, -250+200j),
        ):
            self._confirm_transform(line)

    def notest_confirm_quads(self):
        for quad in (
            path.QuadraticBezier(0, 100j, 100 + 100j),
            path.QuadraticBezier(300+100j, 200+200j, 200+300j),
            path.QuadraticBezier(6 + 2j, 5 - 1j, 6 + 2j),
        ):
            self._confirm_transform(quad)

    def notest_confirm_cubes(self):
        for cube in(
            path.CubicBezier(0, +100j, 100, 100 + 100j),
        ):
            self._confirm_transform(cube)

    def test_confirm_arcs(self):
        for arc in (
            path.Arc(-200-200j, 400 + 400j, 0, 0, 1, 200+200j),
            #path.Arc(-200, 200 + 200j, 0, 0, 1, 200),
            #path.Arc(-100, 100 + 50j, 0, 0, 1, 100),
            #path.Arc(100, 100 + 50j, 0, 0, 1, -100),
        ):
            self._confirm_transform(arc)


class TranslateTransformTests(BaseTransformTests, unittest.TestCase):
    def _confirm_transform(self, original):
        for x in (-100, -5, 0, 0.1, 1, 5, 10, 157):
            for y in (-100, -5, 0, 0.1, 1, 5, 10, 157):
                scale = transform.translate_matrix(x, y)
                xformed = original.transform(scale)

                for pos in range(0, 101):
                    opoint = original.point(pos*0.01)
                    xpoint = xformed.point(pos*0.01)
                    assert abs(xpoint.real - opoint.real - x) < 0.00001
                    assert abs(xpoint.imag - opoint.imag - y) < 0.00001


class ScaleTransformTests(BaseTransformTests, unittest.TestCase):
    def _confirm_transform(self, original):
        for x in (0.1, 0.5, 1, 1.1, 1.5, 2, 10):
            for y in (0.1, 0.5, 1, 1.1, 1.5, 2, 10):
                scale = transform.scale_matrix(x, y)
                xformed = original.transform(scale)

                for pos in range(0, 101):
                    opoint = original.point(pos*0.01)
                    xpoint = xformed.point(pos*0.01)
                    assert abs(xpoint.real - opoint.real * x) < 0.00001
                    assert abs(xpoint.imag - opoint.imag * y) < 0.00001


class SkewTransformTests(BaseTransformTests, unittest.TestCase):
    def _confirm_transform(self, original):
        for alpha in range(1, 2):
            angle = (alpha * 15 * 2 * pi) / 360
            skewx = transform.skewx_matrix(angle)
            xformed_x = original.transform(skewx)
            skewy = transform.skewy_matrix(angle)
            xformed_y = original.transform(skewy)
            skewboth = transform.make_matrix(ax=angle, ay=angle)
            xformed_both2 = original.transform(skewboth)
            xformed_both = path.Arc(xformed_both2.start, 780+780j, 0, 0, 1, xformed_both2.end)

            from .utils import DebugTurtle
            with DebugTurtle(steps=25) as t:
                #t.draw_path(original)
                #t.draw_path(original, color="blue", matrix=skewx)
                #t.draw_path(xformed_x, color="light blue")
                #t.draw_path(original, color="green", matrix=skewy)
                #t.draw_path(xformed_y, color="light green")
                t.draw_path(original, color="red", matrix=skewboth)
                t.draw_path(xformed_both, color="pink")

            for x in range(1, 101):
                px = xformed_x.point(x * 0.01)
                py = xformed_y.point(x * 0.01)
                pb = xformed_both.point(x * 0.01)
                o = original.point(x * 0.01)

                assert abs(px.real - (tan(angle) * o.imag + o.real)) < 0.00001
                assert abs(px.imag - o.imag) < 0.00001

                assert abs(py.real - o.real) < 0.00001
                assert abs(py.imag - (tan(angle) * o.real + o.imag)) < 0.00001

                print(x, "X:", abs(pb.real - (tan(angle) * o.imag + o.real)))
                print(x, "Y:", abs(pb.imag - (tan(angle) * o.real + o.imag)))

            assert 1==0


class RotateTransformTests(BaseTransformTests, unittest.TestCase):
    def _confirm_transform(self, original):
        for alpha in range(1, 7):
            angle = (alpha * 15 * 2 * pi) / 360
            skewx = transform.rotate_matrix(angle)
            xformed = original.transform(skewx)

            for x in range(1, 101):
                px = xformed.point(x * 0.01)
                o = original.point(x * 0.01)

                c, phi = polar(o)
                px2 = rect(c, phi+angle)
                assert abs(px - px2) < 1e-10


class TransformTests(unittest.TestCase):

    def test_svg_path_transform(self):
        line = path.Line(0, 100 + 100j)
        linex = line.transform(transform.make_matrix(sx=0.1, sy=0.2))
        assert linex == path.Line(0, 10 + 20j)

        d = path.parser.parse_path("M 750,100 L 250,900 L 1250,900 z")
        # Makes it 10% as big in x and 20% as big in y
        td = d.transform(transform.make_matrix(sx=0.1, sy=0.2))
        assert td.d() == "M 75,20 L 25,180 L 125,180 z"

        d = path.parser.parse_path(
            "M 10, 30 A 20, 20 0, 0, 1 50, 30 A 20,20 0, 0, 1 90, 30 Q 90, 60 50, 90 Q 10, 60 10, 30 z"
        )
        # Makes it 10% as big in x and 20% as big in y
        m = (
            transform.rotate_matrix((-10 * 2 * pi) / 360, 50, 100)
            @ transform.translate_matrix(-36, 45.5)
            @ transform.skewx_matrix((40 * 2 * pi) / 360)
            @ transform.scale_matrix(1, 0.5)
        )
        td = d.transform(m)
        # assert (
        # td.d()
        # == "M 149.32,82.6809 A 20,20 0 0,1 115.757,104.442 A 20,20 0 0,1 82.1939,126.203 "
        # "Q 88.0949,104.5 127.559,61.0359 Q 155.221,60.978 149.32,82.6809 z"
        # )

        import turtle
        t = turtle.Turtle()
        t.penup()
        arc = path.parser.parse_path(
            "M 10, 30 A 20, 20 0, 0, 1 50, 30 A 20,20 0, 0, 1 90, 30 Q 90, 60 50, 90 Q 10, 60 10, 30 z"
        )

        arc = arc.transform(transform.scale_matrix(3) @ transform.translate_matrix(-50, -50))
        for m in (
            transform.skewx_matrix((40*2*pi)/360),
            transform.scale_matrix(1, 0.5),
            transform.translate_matrix(-36, 45.5),
            #transform.rotate_matrix((-10*2*pi)/360),
            #transform.scale_matrix(1, 0.5)
            ):
            p = arc.point(0)
            t.goto(p.real, -p.imag)
            t.dot(3, 'black')
            t.pendown()
            for x in range(1, 101):
                p = arc.point(x * 0.01)
                t.goto(p.real, -p.imag)
            t.penup()
            t.dot(3, 'black')
            arc = arc.transform(m)

        import pdb;pdb.set_trace()
