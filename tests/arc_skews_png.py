import turtle

import unittest

from svg import path, transform
from math import pi


class TransformTests(unittest.TestCase):
    def test_make_skew_png(self):
        arc1 = path.Arc(-100, 100 + 50j, 0, 0, 1, 100)
        arc2 = path.Arc(100, 100 + 50j, 0, 0, 1, -100)

        t = turtle.Turtle()
        t.speed(10)
        t.penup()

        for testpath in (arc1, arc2):
            p = testpath.point(0)
            t.goto(p.real, p.imag)
            t.dot(3, "black")
            t.pendown()
            for x in range(1, 101):
                p = testpath.point(x * 0.01)
                t.goto(p.real, p.imag)
            t.penup()
            t.dot(3, "black")

        for x in range(1, 6):
            angle = (x * 15 * 2 * pi) / 360
            skewx = transform.skewx_matrix(angle)
            arcx1 = arc1.transform(skewx)
            arcx2 = arc2.transform(skewx)
            skewy = transform.skewy_matrix(angle)
            arcy1 = arc1.transform(skewy)
            arcy2 = arc2.transform(skewy)

            t = turtle.Turtle()
            t.speed(10)
            t.penup()

            for testpath, color in (
                (arcx1, "blue"),
                (arcx2, "blue"),
                (arcy1, "green"),
                (arcy2, "green"),
            ):
                t.pencolor(color)
                p = testpath.point(0)
                t.goto(p.real, p.imag)
                t.dot(3, "black")
                t.pendown()
                for x in range(1, 101):
                    p = testpath.point(x * 0.01)
                    t.goto(p.real, p.imag)
                t.penup()
                t.dot(3, "black")
