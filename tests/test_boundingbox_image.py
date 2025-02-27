from typing import Tuple
import unittest
import os
import pytest
import sys

from PIL import Image, ImageDraw, ImageColor, ImageChops
from svg.path.path import CubicBezier, QuadraticBezier, Line, Arc, PathSegment
from .font import get_better_than_nothing_font


RED = ImageColor.getrgb("red")
GREEN = ImageColor.getrgb("limegreen")
BLUE = ImageColor.getrgb("cornflowerblue")
YELLOW = ImageColor.getrgb("yellow")
CYAN = ImageColor.getrgb("cyan")
WHITE = ImageColor.getrgb("white")
BLACK = ImageColor.getrgb("black")

DOT = 4 + 4j  # x+y radius of dot


def c2t(c: complex) -> Tuple[float, float]:
    """Make a complex number into a tuple"""
    return c.real, c.imag


class BoundingBoxImageTest(unittest.TestCase):
    """Creates a PNG image and compares with a correct PNG to test boundingbox capability"""

    def setUp(self) -> None:
        self.image = Image.new(mode="RGB", size=(500, 1200))
        self.draw = ImageDraw.Draw(self.image)

    def draw_path(self, path: PathSegment) -> None:
        lines = [c2t(path.point(x * 0.01)) for x in range(1, 101)]
        self.draw.line(lines, fill=WHITE, width=2)

        p = path.point(0)
        self.draw.ellipse([c2t(p - DOT), c2t(p + DOT)], fill=BLUE)
        p = path.point(1)
        self.draw.ellipse([c2t(p - DOT), c2t(p + DOT)], fill=GREEN)

    def draw_boundingbox(self, path: PathSegment) -> None:
        x1, y1, x2, y2 = path.boundingbox()
        self.draw.line(
            [
                (x1, y1),
                (x2, y1),
                (x2, y2),
                (x1, y2),
                (x1, y1),
            ],
            fill=RED,
            width=2,
        )

    @pytest.mark.skipif(
        sys.platform != "linux", reason="Different platforms have different fonts"
    )
    def test_image(self) -> None:
        font = get_better_than_nothing_font()
        self.draw.text((10, 10), "This is an SVG line:", font=font)
        self.draw.text((10, 100), "The red line is a bounding box.", font=font)

        line1 = Line(40 + 60j, 200 + 80j)
        self.draw_path(line1)
        self.draw_boundingbox(line1)

        self.draw.text((10, 140), "These are Arc segments:", font=font)
        arc1 = Arc(260 + 320j, 100 + 100j, 0, 1, 1, 260 + 319j)
        self.draw_path(arc1)
        self.draw_boundingbox(arc1)

        arc2 = Arc(450 + 320j, 40 + 80j, 50, 1, 1, 420 + 319j)
        self.draw_path(arc2)
        self.draw_boundingbox(arc2)

        arc3 = Arc(400 + 260j, 40 + 70j, 50, 0, 1, 340 + 260j)
        self.draw_path(arc3)
        self.draw_boundingbox(arc3)

        self.draw.text(
            (10, 500),
            "Next we have a quadratic bezier curve, with one tangent:",
            font=font,
        )
        start = 30 + 600j
        control = 400 + 540j
        end = 260 + 650j
        qbez1 = QuadraticBezier(start, control, end)
        self.draw_path(qbez1)
        self.draw.ellipse([c2t(control - DOT), c2t(control + DOT)], fill=WHITE)
        self.draw.line([c2t(start), c2t(control), c2t(end)], fill=CYAN)
        self.draw_boundingbox(qbez1)
        self.draw.text(
            (10, 670),
            "The white dot is the control point, and the cyan lines are ",
            font=font,
        )
        self.draw.text(
            (10, 690), "illustrating the how the control point works.", font=font
        )

        self.draw.text(
            (10, 730),
            "Lastly is a cubic bezier, with 2 tangents, and 2 control points:",
            font=font,
        )

        start = 200 + 800j
        control1 = 350 + 750j
        control2 = 50 + 900j
        end = 190 + 980j
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
        self.draw_boundingbox(cbez1)

        # self.image.show()  # Useful when debugging

        filename = os.path.join(
            os.path.split(__file__)[0], "test_boundingbox_image.png"
        )

        # If you have made intentional changes to the test_boundingbox_image.png,
        # save it by uncommenting these lines. Don't forget to comment them out again,
        # or the test will always pass
        # with open(filename, "wb") as fp:
        #     self.image.save(fp, format="PNG")

        with open(filename, "rb") as fp:
            test_image = Image.open(fp, mode="r")
            diff = ImageChops.difference(test_image, self.image)
            self.assertFalse(
                diff.getbbox(),
                "The resulting image is different from test_boundingbox_image.png",
            )
