from functions import *


class VariationButton:
    in_use = 0

    def __init__(self, size, x, y, increment=True):
        self.size = size
        self.x = x
        self.y = y
        self.increment = increment
        self.constants = divisors(cs.WIDTH)
        self.divisors = len(self.constants)

        self.color = cs.BLUE
        self.inner_color = cs.WHITE

        self.press = False

        self.background = pg.Rect(x, y, size, size)
        self.sign = [pg.Rect(x + cs.PAD, y + self.size // 2 - self.size // 8, self.size - 2 * cs.PAD,
                             self.size // 4)]
        if self.increment:
            self.sign.append(pg.Rect(x + self.size // 2 - self.size // 8, y + cs.PAD, self.size // 4,
                                     self.size - 2 * cs.PAD))

    def use(self, sort: sorts.Sort):
        if not self.increment:
            if self.in_use < self.divisors - 1:
                self.in_use += 1
                sort.size = cs.WIDTH // self.constants[self.in_use]
                sort.set_blocks()
        else:
            if self.in_use > 0:
                self.in_use -= 1
                sort.size = cs.WIDTH // self.constants[self.in_use]
                sort.set_blocks()
        return sort

    def set_colors(self, color, inner_color):
        self.color = color
        self.inner_color = inner_color

    def timeout_color(self, color, inner_color, timeout):
        prev = self.color, self.inner_color
        self.color, self.inner_color = color, inner_color
        self.press = True
        time.sleep(timeout)
        self.color, self.inner_color = prev
        self.press = False

    def get_coordinates(self):
        return self.x, self.y

    def get_size(self):
        return self.size

    def draw(self, window):
        pg.draw.rect(window, self.color, self.background)
        for rect in self.sign:
            pg.draw.rect(window, self.inner_color, rect)


class Theme:
    def __init__(self, theme, x, y, width, height):
        self.theme = theme
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.selected = False
        self.hovering = False

        self.bound = pg.Rect(self.x, self.y, self.width, self.height)
        self.theme_rects = [pg.Rect(self.x + self.width // 3 * i, self.y, self.width // 3, self.height)
                            for i in range(3)]

    def set(self, sort: sorts.Sort):
        sort.theme = self.theme
        return sort

    def get_position(self):
        return self.x, self.y

    def get_size(self):
        return self.width, self.height

    def draw(self, window, width=4):
        for color, rect in zip(self.theme, self.theme_rects):
            pg.draw.rect(window, color, rect)
        if self.selected: color = cs.PURPLE
        elif self.hovering: color = cs.YELLOW
        else: color = cs.CYAN
        for i in range(3):
            pg.draw.line(window, color, (self.x + i * self.width // 3, self.y),
                         (self.x + i * self.width // 3, self.y + self.height), width=width)
        pg.draw.line(window, color, (self.x + self.width - 2 * width, self.y),
                     (self.x + self.width - 2 * width, self.y + self.height), width=width)
        pg.draw.line(window, color, (self.x, self.y), (self.x + self.width, self.y), width=width)
        pg.draw.line(window, color, (self.x, self.y + self.height - width // 2),
                     (self.x + self.width, self.y + self.height - width // 2), width=width)