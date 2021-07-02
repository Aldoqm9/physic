__all__ = [
    "Charge",
    "ElectricField",
    "Current",
    "CurrentMagneticField",
    "BarMagnet",
    "BarMagneticField",
]

from typing import Sequence
from manim import *


class Charge(Dot, VGroup):
    def __init__(self, magnitude=1, point=ORIGIN, **kwargs):
        self.magnitude = magnitude
        radius = abs(magnitude) * 0.5 if abs(magnitude) < 2 else 1
        super().__init__(point=point, radius=radius * 0.3)
        if magnitude > 0:
            label = MathTex("+")
            color = RED
        else:
            label = MathTex("-")
            color = BLUE
        self.set_color(color)
        self.add(label.scale(radius).shift(point))


class ElectricField(ArrowVectorField):
    def __init__(self, *charges: Charge, **kwargs):
        super().__init__(lambda p: self.field_func(p, *charges), **kwargs)

    def field_func(self, p, *charges):
        direction = np.zeros(3)
        for charge in charges:
            p0, mag = charge.get_center(), charge.magnitude
            x, y, z = p - p0
            dist = (x ** 2 + y ** 2 + z ** 2) ** 1.5
            if (x ** 2) > 0.05 or (y ** 2) > 0.05:
                direction += mag * np.array([x / dist, y / dist, z / dist])
            else:
                direction += np.zeros(3)
        return direction

    def get_force_on_charge(self, charge):
        p0 = charge.get_center()
        return (
            Vector((self.get_vector(p0).get_end() - p0) * charge.magnitude)
            .shift(p0)
            .set_color(self.get_vector(p0).color)
        )


class Current(VGroup):
    def __init__(
        self, point: Sequence[float] = ORIGIN, magnitude=1, direction=OUT, **kwargs
    ):
        if np.all(direction == OUT) or np.all(direction == IN):
            self.direction = direction
        else:
            raise ValueError("only IN and OUT are supported.")
        self.magnitude = magnitude
        if np.all(direction == IN):
            label = VGroup(
                Line(ORIGIN, UR).move_to(ORIGIN),
                Line(ORIGIN, UL).move_to(ORIGIN),
            )
            self.magnitude *= -1
        else:
            label = Dot(radius=0.2)
        super().__init__(**kwargs)
        self.add(Circle(color=WHITE), label).scale(0.2).shift(point)


class CurrentMagneticField(ArrowVectorField):
    def __init__(self, *currents: Current, **kwargs):
        super().__init__(lambda p: self.field_func(p, *currents), **kwargs)

    def field_func(self, p, *currents):
        direction = np.zeros(3)
        for current in currents:
            x, y, z = p
            x0, y0, z0 = point = current.get_center()
            mag = current.magnitude
            if (x - x0) ** 2 > 0.05 or (y - y0) ** 2 > 0.05:
                dist = np.linalg.norm(p - point)
                direction += mag * np.array([-(y - y0), (x - x0), 0]) / dist ** 3
            else:
                direction += np.zeros(3)
        return direction


class BarMagnet(VGroup):
    def __init__(
        self,
        north: Sequence[float] = UP,
        south: Sequence[float] = DOWN,
        height: float = 2,
        width: float = 0.5,
        **kwargs
    ):
        self.length = np.linalg.norm(north - south)
        # self.width = width
        super().__init__(**kwargs)
        if width > height:
            raise ValueError("Bar magnet must be taller than it's width")
        self.bar = VGroup(
            Rectangle(
                height=height / 2, width=width, fill_opacity=1, color=RED
            ).next_to(ORIGIN, UP, 0),
            Rectangle(
                height=height / 2, width=width, fill_opacity=1, color=BLUE
            ).next_to(ORIGIN, DOWN, 0),
        )
        self.north_label = Tex("N").shift(UP * (self.length / 2 - 0.5))
        self.south_label = Tex("S").shift(UP * -(self.length / 2 - 0.5))
        self.add(self.bar, self.north_label, self.south_label)
        self.rotate(-PI / 2 + angle_of_vector(self.get_south_to_north()))

    def get_south_to_north(self):
        return Vector(
            self.north_label.get_center() - self.south_label.get_center()
        ).get_vector()


class BarMagneticField(CurrentMagneticField):
    def __init__(self, *bars: BarMagnet, **kwargs):
        currents = []
        for bar in bars:
            currents_ = []
            currents_ += [
                Current(magnitude=-1).move_to(i)
                for i in np.linspace(
                    [bar.width / 2, bar.length / 2, 0],
                    [bar.width / 2, -bar.length / 2, 0],
                    10,
                )
            ]
            currents_ += [
                Current(magnitude=1).move_to(i)
                for i in np.linspace(
                    [-bar.width / 2, bar.length / 2, 0],
                    [-bar.width / 2, -bar.length / 2, 0],
                    10,
                )
            ]
            VGroup(*currents_).rotate(
                -PI / 2 + angle_of_vector(bar.get_south_to_north())
            ).shift(bar.get_center())
            currents += currents_

        super().__init__(*currents, **kwargs)
