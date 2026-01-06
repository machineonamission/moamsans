from dataclasses import dataclass


@dataclass
class Point:
    x: int
    y: int
    rounded: bool = False


@dataclass
class PixelPoint:
    x: float
    y: float

    def __mul__(self, other: float) -> "PixelPoint":
        return PixelPoint(self.x * other, self.y * other)

    def __truediv__(self, other):
        return PixelPoint(self.x / other, self.y / other)

    def __add__(self, other: "PixelPoint | float") -> "PixelPoint":
        if isinstance(other, float):
            return PixelPoint(self.x + other, self.y + other)
        else:
            return PixelPoint(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "PixelPoint | float") -> "PixelPoint":
        return self + -other

    def __neg__(self) -> "PixelPoint":
        return self * -1

    def __imul__(self, other: float) -> "PixelPoint":
        self.x *= other
        self.y *= other
        return self

    def __itruediv__(self, other: float) -> "PixelPoint":
        self.x /= other
        self.y /= other
        return self

    def __iadd__(self, other: "PixelPoint | float") -> "PixelPoint":
        if isinstance(other, float):
            self.x += other
            self.y += other
        else:
            self.x += other.x
            self.y += other.y
        return self

    def __isub__(self, other: "PixelPoint | float") -> "PixelPoint":
        if isinstance(other, float):
            self.x -= other
            self.y -= other
        else:
            self.x -= other.x
            self.y -= other.y
        return self

    @property
    def length(self) -> float:
        return(self.x ** 2 + self.y ** 2) ** 0.5

    def normalize(self) -> "PixelPoint":
        length = self.length
        if length == 0:
            return PixelPoint(0.0, 0.0)
        return self / length

    def as_tuple(self) -> tuple[float, float]:
        return self.x, self.y

    @staticmethod
    def from_point(point: Point) -> "PixelPoint":
        return PixelPoint(point.x, point.y)


@dataclass
class Line:
    points: list[Point]


@dataclass
class Letter:
    lines: list[Line]


@dataclass
class Grid:
    xmin: int
    xmax: int
    ymin: int
    ymax: int
    em_height: float
    x_ratio: float
    stroke_ratio: float = None
    factory_stroke: float = None

    # xstep: int
    # ystep: int
    # stroke_width: int

    @property
    def ystep(self) -> float:
        """
        1. xstep = ystep * x_ratio
        2. stroke_width = min(xstep, ystep) * stroke_ratio
        3. ystep * height + stroke_width = em_height
        :return:
        """
        if self.stroke_ratio:
            return self.em_height / (self.height + min(self.x_ratio, 1) * self.stroke_ratio)
        else:
            return (self.em_height - self.factory_stroke) / self.height

    @property
    def xstep(self) -> float:
        return self.ystep * self.x_ratio

    @property
    def width(self) -> int:
        return self.xmax - self.xmin

    @property
    def height(self) -> int:
        return self.ymax - self.ymin

    @property
    def stroke_width(self) -> float:
        if self.stroke_ratio:
            return min(self.xstep, self.ystep) * self.stroke_ratio
        else:
            return self.factory_stroke

    @property
    def hsw(self) -> float:
        return self.stroke_width / 2

    @property
    def ascent(self) -> float:
        return self.ymax * self.ystep + self.stroke_width

    @property
    def descent(self) -> float:
        return -self.ymin * self.ystep

    # @property
    # def pixel_width(self) -> int:
    #     return self.width * self.xstep + self.stroke_width
    #
    # @property
    # def pixel_height(self) -> int:
    #     return self.height * self.ystep + self.stroke_width

    def pixel_pos(self, x: int, y: int) -> PixelPoint:
        return PixelPoint(x * self.xstep, y * self.ystep) + (self.stroke_width / 2)

    def point_pos(self, point: Point) -> PixelPoint:
        return self.pixel_pos(point.x, point.y)


def normal(p: tuple[float, float]) -> tuple[float, float]:
    x, y = p
    length = (x ** 2 + y ** 2) ** 0.5
    if length == 0:
        return 0.0, 0.0
    return x / length, y / length
