# SVG Path specification parser

from . import path


def parse_path(pathdef, current_pos=0j):
    return path.Path(pathdef, current_pos=current_pos)
