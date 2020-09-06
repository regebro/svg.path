from svg.path.path import Arc, CubicBezier

from math import tau, atan2, ceil, cos, sin, sqrt, tan, radians


class Arc_with_to_Bezier (Arc):
    """ extract form svgelements
        To do matrix transitions, the native parameterization is start, end, center, prx, pry, sweep

        'start, end, center, prx, pry' are points and sweep amount is a t value in tau radians.
        If points are modified by an affine transformation, the arc is transformed.
        There is a special case for when the scale factor inverts, it inverts the sweep.

        Note: t-values are not angles from center in elliptical arcs. These are the same thing in
        circular arcs. But, here t is a parameterization around the ellipse, as if it were a circle.
        The position on the arc is (a * cos(t), b * sin(t)). If r-major was 0 for example. The
        positions would all fall on the x-axis. And the angle from center would all be either 0 or
        tau/2. However, since t is the parameterization we can conceptualize it as a position on a
        circle which is then scaled and rotated by a matrix.

        prx is the point at t 0 in the ellipse.
        pry is the point at t tau/4 in the ellipse.
        prx -> center -> pry should form a right triangle.

        The rotation can be defined as the angle from center to prx. Since prx is located at
        t(0) its deviation can only be the result of a rotation.

        Sweep is a value in t.
        The sweep angle can be a value greater than tau and less than -tau.
        However if this is the case, conversion back to Path.d() is expected to fail.
        We can denote these arc events but not as a single command.

        start_t + sweep = end_t

        comparaison between svgelements and regebro's Arc attributes :
        self.rx, self.ry are regebro's self.radius real and imag
        ?get_rotation() returns regebro's self.rotation which needs to be converted in radians or is it a different angle?
        self.sweep is aa boolean in regebro's and something different in svgelements

        """

    def as_cubic_curves(self):
        sweep_limit = tau / 12
        end_t = self.get_end_t()
        start_t = self.get_start_t()
        sweep = end_t - start_t
        arc_required = int(ceil(abs(sweep) / sweep_limit))
        if arc_required == 0:
            return
        slice = sweep / float(arc_required)

        theta = self.theta
        rx = self.radius.real
        ry = self.radius.imag
        p_start = self.start
        current_t = start_t
        x0 = self.center.real
        y0 = self.center.imag
        cos_theta = cos(theta)
        sin_theta = sin(theta)
        arc_end = (self.end.real, self.end.imag)
        p_start = (self.start.real, self.start.imag)

        for i in range(0, arc_required):
            next_t = current_t + slice

            alpha = sin(slice) * (sqrt(4 + 3 * pow(tan((slice) / 2.0), 2)) - 1) / 3.0

            cos_start_t = cos(current_t)
            sin_start_t = sin(current_t)

            ePrimen1x = -rx * cos_theta * sin_start_t - ry * sin_theta * cos_start_t
            ePrimen1y = -rx * sin_theta * sin_start_t + ry * cos_theta * cos_start_t

            cos_end_t = cos(next_t)
            sin_end_t = sin(next_t)

            p2En2x = x0 + rx * cos_end_t * cos_theta - ry * sin_end_t * sin_theta
            p2En2y = y0 + rx * cos_end_t * sin_theta + ry * sin_end_t * cos_theta
            p_end = (p2En2x, p2En2y)
            if i == arc_required - 1:
                p_end = arc_end

            ePrimen2x = -rx * cos_theta * sin_end_t - ry * sin_theta * cos_end_t
            ePrimen2y = -rx * sin_theta * sin_end_t + ry * cos_theta * cos_end_t

            p_c1 = (p_start[0] + alpha * ePrimen1x, p_start[1] + alpha * ePrimen1y)
            p_c2 = (p_end[0] - alpha * ePrimen2x, p_end[1] - alpha * ePrimen2y)
            control1 = p_c1[0] + p_c1[1] * 1j
            control2 = p_c2[0] + p_c2[1] * 1j

            yield Cubic_with_draw(p_start[0] + p_start[1] * 1j, control1, control2, p_end[0] + p_end[1] * 1j)
            p_start = p_end
            current_t = next_t

    def get_start_t(self):
        angle = radians(self.rotation)
        t = atan2(self.radius.real * tan(angle), self.radius.imag)
        tau_1_4 = tau / 4.0
        tau_3_4 = 3 * tau_1_4
        if tau_3_4 >= abs(angle) % tau > tau_1_4:
            t += tau / 2
        return t

    def get_end_t(self):
        angle = radians(self.rotation + self.delta)
        t = atan2(self.radius.real * tan(angle), self.radius.imag)
        return t

    def draw(self, turtle):
        t.penup()
        t.pencolor('black')
        t.goto(self.start.real, self.start.imag)
        t.dot(3, 'black')
        t.pendown()
        for x in range(1, 101):
            p = self.point(x * 0.01)
            t.goto(p.real, p.imag)
        t.dot(3, 'black')
        t.penup()
        t.goto(0, 0)


class Cubic_with_draw (CubicBezier):

    def draw(self, turtle, coords):
        t.penup()
        t.goto(self.start.real + coords.real, self.start.imag + coords.imag)
        t.pencolor('red')
        t.dot(3, 'red')
        t.pendown()
        for x in range(1, 101):
            p = self.point(x * 0.01)
            t.goto(p.real + coords.real, p.imag + coords.imag)
        t.dot(3, 'red')
        t.penup()


if __name__ == '__main__':

    import turtle
    t = turtle.Turtle()
    coords = 0 + 0 * 1j
    start = 300 + 100 * 1j
    end = 300 + 300 * 1j
    radius = 100 + 50 * 1j
    arc = Arc_with_to_Bezier(start, radius, 0, False, False, end)
    arc.draw(t)
    curves = list((curve for curve in arc.as_cubic_curves()))
    for curve in curves:
        curve.draw(t, coords)
    _ = input('tupe enter to go to the next test')
    t.clear()
    t.reset()

    arc = Arc_with_to_Bezier(start, radius, 40, 0, 0, end)
    arc.draw(t)
    curves = list((curve for curve in arc.as_cubic_curves()))
    for curve in curves:
        curve.draw(t, coords)



