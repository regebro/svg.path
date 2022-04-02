import unittest
from math import sqrt, pi

from ..path import CubicBezier, QuadraticBezier, Line, Arc, Move, Close, Path
from ..parser import parse_path


# Most of these test points are not calculated separately, as that would
# take too long and be too error prone. Instead the curves have been verified
# to be correct visually, by drawing them with the turtle module, with code
# like this:
#
#        import turtle
#        t = turtle.Turtle()
#        t.penup()
#
#        for arc in (path1, path2):
#            p = arc.point(0)
#            t.goto(p.real - 500, -p.imag + 300)
#            t.dot(3, 'black')
#            t.pendown()
#            for x in range(1, 101):
#                p = arc.point(x * 0.01)
#                t.goto(p.real - 500, -p.imag + 300)
#            t.penup()
#            t.dot(3, 'black')
#
#        raw_input()
#
# After the paths have been verified to be correct this way, the testing of
# points along the paths has been added as regression tests, to make sure
# nobody changes the way curves are drawn by mistake. Therefore, do not take
# these points religiously. They might be subtly wrong, unless otherwise
# noted.


class LineTest(unittest.TestCase):
    def test_lines(self):
        # These points are calculated, and not just regression tests.

        line1 = Line(0j, 400 + 0j)
        self.assertAlmostEqual(line1.point(0), (0j))
        self.assertAlmostEqual(line1.point(0.3), (120 + 0j))
        self.assertAlmostEqual(line1.point(0.5), (200 + 0j))
        self.assertAlmostEqual(line1.point(0.9), (360 + 0j))
        self.assertAlmostEqual(line1.point(1), (400 + 0j))
        self.assertAlmostEqual(line1.length(), 400)

        line2 = Line(400 + 0j, 400 + 300j)
        self.assertAlmostEqual(line2.point(0), (400 + 0j))
        self.assertAlmostEqual(line2.point(0.3), (400 + 90j))
        self.assertAlmostEqual(line2.point(0.5), (400 + 150j))
        self.assertAlmostEqual(line2.point(0.9), (400 + 270j))
        self.assertAlmostEqual(line2.point(1), (400 + 300j))
        self.assertAlmostEqual(line2.length(), 300)

        line3 = Line(400 + 300j, 0j)
        self.assertAlmostEqual(line3.point(0), (400 + 300j))
        self.assertAlmostEqual(line3.point(0.3), (280 + 210j))
        self.assertAlmostEqual(line3.point(0.5), (200 + 150j))
        self.assertAlmostEqual(line3.point(0.9), (40 + 30j))
        self.assertAlmostEqual(line3.point(1), (0j))
        self.assertAlmostEqual(line3.length(), 500)

    def test_equality(self):
        # This is to test the __eq__ and __ne__ methods, so we can't use
        # assertEqual and assertNotEqual
        line = Line(0j, 400 + 0j)
        self.assertTrue(line == Line(0, 400))
        self.assertTrue(line != Line(100, 400))
        self.assertFalse(line == str(line))
        self.assertTrue(line != str(line))
        self.assertFalse(
            CubicBezier(600 + 500j, 600 + 350j, 900 + 650j, 900 + 500j) == line
        )


class CubicBezierTest(unittest.TestCase):
    def test_approx_circle(self):
        """This is a approximate circle drawn in Inkscape"""

        arc1 = CubicBezier(
            complex(0, 0),
            complex(0, 109.66797),
            complex(-88.90345, 198.57142),
            complex(-198.57142, 198.57142),
        )

        self.assertAlmostEqual(arc1.point(0), (0j))
        self.assertAlmostEqual(arc1.point(0.1), (-2.59896457 + 32.20931647j))
        self.assertAlmostEqual(arc1.point(0.2), (-10.12330256 + 62.76392816j))
        self.assertAlmostEqual(arc1.point(0.3), (-22.16418039 + 91.25500149j))
        self.assertAlmostEqual(arc1.point(0.4), (-38.31276448 + 117.27370288j))
        self.assertAlmostEqual(arc1.point(0.5), (-58.16022125 + 140.41119875j))
        self.assertAlmostEqual(arc1.point(0.6), (-81.29771712 + 160.25865552j))
        self.assertAlmostEqual(arc1.point(0.7), (-107.31641851 + 176.40723961j))
        self.assertAlmostEqual(arc1.point(0.8), (-135.80749184 + 188.44811744j))
        self.assertAlmostEqual(arc1.point(0.9), (-166.36210353 + 195.97245543j))
        self.assertAlmostEqual(arc1.point(1), (-198.57142 + 198.57142j))

        arc2 = CubicBezier(
            complex(-198.57142, 198.57142),
            complex(-109.66797 - 198.57142, 0 + 198.57142),
            complex(-198.57143 - 198.57142, -88.90345 + 198.57142),
            complex(-198.57143 - 198.57142, 0),
        )

        self.assertAlmostEqual(arc2.point(0), (-198.57142 + 198.57142j))
        self.assertAlmostEqual(arc2.point(0.1), (-230.78073675 + 195.97245543j))
        self.assertAlmostEqual(arc2.point(0.2), (-261.3353492 + 188.44811744j))
        self.assertAlmostEqual(arc2.point(0.3), (-289.82642365 + 176.40723961j))
        self.assertAlmostEqual(arc2.point(0.4), (-315.8451264 + 160.25865552j))
        self.assertAlmostEqual(arc2.point(0.5), (-338.98262375 + 140.41119875j))
        self.assertAlmostEqual(arc2.point(0.6), (-358.830082 + 117.27370288j))
        self.assertAlmostEqual(arc2.point(0.7), (-374.97866745 + 91.25500149j))
        self.assertAlmostEqual(arc2.point(0.8), (-387.0195464 + 62.76392816j))
        self.assertAlmostEqual(arc2.point(0.9), (-394.54388515 + 32.20931647j))
        self.assertAlmostEqual(arc2.point(1), (-397.14285 + 0j))

        arc3 = CubicBezier(
            complex(-198.57143 - 198.57142, 0),
            complex(0 - 198.57143 - 198.57142, -109.66797),
            complex(88.90346 - 198.57143 - 198.57142, -198.57143),
            complex(-198.57142, -198.57143),
        )

        self.assertAlmostEqual(arc3.point(0), (-397.14285 + 0j))
        self.assertAlmostEqual(arc3.point(0.1), (-394.54388515 - 32.20931675j))
        self.assertAlmostEqual(arc3.point(0.2), (-387.0195464 - 62.7639292j))
        self.assertAlmostEqual(arc3.point(0.3), (-374.97866745 - 91.25500365j))
        self.assertAlmostEqual(arc3.point(0.4), (-358.830082 - 117.2737064j))
        self.assertAlmostEqual(arc3.point(0.5), (-338.98262375 - 140.41120375j))
        self.assertAlmostEqual(arc3.point(0.6), (-315.8451264 - 160.258662j))
        self.assertAlmostEqual(arc3.point(0.7), (-289.82642365 - 176.40724745j))
        self.assertAlmostEqual(arc3.point(0.8), (-261.3353492 - 188.4481264j))
        self.assertAlmostEqual(arc3.point(0.9), (-230.78073675 - 195.97246515j))
        self.assertAlmostEqual(arc3.point(1), (-198.57142 - 198.57143j))

        arc4 = CubicBezier(
            complex(-198.57142, -198.57143),
            complex(109.66797 - 198.57142, 0 - 198.57143),
            complex(0, 88.90346 - 198.57143),
            complex(0, 0),
        )

        self.assertAlmostEqual(arc4.point(0), (-198.57142 - 198.57143j))
        self.assertAlmostEqual(arc4.point(0.1), (-166.36210353 - 195.97246515j))
        self.assertAlmostEqual(arc4.point(0.2), (-135.80749184 - 188.4481264j))
        self.assertAlmostEqual(arc4.point(0.3), (-107.31641851 - 176.40724745j))
        self.assertAlmostEqual(arc4.point(0.4), (-81.29771712 - 160.258662j))
        self.assertAlmostEqual(arc4.point(0.5), (-58.16022125 - 140.41120375j))
        self.assertAlmostEqual(arc4.point(0.6), (-38.31276448 - 117.2737064j))
        self.assertAlmostEqual(arc4.point(0.7), (-22.16418039 - 91.25500365j))
        self.assertAlmostEqual(arc4.point(0.8), (-10.12330256 - 62.7639292j))
        self.assertAlmostEqual(arc4.point(0.9), (-2.59896457 - 32.20931675j))
        self.assertAlmostEqual(arc4.point(1), (0j))

    def test_svg_examples(self):

        # M100,200 C100,100 250,100 250,200
        path1 = CubicBezier(100 + 200j, 100 + 100j, 250 + 100j, 250 + 200j)
        self.assertAlmostEqual(path1.point(0), (100 + 200j))
        self.assertAlmostEqual(path1.point(0.3), (132.4 + 137j))
        self.assertAlmostEqual(path1.point(0.5), (175 + 125j))
        self.assertAlmostEqual(path1.point(0.9), (245.8 + 173j))
        self.assertAlmostEqual(path1.point(1), (250 + 200j))

        # S400,300 400,200
        path2 = CubicBezier(250 + 200j, 250 + 300j, 400 + 300j, 400 + 200j)
        self.assertAlmostEqual(path2.point(0), (250 + 200j))
        self.assertAlmostEqual(path2.point(0.3), (282.4 + 263j))
        self.assertAlmostEqual(path2.point(0.5), (325 + 275j))
        self.assertAlmostEqual(path2.point(0.9), (395.8 + 227j))
        self.assertAlmostEqual(path2.point(1), (400 + 200j))

        # M100,200 C100,100 400,100 400,200
        path3 = CubicBezier(100 + 200j, 100 + 100j, 400 + 100j, 400 + 200j)
        self.assertAlmostEqual(path3.point(0), (100 + 200j))
        self.assertAlmostEqual(path3.point(0.3), (164.8 + 137j))
        self.assertAlmostEqual(path3.point(0.5), (250 + 125j))
        self.assertAlmostEqual(path3.point(0.9), (391.6 + 173j))
        self.assertAlmostEqual(path3.point(1), (400 + 200j))

        # M100,500 C25,400 475,400 400,500
        path4 = CubicBezier(100 + 500j, 25 + 400j, 475 + 400j, 400 + 500j)
        self.assertAlmostEqual(path4.point(0), (100 + 500j))
        self.assertAlmostEqual(path4.point(0.3), (145.9 + 437j))
        self.assertAlmostEqual(path4.point(0.5), (250 + 425j))
        self.assertAlmostEqual(path4.point(0.9), (407.8 + 473j))
        self.assertAlmostEqual(path4.point(1), (400 + 500j))

        # M100,800 C175,700 325,700 400,800
        path5 = CubicBezier(100 + 800j, 175 + 700j, 325 + 700j, 400 + 800j)
        self.assertAlmostEqual(path5.point(0), (100 + 800j))
        self.assertAlmostEqual(path5.point(0.3), (183.7 + 737j))
        self.assertAlmostEqual(path5.point(0.5), (250 + 725j))
        self.assertAlmostEqual(path5.point(0.9), (375.4 + 773j))
        self.assertAlmostEqual(path5.point(1), (400 + 800j))

        # M600,200 C675,100 975,100 900,200
        path6 = CubicBezier(600 + 200j, 675 + 100j, 975 + 100j, 900 + 200j)
        self.assertAlmostEqual(path6.point(0), (600 + 200j))
        self.assertAlmostEqual(path6.point(0.3), (712.05 + 137j))
        self.assertAlmostEqual(path6.point(0.5), (806.25 + 125j))
        self.assertAlmostEqual(path6.point(0.9), (911.85 + 173j))
        self.assertAlmostEqual(path6.point(1), (900 + 200j))

        # M600,500 C600,350 900,650 900,500
        path7 = CubicBezier(600 + 500j, 600 + 350j, 900 + 650j, 900 + 500j)
        self.assertAlmostEqual(path7.point(0), (600 + 500j))
        self.assertAlmostEqual(path7.point(0.3), (664.8 + 462.2j))
        self.assertAlmostEqual(path7.point(0.5), (750 + 500j))
        self.assertAlmostEqual(path7.point(0.9), (891.6 + 532.4j))
        self.assertAlmostEqual(path7.point(1), (900 + 500j))

        # M600,800 C625,700 725,700 750,800
        path8 = CubicBezier(600 + 800j, 625 + 700j, 725 + 700j, 750 + 800j)
        self.assertAlmostEqual(path8.point(0), (600 + 800j))
        self.assertAlmostEqual(path8.point(0.3), (638.7 + 737j))
        self.assertAlmostEqual(path8.point(0.5), (675 + 725j))
        self.assertAlmostEqual(path8.point(0.9), (740.4 + 773j))
        self.assertAlmostEqual(path8.point(1), (750 + 800j))

        # S875,900 900,800
        inversion = (750 + 800j) + (750 + 800j) - (725 + 700j)
        path9 = CubicBezier(750 + 800j, inversion, 875 + 900j, 900 + 800j)
        self.assertAlmostEqual(path9.point(0), (750 + 800j))
        self.assertAlmostEqual(path9.point(0.3), (788.7 + 863j))
        self.assertAlmostEqual(path9.point(0.5), (825 + 875j))
        self.assertAlmostEqual(path9.point(0.9), (890.4 + 827j))
        self.assertAlmostEqual(path9.point(1), (900 + 800j))

    def test_length(self):

        # A straight line:
        arc = CubicBezier(
            complex(0, 0), complex(0, 0), complex(0, 100), complex(0, 100)
        )

        self.assertAlmostEqual(arc.length(), 100)

        # A diagonal line:
        arc = CubicBezier(
            complex(0, 0), complex(0, 0), complex(100, 100), complex(100, 100)
        )

        self.assertAlmostEqual(arc.length(), sqrt(2 * 100 * 100))

        # A quarter circle arc with radius 100:
        kappa = (
            4 * (sqrt(2) - 1) / 3
        )  # http://www.whizkidtech.redprince.net/bezier/circle/

        arc = CubicBezier(
            complex(0, 0),
            complex(0, kappa * 100),
            complex(100 - kappa * 100, 100),
            complex(100, 100),
        )

        # We can't compare with pi*50 here, because this is just an
        # approximation of a circle arc. pi*50 is 157.079632679
        # So this is just yet another "warn if this changes" test.
        # This value is not verified to be correct.
        self.assertAlmostEqual(arc.length(), 157.1016698)

        # A recursive solution has also been suggested, but for CubicBezier
        # curves it could get a false solution on curves where the midpoint is on a
        # straight line between the start and end. For example, the following
        # curve would get solved as a straight line and get the length 300.
        # Make sure this is not the case.
        arc = CubicBezier(
            complex(600, 500), complex(600, 350), complex(900, 650), complex(900, 500)
        )
        self.assertTrue(arc.length() > 300.0)

    def test_equality(self):
        # This is to test the __eq__ and __ne__ methods, so we can't use
        # assertEqual and assertNotEqual
        segment = CubicBezier(
            complex(600, 500), complex(600, 350), complex(900, 650), complex(900, 500)
        )

        self.assertTrue(
            segment == CubicBezier(600 + 500j, 600 + 350j, 900 + 650j, 900 + 500j)
        )
        self.assertTrue(
            segment != CubicBezier(600 + 501j, 600 + 350j, 900 + 650j, 900 + 500j)
        )
        self.assertTrue(segment != Line(0, 400))

    def test_smooth(self):
        cb1 = CubicBezier(0, 0, 100 + 100j, 100 + 100j)
        cb2 = CubicBezier(600 + 500j, 600 + 350j, 900 + 650j, 900 + 500j)
        self.assertFalse(cb2.is_smooth_from(cb1))
        cb2.set_smooth_from(cb1)
        self.assertTrue(cb2.is_smooth_from(cb1))


class QuadraticBezierTest(unittest.TestCase):
    def test_svg_examples(self):
        """These is the path in the SVG specs"""
        # M200,300 Q400,50 600,300 T1000,300
        path1 = QuadraticBezier(200 + 300j, 400 + 50j, 600 + 300j)
        self.assertAlmostEqual(path1.point(0), (200 + 300j))
        self.assertAlmostEqual(path1.point(0.3), (320 + 195j))
        self.assertAlmostEqual(path1.point(0.5), (400 + 175j))
        self.assertAlmostEqual(path1.point(0.9), (560 + 255j))
        self.assertAlmostEqual(path1.point(1), (600 + 300j))

        # T1000, 300
        inversion = (600 + 300j) + (600 + 300j) - (400 + 50j)
        path2 = QuadraticBezier(600 + 300j, inversion, 1000 + 300j)
        self.assertAlmostEqual(path2.point(0), (600 + 300j))
        self.assertAlmostEqual(path2.point(0.3), (720 + 405j))
        self.assertAlmostEqual(path2.point(0.5), (800 + 425j))
        self.assertAlmostEqual(path2.point(0.9), (960 + 345j))
        self.assertAlmostEqual(path2.point(1), (1000 + 300j))

    def test_length(self):
        # expected results calculated with
        # svg.path.segment_length(q, 0, 1, q.start, q.end, 1e-14, 20, 0)
        q1 = QuadraticBezier(200 + 300j, 400 + 50j, 600 + 300j)
        q2 = QuadraticBezier(200 + 300j, 400 + 50j, 500 + 200j)
        closedq = QuadraticBezier(6 + 2j, 5 - 1j, 6 + 2j)
        linq1 = QuadraticBezier(1, 2, 3)
        linq2 = QuadraticBezier(1 + 3j, 2 + 5j, -9 - 17j)
        nodalq = QuadraticBezier(1, 1, 1)
        tests = [
            (q1, 487.77109389525975),
            (q2, 379.90458193489155),
            (closedq, 3.1622776601683795),
            (linq1, 2),
            (linq2, 22.73335777124786),
            (nodalq, 0),
        ]
        for q, exp_res in tests:
            self.assertAlmostEqual(q.length(), exp_res)

    def test_equality(self):
        # This is to test the __eq__ and __ne__ methods, so we can't use
        # assertEqual and assertNotEqual
        segment = QuadraticBezier(200 + 300j, 400 + 50j, 600 + 300j)
        self.assertTrue(segment == QuadraticBezier(200 + 300j, 400 + 50j, 600 + 300j))
        self.assertTrue(segment != QuadraticBezier(200 + 301j, 400 + 50j, 600 + 300j))
        self.assertFalse(segment == Arc(0j, 100 + 50j, 0, 0, 0, 100 + 50j))
        self.assertTrue(Arc(0j, 100 + 50j, 0, 0, 0, 100 + 50j) != segment)

    def test_linear_arcs_issue_61(self):
        p = parse_path("M 206.5,525 Q 162.5,583 162.5,583")
        self.assertAlmostEqual(p.length(), 72.80109889280519)
        p = parse_path("M 425.781 446.289 Q 410.40000000000003 373.047 410.4 373.047")
        self.assertAlmostEqual(p.length(), 74.83959997888816)
        p = parse_path("M 639.648 568.115 Q 606.6890000000001 507.568 606.689 507.568")
        self.assertAlmostEqual(p.length(), 68.93645544992873)
        p = parse_path("M 288.818 616.699 Q 301.025 547.3629999999999 301.025 547.363")
        self.assertAlmostEqual(p.length(), 70.40235610403947)
        p = parse_path("M 339.927 706.25 Q 243.92700000000002 806.25 243.927 806.25")
        self.assertAlmostEqual(p.length(), 138.6217876093077)
        p = parse_path(
            "M 539.795 702.637 Q 548.0959999999999 803.4669999999999 548.096 803.467"
        )
        self.assertAlmostEqual(p.length(), 101.17111989594662)
        p = parse_path(
            "M 537.815 555.042 Q 570.1680000000001 499.1600000000001 570.168 499.16"
        )
        self.assertAlmostEqual(p.length(), 64.57177814649368)
        p = parse_path("M 615.297 470.503 Q 538.797 694.5029999999999 538.797 694.503")
        self.assertAlmostEqual(p.length(), 236.70287281737836)

    def test_smooth(self):
        cb1 = QuadraticBezier(200 + 300j, 400 + 50j, 600 + 300j)
        cb2 = QuadraticBezier(600 + 300j, 400 + 50j, 1000 + 300j)
        self.assertFalse(cb2.is_smooth_from(cb1))
        cb2.set_smooth_from(cb1)
        self.assertTrue(cb2.is_smooth_from(cb1))


class ArcTest(unittest.TestCase):
    def test_points(self):
        arc1 = Arc(0j, 100 + 50j, 0, 0, 0, 100 + 50j)
        self.assertAlmostEqual(arc1.center, 100 + 0j)
        self.assertAlmostEqual(arc1.theta, 180.0)
        self.assertAlmostEqual(arc1.delta, -90.0)

        self.assertAlmostEqual(arc1.point(0.0), (0j))
        self.assertAlmostEqual(arc1.point(0.1), (1.23116594049 + 7.82172325201j))
        self.assertAlmostEqual(arc1.point(0.2), (4.89434837048 + 15.4508497187j))
        self.assertAlmostEqual(arc1.point(0.3), (10.8993475812 + 22.699524987j))
        self.assertAlmostEqual(arc1.point(0.4), (19.0983005625 + 29.3892626146j))
        self.assertAlmostEqual(arc1.point(0.5), (29.2893218813 + 35.3553390593j))
        self.assertAlmostEqual(arc1.point(0.6), (41.2214747708 + 40.4508497187j))
        self.assertAlmostEqual(arc1.point(0.7), (54.6009500260 + 44.5503262094j))
        self.assertAlmostEqual(arc1.point(0.8), (69.0983005625 + 47.5528258148j))
        self.assertAlmostEqual(arc1.point(0.9), (84.3565534960 + 49.3844170298j))
        self.assertAlmostEqual(arc1.point(1.0), (100 + 50j))

        arc2 = Arc(0j, 100 + 50j, 0, 1, 0, 100 + 50j)
        self.assertAlmostEqual(arc2.center, 50j)
        self.assertAlmostEqual(arc2.theta, 270.0)
        self.assertAlmostEqual(arc2.delta, -270.0)

        self.assertAlmostEqual(arc2.point(0.0), (0j))
        self.assertAlmostEqual(arc2.point(0.1), (-45.399049974 + 5.44967379058j))
        self.assertAlmostEqual(arc2.point(0.2), (-80.9016994375 + 20.6107373854j))
        self.assertAlmostEqual(arc2.point(0.3), (-98.7688340595 + 42.178276748j))
        self.assertAlmostEqual(arc2.point(0.4), (-95.1056516295 + 65.4508497187j))
        self.assertAlmostEqual(arc2.point(0.5), (-70.7106781187 + 85.3553390593j))
        self.assertAlmostEqual(arc2.point(0.6), (-30.9016994375 + 97.5528258148j))
        self.assertAlmostEqual(arc2.point(0.7), (15.643446504 + 99.3844170298j))
        self.assertAlmostEqual(arc2.point(0.8), (58.7785252292 + 90.4508497187j))
        self.assertAlmostEqual(arc2.point(0.9), (89.1006524188 + 72.699524987j))
        self.assertAlmostEqual(arc2.point(1.0), (100 + 50j))

        arc3 = Arc(0j, 100 + 50j, 0, 0, 1, 100 + 50j)
        self.assertAlmostEqual(arc3.center, 50j)
        self.assertAlmostEqual(arc3.theta, 270.0)
        self.assertAlmostEqual(arc3.delta, 90.0)

        self.assertAlmostEqual(arc3.point(0.0), (0j))
        self.assertAlmostEqual(arc3.point(0.1), (15.643446504 + 0.615582970243j))
        self.assertAlmostEqual(arc3.point(0.2), (30.9016994375 + 2.44717418524j))
        self.assertAlmostEqual(arc3.point(0.3), (45.399049974 + 5.44967379058j))
        self.assertAlmostEqual(arc3.point(0.4), (58.7785252292 + 9.54915028125j))
        self.assertAlmostEqual(arc3.point(0.5), (70.7106781187 + 14.6446609407j))
        self.assertAlmostEqual(arc3.point(0.6), (80.9016994375 + 20.6107373854j))
        self.assertAlmostEqual(arc3.point(0.7), (89.1006524188 + 27.300475013j))
        self.assertAlmostEqual(arc3.point(0.8), (95.1056516295 + 34.5491502813j))
        self.assertAlmostEqual(arc3.point(0.9), (98.7688340595 + 42.178276748j))
        self.assertAlmostEqual(arc3.point(1.0), (100 + 50j))

        arc4 = Arc(0j, 100 + 50j, 0, 1, 1, 100 + 50j)
        self.assertAlmostEqual(arc4.center, 100 + 0j)
        self.assertAlmostEqual(arc4.theta, 180.0)
        self.assertAlmostEqual(arc4.delta, 270.0)

        self.assertAlmostEqual(arc4.point(0.0), (0j))
        self.assertAlmostEqual(arc4.point(0.1), (10.8993475812 - 22.699524987j))
        self.assertAlmostEqual(arc4.point(0.2), (41.2214747708 - 40.4508497187j))
        self.assertAlmostEqual(arc4.point(0.3), (84.3565534960 - 49.3844170298j))
        self.assertAlmostEqual(arc4.point(0.4), (130.901699437 - 47.5528258148j))
        self.assertAlmostEqual(arc4.point(0.5), (170.710678119 - 35.3553390593j))
        self.assertAlmostEqual(arc4.point(0.6), (195.105651630 - 15.4508497187j))
        self.assertAlmostEqual(arc4.point(0.7), (198.768834060 + 7.82172325201j))
        self.assertAlmostEqual(arc4.point(0.8), (180.901699437 + 29.3892626146j))
        self.assertAlmostEqual(arc4.point(0.9), (145.399049974 + 44.5503262094j))
        self.assertAlmostEqual(arc4.point(1.0), (100 + 50j))

    def test_length(self):
        # I'll test the length calculations by making a circle, in two parts.
        arc1 = Arc(0j, 100 + 100j, 0, 0, 0, 200 + 0j)
        arc2 = Arc(200 + 0j, 100 + 100j, 0, 0, 0, 0j)
        self.assertAlmostEqual(arc1.length(), pi * 100)
        self.assertAlmostEqual(arc2.length(), pi * 100)

    def test_length_out_of_range(self):
        # See F.6.2 Out-of-range parameters

        # If the endpoints (x1, y1) and (x2, y2) are identical, then this is
        # equivalent to omitting the elliptical arc segment entirely.
        arc = Arc(0j, 100 + 100j, 0, 0, 0, 0j)
        self.assertAlmostEqual(arc.length(), 0)

        # If rx = 0 or ry = 0 then this arc is treated as a straight
        # line segment (a "lineto") joining the endpoints.
        arc = Arc(0j, 0j, 0, 0, 0, 200 + 0j)
        self.assertAlmostEqual(arc.length(), 200)

        # If rx or ry have negative signs, these are dropped;
        # the absolute value is used instead.
        arc = Arc(200 + 0j, -100 - 100j, 0, 0, 0, 0j)
        self.assertAlmostEqual(arc.length(), pi * 100)

        # If rx, ry and φ are such that there is no solution (basically,
        # the ellipse is not big enough to reach from (x1, y1) to (x2, y2))
        # then the ellipse is scaled up uniformly until there is exactly
        # one solution (until the ellipse is just big enough).
        arc = Arc(0j, 1 + 1j, 0, 0, 0, 200 + 0j)
        self.assertAlmostEqual(arc.length(), pi * 100)

        # φ is taken mod 360 degrees.
        arc = Arc(200 + 0j, -100 - 100j, 720, 0, 0, 0j)
        self.assertAlmostEqual(arc.length(), pi * 100)

    def test_equality(self):
        # This is to test the __eq__ and __ne__ methods, so we can't use
        # assertEqual and assertNotEqual
        segment = Arc(0j, 100 + 50j, 0, 0, 0, 100 + 50j)
        self.assertTrue(segment == Arc(0j, 100 + 50j, 0, 0, 0, 100 + 50j))
        self.assertTrue(segment != Arc(0j, 100 + 50j, 0, 1, 0, 100 + 50j))

    def test_issue25(self):
        # This raised a math domain error
        Arc(
            (725.307482225571 - 915.5548199281527j),
            (202.79421639137703 + 148.77294617167183j),
            225.6910319606926,
            1,
            1,
            (-624.6375539637027 + 896.5483089399895j),
        )


class TestPath(unittest.TestCase):
    def test_circle(self):
        arc1 = Arc(0j, 100 + 100j, 0, 0, 0, 200 + 0j)
        arc2 = Arc(200 + 0j, 100 + 100j, 0, 0, 0, 0j)
        path = Path(arc1, arc2)
        self.assertAlmostEqual(path.point(0.0), (0j))
        self.assertAlmostEqual(path.point(0.25), (100 + 100j))
        self.assertAlmostEqual(path.point(0.5), (200 + 0j))
        self.assertAlmostEqual(path.point(0.75), (100 - 100j))
        self.assertAlmostEqual(path.point(1.0), (0j))
        self.assertAlmostEqual(path.length(), pi * 200)

    def test_svg_specs(self):
        """The paths that are in the SVG specs"""

        # Big pie: M300,200 h-150 a150,150 0 1,0 150,-150 z
        path = Path(
            Line(300 + 200j, 150 + 200j),
            Arc(150 + 200j, 150 + 150j, 0, 1, 0, 300 + 50j),
            Line(300 + 50j, 300 + 200j),
        )
        # The points and length for this path are calculated and not regression tests.
        self.assertAlmostEqual(path.point(0.0), (300 + 200j))
        self.assertAlmostEqual(path.point(0.14897825542), (150 + 200j))
        self.assertAlmostEqual(path.point(0.5), (406.066017177 + 306.066017177j))
        self.assertAlmostEqual(path.point(1 - 0.14897825542), (300 + 50j))
        self.assertAlmostEqual(path.point(1.0), (300 + 200j))
        # The errors seem to accumulate. Still 6 decimal places is more than good enough.
        self.assertAlmostEqual(path.length(), pi * 225 + 300, places=6)

        # Little pie: M275,175 v-150 a150,150 0 0,0 -150,150 z
        path = Path(
            Line(275 + 175j, 275 + 25j),
            Arc(275 + 25j, 150 + 150j, 0, 0, 0, 125 + 175j),
            Line(125 + 175j, 275 + 175j),
        )
        # The points and length for this path are calculated and not regression tests.
        self.assertAlmostEqual(path.point(0.0), (275 + 175j))
        self.assertAlmostEqual(path.point(0.2800495767557787), (275 + 25j))
        self.assertAlmostEqual(
            path.point(0.5), (168.93398282201787 + 68.93398282201787j)
        )
        self.assertAlmostEqual(path.point(1 - 0.2800495767557787), (125 + 175j))
        self.assertAlmostEqual(path.point(1.0), (275 + 175j))
        # The errors seem to accumulate. Still 6 decimal places is more than good enough.
        self.assertAlmostEqual(path.length(), pi * 75 + 300, places=6)

        # Bumpy path: M600,350 l 50,-25
        #             a25,25 -30 0,1 50,-25 l 50,-25
        #             a25,50 -30 0,1 50,-25 l 50,-25
        #             a25,75 -30 0,1 50,-25 l 50,-25
        #             a25,100 -30 0,1 50,-25 l 50,-25
        path = Path(
            Line(600 + 350j, 650 + 325j),
            Arc(650 + 325j, 25 + 25j, -30, 0, 1, 700 + 300j),
            Line(700 + 300j, 750 + 275j),
            Arc(750 + 275j, 25 + 50j, -30, 0, 1, 800 + 250j),
            Line(800 + 250j, 850 + 225j),
            Arc(850 + 225j, 25 + 75j, -30, 0, 1, 900 + 200j),
            Line(900 + 200j, 950 + 175j),
            Arc(950 + 175j, 25 + 100j, -30, 0, 1, 1000 + 150j),
            Line(1000 + 150j, 1050 + 125j),
        )

        # These are *not* calculated, but just regression tests. Be skeptical.
        self.assertAlmostEqual(path.point(0.0), (600 + 350j))
        self.assertAlmostEqual(path.point(0.3), (755.23979927 + 212.1820209585j))
        self.assertAlmostEqual(path.point(0.5), (827.73074926 + 147.8241574162j))
        self.assertAlmostEqual(path.point(0.9), (971.28435780 + 106.3023526073j))
        self.assertAlmostEqual(path.point(1.0), (1050 + 125j))
        self.assertAlmostEqual(path.length(), 928.388639381)

    def test_repr(self):
        path = Path(
            Line(start=600 + 350j, end=650 + 325j),
            Arc(
                start=650 + 325j,
                radius=25 + 25j,
                rotation=-30,
                arc=0,
                sweep=1,
                end=700 + 300j,
            ),
            CubicBezier(
                start=700 + 300j,
                control1=800 + 400j,
                control2=750 + 200j,
                end=600 + 100j,
            ),
            QuadraticBezier(start=600 + 100j, control=600, end=600 + 300j),
        )
        self.assertEqual(eval(repr(path)), path)

    def test_reverse(self):
        # Currently you can't reverse paths.
        self.assertRaises(NotImplementedError, Path().reverse)

    def test_equality(self):
        # This is to test the __eq__ and __ne__ methods, so we can't use
        # assertEqual and assertNotEqual
        path1 = Path(
            Line(start=600 + 350j, end=650 + 325j),
            Arc(
                start=650 + 325j,
                radius=25 + 25j,
                rotation=-30,
                arc=0,
                sweep=1,
                end=700 + 300j,
            ),
            CubicBezier(
                start=700 + 300j,
                control1=800 + 400j,
                control2=750 + 200j,
                end=600 + 100j,
            ),
            QuadraticBezier(start=600 + 100j, control=600, end=600 + 300j),
        )
        path2 = Path(
            Line(start=600 + 350j, end=650 + 325j),
            Arc(
                start=650 + 325j,
                radius=25 + 25j,
                rotation=-30,
                arc=0,
                sweep=1,
                end=700 + 300j,
            ),
            CubicBezier(
                start=700 + 300j,
                control1=800 + 400j,
                control2=750 + 200j,
                end=600 + 100j,
            ),
            QuadraticBezier(start=600 + 100j, control=600, end=600 + 300j),
        )

        self.assertTrue(path1 == path2)
        # Modify path2:
        path2[0].start = 601 + 350j
        self.assertTrue(path1 != path2)

        # Modify back:
        path2[0].start = 600 + 350j
        self.assertFalse(path1 != path2)

        # Get rid of the last segment:
        del path2[-1]
        self.assertFalse(path1 == path2)

        # It's not equal to a list of it's segments
        self.assertTrue(path1 != path1[:])
        self.assertFalse(path1 == path1[:])

    def test_non_arc(self):
        # And arc with the same start and end is a noop.
        segment = Arc(0j + 70j, 35 + 35j, 0, 1, 0, 0 + 70j)
        self.assertEqual(segment.length(), 0)
        self.assertEqual(segment.point(0.5), segment.start)

    def test_zero_paths(self):
        move_only = Path(Move(0))
        self.assertEqual(move_only.point(0), 0 + 0j)
        self.assertEqual(move_only.point(0.5), 0 + 0j)
        self.assertEqual(move_only.point(1), 0 + 0j)
        self.assertEqual(move_only.length(), 0)

        move_onlyz = Path(Move(0), Close(0, 0))
        self.assertEqual(move_onlyz.point(0), 0 + 0j)
        self.assertEqual(move_onlyz.point(0.5), 0 + 0j)
        self.assertEqual(move_onlyz.point(1), 0 + 0j)
        self.assertEqual(move_onlyz.length(), 0)

        zero_line = Path(Move(0), Line(0, 0))
        self.assertEqual(zero_line.point(0), 0 + 0j)
        self.assertEqual(zero_line.point(0.5), 0 + 0j)
        self.assertEqual(zero_line.point(1), 0 + 0j)
        self.assertEqual(zero_line.length(), 0)

        only_line = Path(Line(1 + 1j, 1 + 1j))
        self.assertEqual(only_line.point(0), 1 + 1j)
        self.assertEqual(only_line.point(0.5), 1 + 1j)
        self.assertEqual(only_line.point(1), 1 + 1j)
        self.assertEqual(only_line.length(), 0)

    def test_tangent(self):
        path = Path(
            Line(start=600 + 350j, end=650 + 325j),
            Arc(
                start=650 + 325j,
                radius=25 + 25j,
                rotation=-30,
                arc=0,
                sweep=1,
                end=700 + 300j,
            ),
            CubicBezier(
                start=700 + 300j,
                control1=800 + 400j,
                control2=750 + 200j,
                end=600 + 100j,
            ),
            QuadraticBezier(start=600 + 100j, control=600, end=600 + 300j),
        )

        self.assertEqual(path.tangent(0), 50 - 25j)
        # These are *not* calculated, but just regression tests. Be skeptical.
        self.assertAlmostEqual(
            path.tangent(0.25), 197.17077123205894 + 106.56022001841387j
        )
        self.assertAlmostEqual(
            path.tangent(0.5), -226.30788045372367 - 364.5433357646594j
        )
        self.assertAlmostEqual(path.tangent(0.75), 13.630819414210208j)
        self.assertAlmostEqual(path.tangent(1), 600j)

    def test_tangent_magnitude(self):

        line1 = Line(start=6 + 3.5j, end=6.5 + 3.25j)
        line2 = Line(start=6 + 3.5j, end=7 + 3j)
        # line2 is twice as long as line1, the tangent should have twice the magnitude:
        self.assertAlmostEqual(line2.tangent(0.5) / line1.tangent(0.5), 2)

        arc1 = Arc(
            start=0 - 2.5j, radius=2.5 + 2.5j, rotation=0, arc=0, sweep=1, end=0 + 2.5j
        )
        arc2 = Arc(start=0 - 5j, radius=5 + 5j, rotation=0, arc=0, sweep=1, end=0 + 5j)
        # The radius is twice as large, so the magnitude is twice as large
        self.assertAlmostEqual(arc2.tangent(0.5) / arc1.tangent(0.5), 2)

        bez1 = CubicBezier(start=0, control1=1 + 1j, control2=2 - 1j, end=3)
        bez2 = CubicBezier(start=0, control1=2 + 2j, control2=4 - 2j, end=6)
        # Length should be double, tangent is double.
        self.assertAlmostEqual(bez2.tangent(0.5) / bez1.tangent(0.5), 2)

        qb1 = QuadraticBezier(start=0, control=1 + 1j, end=2)
        qb2 = QuadraticBezier(start=0, control=2 + 2j, end=4)
        # Length should be double, tangent is double.
        self.assertAlmostEqual(qb2.tangent(0.5) / qb1.tangent(0.5), 2)

        # Code for visually verifying these tangents. I should make a test of this.
        # import turtle
        # t = turtle.Turtle()
        # t.penup()

        # for arc in (line1, line2, arc1, arc2, bez1, bez2):
        # p = arc.point(0)
        # t.goto(p.real*20, -p.imag*20)
        # t.dot(3, 'black')
        # t.pendown()
        # for x in range(1, 101):
        # p = arc.point(x * 0.01)
        # t.goto(p.real*20,-p.imag*20)
        # t.penup()
        # t.dot(3, 'black')
        # p = arc.point(0.5)
        # t.goto(p.real*20,-p.imag*20)
        # t.dot(3, 'red')
        # t.pendown()
        # p += arc.tangent(0.5)
        # t.goto(p.real*20,-p.imag*20)
        # t.penup()
