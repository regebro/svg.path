import unittest

from svg import path, transform
from math import tan, radians
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
            path.Arc(-200, 200 + 200j, 0, 0, 1, 200),
            path.Arc(-100, 100 + 50j, 0, 0, 1, 100),
            path.Arc(100, 100 + 50j, 0, 0, 1, -100),
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
        from .utils import DebugTurtle

        for x in (0.1, 0.5, 1, 1.1, 1.5, 2, 10):
            for y in (0.1, 0.5, 1, 1.1, 1.5, 2, 10):
                scale = transform.scale_matrix(x, y)
                xformed = original.transform(scale)

                for pos in range(0, 101):
                    opoint = original.point(pos*0.01)
                    xpoint = xformed.point(pos*0.01)
                    if not abs(xpoint.real - opoint.real * x) < 0.00001:
                        print(f"Failed scale x: {x} at pos {pos} for {xformed}")
                        import pdb;pdb.set_trace()
                    if not abs(xpoint.imag - opoint.imag * y) < 0.00001:
                        print(f"Failed scale y: {y} at pos {pos} for {xformed}")
                        import pdb;pdb.set_trace()
                    assert abs(xpoint.real - opoint.real * x) < 0.00001
                    assert abs(xpoint.imag - opoint.imag * y) < 0.00001


class SkewTransformTests(BaseTransformTests, unittest.TestCase):
    def _confirm_transform(self, original):
        for alpha in range(1, 2):
            angle = radians(alpha * 15)
            skewx = transform.skewx_matrix(angle)
            xformed_x = original.transform(skewx)
            skewy = transform.skewy_matrix(angle)
            xformed_y = original.transform(skewy)
            skewboth = transform.make_matrix(ax=angle, ay=angle)
            xformed_both = original.transform(skewboth)

            for x in range(1, 101):
                px = xformed_x.point(x * 0.01)
                py = xformed_y.point(x * 0.01)
                pb = xformed_both.point(x * 0.01)
                o = original.point(x * 0.01)

                assert abs(px.real - (tan(angle) * o.imag + o.real)) < 0.00001
                assert abs(px.imag - o.imag) < 0.00001

                assert abs(py.real - o.real) < 0.00001
                assert abs(py.imag - (tan(angle) * o.real + o.imag)) < 0.00001

                assert abs(pb.real - (tan(angle) * o.imag + o.real)) < 0.00001
                assert abs(pb.imag - (tan(angle) * o.real + o.imag)) < 0.00001


class RotateTransformTests(BaseTransformTests, unittest.TestCase):
    def _confirm_transform(self, original):
        for alpha in range(1, 7):
            angle = radians(alpha * 15)
            rotateX = transform.rotate_matrix(angle)
            xformed = original.transform(rotateX)

            for x in range(1, 101):
                px = xformed.point(x * 0.01)
                o = original.point(x * 0.01)
                c, phi = polar(o)
                ox = rect(c, phi+angle)
                assert abs(px - ox) < 1e-5


class MatrixTransformTests(BaseTransformTests, unittest.TestCase):
    def _confirm_transform(self, original):
        for a in (1, 0.5): # scale x
            for b in (0.1, 0.7): # shear y
                for c in (0.2, 0.5): # shear x
                    for d in (1, 2): # scale y
                        for e in (0, 10, 100): # translate x
                            for f in (0, -10, -100): # translate y
                                matrix = transform.matrix_matrix(a, b, c, d, e, f)
                                xformed = original.transform(matrix)

                                for pos in range(0, 101):
                                    opoint = original.point(pos*0.01)
                                    xpoint = xformed.point(pos*0.01)

                                    expected_x = a * opoint.real + c * opoint.imag + e
                                    expected_y = b * opoint.real + d * opoint.imag + f

                                    assert abs(xpoint.real - expected_x) < 0.00001
                                    assert abs(xpoint.imag - expected_y) < 0.00001