from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000

class Color:
    """A slightly more complicated color class"""

    # class variables shared by all instances
    color_count = 0

    def __init__(self, name, red, green, blue):
        self.name = name
        self.red = red
        self.green = green
        self.blue = blue

        # increment class variable
        Color.color_count += 1

    def rgb_to_lab(self):
        color_srgb = sRGBColor(self.red, self.green, self.blue, True)
        return convert_color(color_srgb, LabColor)

    def de2000_compare(self, color2):
        color1_lab = self.rgb_to_lab()
        color2_lab = color2.rgb_to_lab()
        return delta_e_cie2000(color1_lab, color2_lab)

    def __str__(self):
        return f"Hi, I'm {self.name}."

    def __eq__(self, color2):
        return self.red == color2.red and self.green == color2.green and self.blue == color2.blue

a = Color('red', 255, 0, 0)
print(a)

a1 = Color('red1', 255, 0, 0)

print(a == a1)

d = Color('marsala', 173, 101, 95)
print(f'The difference between {a.name} and {d.name} is {a.de2000_compare(d)}')

b = Color('blue', 0, 0, 255)
c = Color('red', 255, 0, 0)
d = Color('marsala', 173, 101, 95)

white = Color('white', 255, 255, 255)
black = Color('black', 0, 0, 0)

print(f'The difference between {a.name} and {b.name} is {a.de2000_compare(b)}')

print(f'The difference between {a.name} and {d.name} is {a.de2000_compare(d)}')

print(f'The difference between {white.name} and {black.name} is {white.de2000_compare(black)}')