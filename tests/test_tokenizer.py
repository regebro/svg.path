from typing import Union, List, Tuple
import pytest
from svg.path import parser

PATHS = [
    (
        "M 100 100 L 300 100 L 200 300 z",
        [("M", "100 100"), ("L", "300 100"), ("L", "200 300"), ("z", "")],
        [("M", 100 + 100j), ("L", 300 + 100j), ("L", 200 + 300j), ("z",)],
    ),
    (
        "M 5 1 v 7.344 A 3.574 3.574 0 003.5 8 3.515 3.515 0 000 11.5 C 0 13.421 1.579 15 3.5 15 "
        "A 3.517 3.517 0 007 11.531 v -7.53 h 6 v 4.343 A 3.574 3.574 0 0011.5 8 3.515 3.515 0 008 11.5 "
        "c 0 1.921 1.579 3.5 3.5 3.5 1.9 0 3.465 -1.546 3.5 -3.437 V 1 z",
        [
            ("M", "5 1"),
            ("v", "7.344"),
            ("A", "3.574 3.574 0 003.5 8 3.515 3.515 0 000 11.5"),
            ("C", "0 13.421 1.579 15 3.5 15"),
            ("A", "3.517 3.517 0 007 11.531"),
            ("v", "-7.53"),
            ("h", "6"),
            ("v", "4.343"),
            ("A", "3.574 3.574 0 0011.5 8 3.515 3.515 0 008 11.5"),
            ("c", "0 1.921 1.579 3.5 3.5 3.5 1.9 0 3.465 -1.546 3.5 -3.437"),
            ("V", "1"),
            ("z", ""),
        ],
        [
            ("M", 5 + 1j),
            ("v", 7.344),
            ("A", 3.574, 3.574, 0, False, False, 3.5 + 8j),
            ("A", 3.515, 3.515, 0, False, False, 0 + 11.5j),
            ("C", 0 + 13.421j, 1.579 + 15j, 3.5 + 15j),
            ("A", 3.517, 3.517, 0, False, False, 7 + 11.531j),
            ("v", -7.53),
            ("h", 6),
            ("v", 4.343),
            ("A", 3.574, 3.574, 0, False, False, 11.5 + 8j),
            ("A", 3.515, 3.515, 0, False, False, 8 + 11.5j),
            ("c", 0 + 1.921j, 1.579 + 3.5j, 3.5 + 3.5j),
            ("c", 1.9 + 0j, 3.465 - 1.546j, 3.5 - 3.437j),
            ("V", 1),
            ("z",),
        ],
    ),
    (
        "M 600,350 L 650,325 A 25,25 -30 0,1 700,300 L 750,275",
        [
            ("M", "600,350"),
            ("L", "650,325"),
            ("A", "25,25 -30 0,1 700,300"),
            ("L", "750,275"),
        ],
        [
            ("M", 600 + 350j),
            ("L", 650 + 325j),
            ("A", 25, 25, -30, False, True, 700 + 300j),
            ("L", 750 + 275j),
        ],
    ),
]


@pytest.mark.parametrize("path, commands, tokens", PATHS)
def test_commandifier(
    path: str,
    commands: List[Tuple[str, ...]],
    tokens: List[Tuple[Union[str, complex, float, bool, None], ...]],
) -> None:
    assert list(parser._commandify_path(path)) == commands
    assert list(parser._tokenize_path(path)) == tokens


@pytest.mark.parametrize("path, commands, tokens", PATHS)
def test_parser(
    path: str,
    commands: List[Tuple[str, ...]],
    tokens: List[Tuple[Union[str, complex, float, bool, None], ...]],
) -> None:
    # TODO: Add a check that svg_path.d() is correct.
    # flake8: F841 local variable 'svg_path' is assigned to but never used
    svg_path = parser.parse_path(path)  # noqa: F841
