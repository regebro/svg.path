import unittest
from ..path import CubicBezier, QuadraticBezier, Line, Arc, Path, Move, Close
from ..parser import parse_path


class TestParser(unittest.TestCase):
    maxDiff = None

    def test_svg_examples(self):
        """Examples from the SVG spec"""
        path1 = parse_path("M 100 100 L 300 100 L 200 300 z")
        self.assertEqual(
            path1,
            Path(
                Move(100 + 100j),
                Line(100 + 100j, 300 + 100j),
                Line(300 + 100j, 200 + 300j),
                Close(200 + 300j, 100 + 100j),
            ),
        )

        # for Z command behavior when there is multiple subpaths
        path1 = parse_path("M 0 0 L 50 20 M 100 100 L 300 100 L 200 300 z")
        self.assertEqual(
            path1,
            Path(
                Move(0j),
                Line(0 + 0j, 50 + 20j),
                Move(100 + 100j),
                Line(100 + 100j, 300 + 100j),
                Line(300 + 100j, 200 + 300j),
                Close(200 + 300j, 100 + 100j),
            ),
        )

        path1 = parse_path("M 100 100 L 200 200")
        path2 = parse_path("M100 100L200 200")
        self.assertEqual(path1, path2)

        path1 = parse_path("M 100 200 L 200 100 L -100 -200")
        path2 = parse_path("M 100 200 L 200 100 -100 -200")
        self.assertEqual(path1, path2)

        path1 = parse_path(
            """M100,200 C100,100 250,100 250,200
                              S400,300 400,200"""
        )
        self.assertEqual(
            path1,
            Path(
                Move(100 + 200j),
                CubicBezier(100 + 200j, 100 + 100j, 250 + 100j, 250 + 200j),
                CubicBezier(250 + 200j, 250 + 300j, 400 + 300j, 400 + 200j),
            ),
        )

        path1 = parse_path("M100,200 C100,100 400,100 400,200")
        self.assertEqual(
            path1,
            Path(
                Move(100 + 200j),
                CubicBezier(100 + 200j, 100 + 100j, 400 + 100j, 400 + 200j),
            ),
        )

        path1 = parse_path("M100,500 C25,400 475,400 400,500")
        self.assertEqual(
            path1,
            Path(
                Move(100 + 500j),
                CubicBezier(100 + 500j, 25 + 400j, 475 + 400j, 400 + 500j),
            ),
        )

        path1 = parse_path("M100,800 C175,700 325,700 400,800")
        self.assertEqual(
            path1,
            Path(
                Move(100 + 800j),
                CubicBezier(100 + 800j, 175 + 700j, 325 + 700j, 400 + 800j),
            ),
        )

        path1 = parse_path("M600,200 C675,100 975,100 900,200")
        self.assertEqual(
            path1,
            Path(
                Move(600 + 200j),
                CubicBezier(600 + 200j, 675 + 100j, 975 + 100j, 900 + 200j),
            ),
        )

        path1 = parse_path("M600,500 C600,350 900,650 900,500")
        self.assertEqual(
            path1,
            Path(
                Move(600 + 500j),
                CubicBezier(600 + 500j, 600 + 350j, 900 + 650j, 900 + 500j),
            ),
        )

        path1 = parse_path(
            """M600,800 C625,700 725,700 750,800
                              S875,900 900,800"""
        )
        self.assertEqual(
            path1,
            Path(
                Move(600 + 800j),
                CubicBezier(600 + 800j, 625 + 700j, 725 + 700j, 750 + 800j),
                CubicBezier(750 + 800j, 775 + 900j, 875 + 900j, 900 + 800j),
            ),
        )

        path1 = parse_path("M200,300 Q400,50 600,300 T1000,300")
        self.assertEqual(
            path1,
            Path(
                Move(200 + 300j),
                QuadraticBezier(200 + 300j, 400 + 50j, 600 + 300j),
                QuadraticBezier(600 + 300j, 800 + 550j, 1000 + 300j),
            ),
        )

        path1 = parse_path("M300,200 h-150 a150,150 0 1,0 150,-150 z")
        self.assertEqual(
            path1,
            Path(
                Move(300 + 200j),
                Line(300 + 200j, 150 + 200j),
                Arc(150 + 200j, 150 + 150j, 0, 1, 0, 300 + 50j),
                Close(300 + 50j, 300 + 200j),
            ),
        )

        path1 = parse_path("M275,175 v-150 a150,150 0 0,0 -150,150 z")
        self.assertEqual(
            path1,
            Path(
                Move(275 + 175j),
                Line(275 + 175j, 275 + 25j),
                Arc(275 + 25j, 150 + 150j, 0, 0, 0, 125 + 175j),
                Close(125 + 175j, 275 + 175j),
            ),
        )

        path1 = parse_path("M275,175 v-150 a150,150 0 0,0 -150,150 L 275,175 z")
        self.assertEqual(
            path1,
            Path(
                Move(275 + 175j),
                Line(275 + 175j, 275 + 25j),
                Arc(275 + 25j, 150 + 150j, 0, 0, 0, 125 + 175j),
                Line(125 + 175j, 275 + 175j),
                Close(275 + 175j, 275 + 175j),
            ),
        )

        path1 = parse_path(
            """M600,350 l 50,-25
                              a25,25 -30 0,1 50,-25 l 50,-25
                              a25,50 -30 0,1 50,-25 l 50,-25
                              a25,75 -30 0,1 50,-25 l 50,-25
                              a25,100 -30 0,1 50,-25 l 50,-25"""
        )
        self.assertEqual(
            path1,
            Path(
                Move(600 + 350j),
                Line(600 + 350j, 650 + 325j),
                Arc(650 + 325j, 25 + 25j, -30, 0, 1, 700 + 300j),
                Line(700 + 300j, 750 + 275j),
                Arc(750 + 275j, 25 + 50j, -30, 0, 1, 800 + 250j),
                Line(800 + 250j, 850 + 225j),
                Arc(850 + 225j, 25 + 75j, -30, 0, 1, 900 + 200j),
                Line(900 + 200j, 950 + 175j),
                Arc(950 + 175j, 25 + 100j, -30, 0, 1, 1000 + 150j),
                Line(1000 + 150j, 1050 + 125j),
            ),
        )

    def test_wc3_examples12(self):
        """
        W3C_SVG_11_TestSuite Paths

        Test using multiple coord sets to build a polybeizer, and implicit values for initial S.
        """
        path12 = parse_path(
            "M  100 100    C  100 20   200 20   200 100   S   300 180   300 100"
        )
        self.assertEqual(
            path12,
            Path(
                Move(to=(100 + 100j)),
                CubicBezier(
                    start=(100 + 100j),
                    control1=(100 + 20j),
                    control2=(200 + 20j),
                    end=(200 + 100j),
                ),
                CubicBezier(
                    start=(200 + 100j),
                    control1=(200 + 180j),
                    control2=(300 + 180j),
                    end=(300 + 100j),
                ),
            ),
        )

        path12 = parse_path("M  100 250    S  200 200   200 250     300 300   300 250")
        self.assertEqual(
            path12,
            Path(
                Move(to=(100 + 250j)),
                CubicBezier(
                    start=(100 + 250j),
                    control1=(100 + 250j),
                    control2=(200 + 200j),
                    end=(200 + 250j),
                ),
                CubicBezier(
                    start=(200 + 250j),
                    control1=(200 + 300j),
                    control2=(300 + 300j),
                    end=(300 + 250j),
                ),
            ),
        )

    def test_wc3_examples13(self):
        """
        W3C_SVG_11_TestSuite Paths

        Test multiple coordinates for V and H.
        """
        #
        path13 = parse_path(
            "   M  240.00000  56.00000    H  270.00000         300.00000 320.00000 400.00000   "
        )
        self.assertEqual(
            path13,
            Path(
                Move(to=(240 + 56j)),
                Line(start=(240 + 56j), end=(270 + 56j)),
                Line(start=(270 + 56j), end=(300 + 56j)),
                Line(start=(300 + 56j), end=(320 + 56j)),
                Line(start=(320 + 56j), end=(400 + 56j)),
            ),
        )

        path13 = parse_path(
            "   M  240.00000  156.00000    V  180.00000         200.00000 260.00000 300.00000   "
        )
        self.assertEqual(
            path13,
            Path(
                Move(to=(240 + 156j)),
                Line(start=(240 + 156j), end=(240 + 180j)),
                Line(start=(240 + 180j), end=(240 + 200j)),
                Line(start=(240 + 200j), end=(240 + 260j)),
                Line(start=(240 + 260j), end=(240 + 300j)),
            ),
        )

    def test_wc3_examples14(self):
        """
        W3C_SVG_11_TestSuite Paths

        Test implicit values for moveto. If the first command is 'm' it should be taken as an absolute moveto,
        plus implicit lineto.
        """
        path14 = parse_path(
            "   m   62.00000  56.00000    51.96152   90.00000   -103.92304         0.00000    51.96152  "
            "-90.00000   z    m    0.00000   15.00000   38.97114   67.50000   -77.91228         0.00000   "
            "38.97114  -67.50000   z  "
        )
        self.assertEqual(
            path14,
            Path(
                Move(to=(62 + 56j)),
                Line(start=(62 + 56j), end=(113.96152000000001 + 146j)),
                Line(
                    start=(113.96152000000001 + 146j), end=(10.038480000000007 + 146j)
                ),
                Line(start=(10.038480000000007 + 146j), end=(62.00000000000001 + 56j)),
                Close(start=(62.00000000000001 + 56j), end=(62 + 56j)),
                Move(to=(62 + 71j)),
                Line(start=(62 + 71j), end=(100.97113999999999 + 138.5j)),
                Line(
                    start=(100.97113999999999 + 138.5j),
                    end=(23.058859999999996 + 138.5j),
                ),
                Line(
                    start=(23.058859999999996 + 138.5j), end=(62.029999999999994 + 71j)
                ),
                Close(start=(62.029999999999994 + 71j), end=(62 + 71j)),
            ),
        )
        path14 = parse_path(
            "M  177.00000   56.00000    228.96152         146.00000   125.03848  146.00000    177.00000   "
            "56.00000   Z    M  177.00000  71.00000   215.97114         138.50000   138.02886  138.50000   "
            "177.00000  71.00000   Z  "
        )

        self.assertEqual(
            path14,
            Path(
                Move(to=(177 + 56j)),
                Line(start=(177 + 56j), end=(228.96152 + 146j)),
                Line(start=(228.96152 + 146j), end=(125.03848 + 146j)),
                Line(start=(125.03848 + 146j), end=(177 + 56j)),
                Close(start=(177 + 56j), end=(177 + 56j)),
                Move(to=(177 + 71j)),
                Line(start=(177 + 71j), end=(215.97114 + 138.5j)),
                Line(start=(215.97114 + 138.5j), end=(138.02886 + 138.5j)),
                Line(start=(138.02886 + 138.5j), end=(177 + 71j)),
                Close(start=(177 + 71j), end=(177 + 71j)),
            ),
        )

    def test_wc3_examples15(self):
        """
        W3C_SVG_11_TestSuite Paths

        'M' or 'm' command with more than one pair of coordinates are absolute
        if the moveto was specified with 'M' and relative if the moveto was
        specified with 'm'.
        """
        path15 = parse_path("M100,120 L160,220 L40,220 z")
        self.assertEqual(
            path15,
            Path(
                Move(to=(100 + 120j)),
                Line(start=(100 + 120j), end=(160 + 220j)),
                Line(start=(160 + 220j), end=(40 + 220j)),
                Close(start=(40 + 220j), end=(100 + 120j)),
            ),
        )
        path15 = parse_path("M350,120 L410,220 L290,220 z")
        self.assertEqual(
            path15,
            Path(
                Move(to=(350 + 120j)),
                Line(start=(350 + 120j), end=(410 + 220j)),
                Line(start=(410 + 220j), end=(290 + 220j)),
                Close(start=(290 + 220j), end=(350 + 120j)),
            ),
        )
        path15 = parse_path("M100,120 160,220 40,220 z")
        self.assertEqual(
            path15,
            Path(
                Move(to=(100 + 120j)),
                Line(start=(100 + 120j), end=(160 + 220j)),
                Line(start=(160 + 220j), end=(40 + 220j)),
                Close(start=(40 + 220j), end=(100 + 120j)),
            ),
        )
        path15 = parse_path("m350,120 60,100 -120,0 z")
        self.assertEqual(
            path15,
            Path(
                Move(to=(350 + 120j)),
                Line(start=(350 + 120j), end=(410 + 220j)),
                Line(start=(410 + 220j), end=(290 + 220j)),
                Close(start=(290 + 220j), end=(350 + 120j)),
            ),
        )

    def test_wc3_examples17(self):
        """
        W3C_SVG_11_TestSuite Paths

        Test that the 'z' and 'Z' command have the same effect.
        """
        path17a = parse_path("M 50 50 L 50 150 L 150 150 L 150 50 z")
        path17b = parse_path("M 50 50 L 50 150 L 150 150 L 150 50 Z")
        self.assertEqual(path17a, path17b)
        path17a = parse_path("M 250 50 L 250 150 L 350 150 L 350 50 Z")
        path17b = parse_path("M 250 50 L 250 150 L 350 150 L 350 50 z")
        self.assertEqual(path17a, path17b)

    def test_wc3_examples18(self):
        """
        W3C_SVG_11_TestSuite Paths

        The 'path' element's 'd' attribute ignores additional whitespace, newline characters, and commas,
        and BNF processing consumes as much content as possible, stopping as soon as a character that doesn't
        satisfy the production is encountered.
        """
        path18a = parse_path("M 20 40 H 40")
        path18b = parse_path(
            """M 20 40
                 H 40"""
        )
        self.assertEqual(path18a, path18b)
        path18a = parse_path("M 20 60 H 40")
        path18b = parse_path(
            """
                  M
                  20
                  60
                  H
                  40
                  """
        )
        self.assertEqual(path18a, path18b)
        path18a = parse_path("M 20 80 H40")
        path18b = parse_path("M       20,80          H    40")
        self.assertEqual(path18a, path18b)
        path18a = parse_path("M 20 100 H 40#90")
        path18b = parse_path("M 20 100 H 40")
        self.assertEqual(path18a, path18b)
        path18a = parse_path("M 20 120 H 40.5 0.6")
        path18b = parse_path("M 20 120 H 40.5.6")
        self.assertEqual(path18a, path18b)
        path18a = parse_path("M 20 140 h 10 -20")
        path18b = parse_path("M 20 140 h 10-20")
        self.assertEqual(path18a, path18b)
        path18a = parse_path("M 20 160 H 40")
        path18b = parse_path("M 20 160 H 40#90")
        self.assertEqual(path18a, path18b)

    def test_wc3_examples19(self):
        """
        W3C_SVG_11_TestSuite Paths

        Test that additional parameters to pathdata commands are treated as additional calls to the most recent command.
        """
        path19a = parse_path("M20 20 H40 H60")
        path19b = parse_path("M20 20 H40 60")
        self.assertEqual(path19a, path19b)
        path19a = parse_path("M20 40 h20 h20")
        path19b = parse_path("M20 40 h20 20")
        self.assertEqual(path19a, path19b)
        path19a = parse_path("M120 20 V40 V60")
        path19b = parse_path("M120 20 V40 60")
        self.assertEqual(path19a, path19b)
        path19a = parse_path("M140 20 v20 v20")
        path19b = parse_path("M140 20 v20 20")
        self.assertEqual(path19a, path19b)
        path19a = parse_path("M220 20 L 240 20 L260 20")
        path19b = parse_path("M220 20 L 240 20 260 20 ")
        self.assertEqual(path19a, path19b)
        path19a = parse_path("M220 40 l 20 0 l 20 0")
        path19b = parse_path("M220 40 l 20 0 20 0")
        self.assertEqual(path19a, path19b)
        path19a = parse_path("M50 150 C50 50 200 50 200 150 C200 50 350 50 350 150")
        path19b = parse_path("M50 150 C50 50 200 50 200 150 200 50 350 50 350 150")
        self.assertEqual(path19a, path19b)
        path19a = parse_path("M50, 200 c0,-100 150,-100 150,0 c0,-100 150,-100 150,0")
        path19b = parse_path("M50, 200 c0,-100 150,-100 150,0 0,-100 150,-100 150,0")
        self.assertEqual(path19a, path19b)
        path19a = parse_path("M50 250 S125 200 200 250 S275, 200 350 250")
        path19b = parse_path("M50 250 S125 200 200 250 275, 200 350 250")
        self.assertEqual(path19a, path19b)
        path19a = parse_path("M50 275 s75 -50 150 0 s75, -50 150 0")
        path19b = parse_path("M50 275 s75 -50 150 0 75, -50 150 0")
        self.assertEqual(path19a, path19b)
        path19a = parse_path("M50 300 Q 125 275 200 300 Q 275 325 350 300")
        path19b = parse_path("M50 300 Q 125 275 200 300 275 325 350 300")
        self.assertEqual(path19a, path19b)
        path19a = parse_path("M50 325 q 75 -25 150 0 q 75 25 150 0")
        path19b = parse_path("M50 325 q 75 -25 150 0 75 25 150 0")
        self.assertEqual(path19a, path19b)
        path19a = parse_path("M425 25 T 425 75 T 425 125")
        path19b = parse_path("M425 25 T 425 75 425 125")
        self.assertEqual(path19a, path19b)
        path19a = parse_path("M450 25 t 0 50 t 0 50")
        path19b = parse_path("M450 25 t 0 50 0 50")
        self.assertEqual(path19a, path19b)
        path19a = parse_path("M400,200 A25 25 0 0 0 425 150 A25 25 0 0 0 400 200")
        path19b = parse_path("M400,200 A25 25 0 0 0 425 150 25 25 0 0 0 400 200")
        self.assertEqual(path19a, path19b)
        path19a = parse_path("M400,300 a25 25 0 0 0 25 -50 a25 25 0 0 0 -25 50")
        path19b = parse_path("M400,300 a25 25 0 0 0 25 -50 25 25 0 0 0 -25 50")
        self.assertEqual(path19a, path19b)

    def test_wc3_examples20(self):
        """
        W3C_SVG_11_TestSuite Paths
        Tests parsing of the elliptical arc path syntax.
        """
        path20a = parse_path("M120,120 h25 a25,25 0 1,0 -25,25 z")
        path20b = parse_path("M120,120 h25 a25,25 0 10 -25,25z")
        self.assertEqual(path20a, path20b)
        path20a = parse_path("M200,120 h-25 a25,25 0 1,1 25,25 z")
        path20b = parse_path("M200,120 h-25 a25,25 0 1125,25 z")
        self.assertEqual(path20a, path20b)
        path20a = parse_path("M280,120 h25 a25,25 0 1,0 -25,25 z")
        self.assertRaises(Exception, 'parse_path("M280,120 h25 a25,25 0 6 0 -25,25 z")')
        path20a = parse_path("M360,120 h-25 a25,25 0 1,1 25,25 z")
        self.assertRaises(
            Exception, 'parse_path("M360,120 h-25 a25,25 0 1 -1 25,25 z")'
        )
        path20a = parse_path("M120,200 h25 a25,25 0 1,1 -25,-25 z")
        path20b = parse_path("M120,200 h25 a25,25 0 1 1-25,-25 z")
        self.assertEqual(path20a, path20b)
        path20a = parse_path("M200,200 h-25 a25,25 0 1,0 25,-25 z")
        self.assertRaises(Exception, 'parse_path("M200,200 h-25 a25,2501 025,-25 z")')
        path20a = parse_path("M280,200 h25 a25,25 0 1,1 -25,-25 z")
        self.assertRaises(
            Exception, 'parse_path("M280,200 h25 a25 25 0 1 7 -25 -25 z")'
        )
        path20a = parse_path("M360,200 h-25 a25,25 0 1,0 25,-25 z")
        self.assertRaises(
            Exception, 'parse_path("M360,200 h-25 a25,25 0 -1 0 25,-25 z")'
        )

    def test_others(self):
        # Other paths that need testing:

        # Relative moveto:
        path1 = parse_path("M 0 0 L 50 20 m 50 80 L 300 100 L 200 300 z")
        self.assertEqual(
            path1,
            Path(
                Move(0j),
                Line(0 + 0j, 50 + 20j),
                Move(100 + 100j),
                Line(100 + 100j, 300 + 100j),
                Line(300 + 100j, 200 + 300j),
                Close(200 + 300j, 100 + 100j),
            ),
        )

        # Initial smooth and relative CubicBezier
        path1 = parse_path("M100,200 s 150,-100 150,0")
        self.assertEqual(
            path1,
            Path(
                Move(100 + 200j),
                CubicBezier(100 + 200j, 100 + 200j, 250 + 100j, 250 + 200j),
            ),
        )

        # Initial smooth and relative QuadraticBezier
        path1 = parse_path("M100,200 t 150,0")
        self.assertEqual(
            path1,
            Path(Move(100 + 200j), QuadraticBezier(100 + 200j, 100 + 200j, 250 + 200j)),
        )

        # Relative QuadraticBezier
        path1 = parse_path("M100,200 q 0,0 150,0")
        self.assertEqual(
            path1,
            Path(Move(100 + 200j), QuadraticBezier(100 + 200j, 100 + 200j, 250 + 200j)),
        )

    def test_negative(self):
        """You don't need spaces before a minus-sign"""
        path1 = parse_path("M100,200c10-5,20-10,30-20")
        path2 = parse_path("M 100 200 c 10 -5 20 -10 30 -20")
        self.assertEqual(path1, path2)

    def test_numbers(self):
        """Exponents and other number format cases"""
        # It can be e or E, the plus is optional, and a minimum of +/-3.4e38 must be supported.
        path1 = parse_path("M-3.4e38 3.4E+38L-3.4E-38,3.4e-38")
        path2 = Path(
            Move(-3.4e38 + 3.4e38j), Line(-3.4e38 + 3.4e38j, -3.4e-38 + 3.4e-38j)
        )
        self.assertEqual(path1, path2)

    def test_errors(self):
        self.assertRaises(ValueError, parse_path, "M 100 100 L 200 200 Z 100 200")

    def test_non_path(self):
        # It's possible in SVG to create paths that has zero length,
        # we need to handle that.

        path = parse_path("M10.236,100.184")
        self.assertEqual(path.d(), "M 10.236,100.184")

    def test_issue_45(self):
        # A missing Z in certain cases
        path = parse_path(
            "m 1672.2372,-54.8161 "
            "a 14.5445,14.5445 0 0 0 -11.3152,23.6652 "
            "l 27.2573,27.2572 27.2572,-27.2572 "
            "a 14.5445,14.5445 0 0 0 -11.3012,-23.634 "
            "a 14.5445,14.5445 0 0 0 -11.414,5.4625 "
            "l -4.542,4.5420 "
            "l -4.5437,-4.5420 "
            "a 14.5445,14.5445 0 0 0 -11.3984,-5.4937 "
            "z"
        )

        self.assertEqual(
            "m 1672.24,-54.8161 "
            "a 14.5445,14.5445 0 0,0 -11.3152,23.6652 "
            "l 27.2573,27.2572 l 27.2572,-27.2572 "
            "a 14.5445,14.5445 0 0,0 -11.3012,-23.634 "
            "a 14.5445,14.5445 0 0,0 -11.414,5.4625 "
            "l -4.542,4.542 "
            "l -4.5437,-4.542 "
            "a 14.5445,14.5445 0 0,0 -11.3984,-5.4937 "
            "z",
            path.d(),
        )

    def test_arc_flag(self):
        """Issue #69"""
        path = parse_path(
            "M 5 1 v 7.344 A 3.574 3.574 0 003.5 8 3.515 3.515 0 000 11.5 C 0 13.421 1.579 15 3.5 15 "
            "A 3.517 3.517 0 007 11.531 v -7.53 h 6 v 4.343 A 3.574 3.574 0 0011.5 8 3.515 3.515 0 008 11.5 "
            "c 0 1.921 1.579 3.5 3.5 3.5 1.9 0 3.465 -1.546 3.5 -3.437 V 1 z"
        )
        # Check that all elemets is there:
        self.assertEqual(len(path), 15)
        # It ends on a vertical line to Y 1:
        self.assertEqual(path[-1].end.imag, 1)

    def test_incomplete_numbers(self):
        path = parse_path("M 0. .1")
        self.assertEqual(path.d(), "M 0,0.1")

        path = parse_path("M 0..1")
        self.assertEqual(path.d(), "M 0,0.1")
