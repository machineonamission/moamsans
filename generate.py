import cairo

from dataclasses import dataclass
import math


@dataclass
class Point:
    x: int
    y: int
    rounded: bool = False


@dataclass
class Line:
    points: list[Point]


@dataclass
class Letter:
    lines: list[Line]


# todo distinguish derived and forced grid
@dataclass
class Grid:
    xmin: int
    xmax: int
    ymin: int
    ymax: int
    em_height: int
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
            return self.em_height / self.height + self.factory_stroke

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

    def pixel_pos(self, x: int, y: int) -> tuple[float, float]:
        return (
            x * self.xstep + self.stroke_width // 2,
            y * self.ystep + self.stroke_width // 2,
        )

    def point_pos(self, point: Point) -> tuple[float, float]:
        return self.pixel_pos(point.x, point.y)


letters = {
    "h": Letter([
        Line([
            Point(0, 3),
            Point(0, -1)
        ]),
        Line([
            Point(0, 1),
            Point(1, 1, True),
            Point(1, 0)
        ])
    ]),
}

grid = Grid(
    xmin=0,
    xmax=2,
    ymin=-1,
    ymax=3,
    em_height=1000,
    x_ratio=0.8,
    stroke_ratio=1/2,
)

print(grid.ascent, grid.descent)

def normal(p: tuple[int, int]) -> tuple[float, float]:
    x, y = p
    length = (x ** 2 + y ** 2) ** 0.5
    if length == 0:
        return 0.0, 0.0
    return x / length, y / length


for letter_key, letter in letters.items():
    letter: Letter
    # grid.xmin * grid.xstep, grid.ymin * grid.ystep, grid.x_ratio * grid.em_height, grid.em_height
    with cairo.SVGSurface(f"svgs/{letter_key}.svg", grid.width * grid.xstep + grid.stroke_width, grid.height * grid.ystep + grid.stroke_width) as surface:
        context = cairo.Context(surface)
        context.translate(0, grid.ystep * grid.ymax + grid.stroke_width)
        context.scale(1, -1)
        context.set_line_width(grid.stroke_width)
        context.set_line_cap(cairo.LINE_CAP_SQUARE)
        for line in letter.lines:
            init = line.points[0]
            context.move_to(
                *grid.point_pos(init)
            )
            for i in range(1, len(line.points)):
                point = line.points[i]
                prev_point = line.points[i - 1]
                next_point = line.points[i + 1] if i + 1 < len(line.points) else None

                x, y = grid.point_pos(point)

                prev_x, prev_y = grid.point_pos(prev_point)
                next_x, next_y = grid.point_pos(next_point) if next_point else (None, None)
                if point.rounded:
                    prev_diff = (x - prev_x, y - prev_y)
                    next_diff = (x - next_x, y - next_y)
                    prev_normal = normal(prev_diff)
                    next_normal = normal(next_diff)
                    offset_x = x - prev_normal[0] * (grid.stroke_width / 2) - next_normal[0] * (
                            grid.stroke_width / 2)
                    offset_y = y - prev_normal[1] * (grid.stroke_width / 2) - next_normal[1] * (
                            grid.stroke_width / 2)

                    a1 = math.atan2(prev_diff[1], prev_diff[0])
                    # a1 = min(math.tau - a1, a1)
                    a2 = math.atan2(next_diff[1], next_diff[0])
                    # a2 = min(math.tau - a2, a2)

                    if a1 < a2:
                        context.arc_negative(offset_x, offset_y, grid.stroke_width / 2, a2, a1)
                    else:
                        context.arc(offset_x, offset_y, grid.stroke_width / 2, a2, a1)
                else:
                    context.line_to(x, y)
            context.stroke()
