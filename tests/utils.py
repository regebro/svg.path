from svg.path.path import _xform


class DebugTurtle:

    def __init__(self, steps=100):
        self.steps = steps

    def __enter__(self):
        import turtle

        self.t = turtle.Turtle()
        self.t.pencolor("gray")
        self.t.penup()
        self.t.goto(0, -100)
        self.t.write("-100")
        self.t.pendown()
        self.t.goto(0, 100)
        self.t.write("100")
        self.t.penup()
        self.t.goto(-100, 0)
        self.t.write("-100")
        self.t.pendown()
        self.t.goto(100, 0)
        self.t.write("100")
        self.t.penup()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return

    def draw_path(self, path, color="black", matrix=None):
        self.t.pencolor(color)
        p = path.point(0)
        if matrix is not None:
            p = _xform(p, matrix)
        self.t.goto(p.real, p.imag)
        self.t.dot(3)
        self.t.pendown()
        s = 1 / self.steps
        for x in range(self.steps):
            p = path.point((x + 1) * s)
            if matrix is not None:
                p = _xform(p, matrix)
            self.t.goto(p.real, p.imag)
        self.t.penup()
        self.t.dot(3)
