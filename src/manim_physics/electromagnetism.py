__all__ = [
    "Charge",
    "ElectricField",
]

from manim import *


class Charge(VGroup):
    def __init__(self, magnitude=1, point=ORIGIN, add_light = False, **kwargs):
        VGroup.__init__(self, **kwargs)
        self.magnitude = magnitude
        radius = abs(magnitude) * 0.5 if abs(magnitude) < 2 else 1
        
        if magnitude > 0:
            label = VGroup(Rectangle(width=0.32 * 1.1, height=0.006 * 1.1), Rectangle(width=0.006 * 1.1, height=0.32 * 1.1))
            color = RED
            layer_colors = [RED_D, RED_A]
            layer_radius = 4
        else:
            label = Rectangle(width=0.27, height=0.003)
            color = BLUE
            layer_colors = ["#3399FF", "#66B2FF"]
            layer_radius = 2

        if add_light:
            layer_num = 80
            color_list = color_gradient(layer_colors, layer_num)
            opacity_func = lambda t: 1500 * (1 - abs(t-0.009) ** 0.0001)
            rate_func = lambda t: t ** 2

            for i in range(layer_num):
                self.add(
                    Arc(
                        radius= layer_radius * rate_func((0.5 + i)/layer_num), 
                        angle=TAU, 
                        color=color_list[i],
                        stroke_width=101 * (rate_func((i + 1)/layer_num) - rate_func(i/layer_num)) * layer_radius,
                        stroke_opacity=opacity_func(rate_func(i/layer_num))
                    ).shift(point)
                )

        self.add(Dot(point=point, radius=radius * 0.3, color = color))
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
                direction += (mag * np.array([x / dist, y / dist, z / dist]))
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
