import unittest

from svg import path
from svg.transform import make_matrix


class TransformTests(unittest.TestCase):
    def test_svg_path_transform(self):
        line = path.Line(0, 100 + 100j)
        xline = line.transform(make_matrix(sx=0.1, sy=0.2))
        assert xline == path.Line(0, 10 + 20j)

        d = path.parser.parse_path("M 750,100 L 250,900 L 1250,900 z")
        # Makes it 10% as big in x and 20% as big in y
        td = d.transform(make_matrix(sx=0.1, sy=0.2))
        assert td.d() == "M 75,20 L 25,180 L 125,180 z"
