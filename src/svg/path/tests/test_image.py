import unittest
import os
from PIL import Image, ImageDraw, ImageColor, ImageChops
from math import sqrt

from ..path import CubicBezier, QuadraticBezier, Line, Arc


RED = ImageColor.getcolor("red", mode="RGB")
GREEN = ImageColor.getcolor("limegreen", mode="RGB")
BLUE = ImageColor.getcolor("cornflowerblue", mode="RGB")
YELLOW = ImageColor.getcolor("yellow", mode="RGB")
CYAN = ImageColor.getcolor("cyan", mode="RGB")
WHITE = ImageColor.getcolor("white", mode="RGB")
BLACK = ImageColor.getcolor("black", mode="RGB")

DOT = 4 + 4j  # x+y radius of dot


def c2t(c):
    """Make a complex number into a tuple"""
    return c.real, c.imag


def magnitude(c):
    return sqrt(c.real**2 + c.imag**2)


class ImageTest(unittest.TestCase):
    """Creates a PNG image and compares with a correct PNG"""

    def setUp(self):
        self.image = Image.new(mode="RGB", size=(500, 1200))
        self.draw = ImageDraw.Draw(self.image)

    def draw_path(self, path):
        lines = [c2t(path.point(x * 0.01)) for x in range(1, 101)]
        self.draw.line(lines, fill=WHITE, width=2)

        p = path.point(0)
        self.draw.ellipse([c2t(p - DOT), c2t(p + DOT)], fill=BLUE)
        p = path.point(1)
        self.draw.ellipse([c2t(p - DOT), c2t(p + DOT)], fill=GREEN)

    def draw_tangents(self, path, count):
        count += 1
        for i in range(1, count):
            p = path.point(i / count)
            t = path.tangent(i / count)
            self.draw.line([c2t(p), c2t(p + t)], fill=RED, width=1)

            # And a nice 90 angle
            tt = complex(t.imag, -t.real)
            # scale it to always be 20px
            tt *= 20 / magnitude(tt)

            self.draw.line([c2t(p), c2t(tt + p)], fill=YELLOW, width=1)

    def test_image(self):
        self.draw.text((10, 10), "This is an SVG line:")
        self.draw.text(
            (10, 100),
            "The red line is a tangent, and the yellow is 90 degrees from that.",
        )

        line1 = Line(40 + 60j, 200 + 80j)
        self.draw_path(line1)
        self.draw_tangents(line1, 1)

        self.draw.text((10, 140), "This is an Arc segment, almost a whole circle:")
        arc1 = Arc(260 + 320j, 100 + 100j, 0, 1, 1, 260 + 319j)
        self.draw_path(arc1)
        self.draw_tangents(arc1, 5)
        self.draw.text((10, 460), "With five tangents.")

        self.draw.text(
            (10, 500),
            "Next we have a quadratic bezier curve, with one tangent:",
        )
        start = 30 + 600j
        control = 400 + 540j
        end = 260 + 650j
        qbez1 = QuadraticBezier(start, control, end)
        self.draw_path(qbez1)
        self.draw.ellipse([c2t(control - DOT), c2t(control + DOT)], fill=WHITE)
        self.draw.line([c2t(start), c2t(control), c2t(end)], fill=CYAN)
        self.draw_tangents(qbez1, 1)
        self.draw.text(
            (10, 670),
            "The white dot is the control point, and the cyan lines are ",
        )
        self.draw.text((10, 690), "illustrating the how the control point works.")

        self.draw.text(
            (10, 730),
            "Lastly is a cubic bezier, with 2 tangents, and 2 control points:",
        )

        start = 30 + 800j
        control1 = 400 + 780j
        control2 = 50 + 900j
        end = 300 + 980j
        cbez1 = CubicBezier(start, control1, control2, end)
        self.draw_path(cbez1)
        self.draw.ellipse([c2t(control1 - DOT), c2t(control1 + DOT)], fill=WHITE)
        self.draw.ellipse([c2t(control2 - DOT), c2t(control2 + DOT)], fill=WHITE)
        self.draw.line(
            [
                c2t(start),
                c2t(control1),
            ],
            fill=CYAN,
        )
        self.draw.line([c2t(control2), c2t(end)], fill=CYAN)
        self.draw_tangents(cbez1, 2)

        # self.image.show()  # Useful when debugging

        filename = os.path.join(os.path.split(__file__)[0], "test_image.png")

        # If you have made intentional changes to the test_image.png, save it
        # by uncommenting these lines. Don't forget to comment them out again,
        # or the test will always pass
        # with open(filename, "wb") as fp:
        #     self.image.save(fp, format="PNG")

        with open(filename, "rb") as fp:
            test_image = Image.open(fp, mode="r")
            diff = ImageChops.difference(test_image, self.image)
            self.assertFalse(
                diff.getbbox(), "The resulting image is different from test_image.png"
            )
