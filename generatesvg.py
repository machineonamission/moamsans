# DEPRECATED, USE GENERATEFONTFORGE

import cairo

import math

from structs import *

lower_letters = {
    "v": Letter([
        Line([
            Point(0, 2),
            Point(1, 0),
            Point(2, 2),
        ]),
    ]),
}

upper_letters = {
}

lower_grid = Grid(
    xmin=0,
    xmax=2,
    ymin=-1,
    ymax=3,
    em_height=1000,
    x_ratio=0.8,
    stroke_ratio=1 / 2,
)

upper_grid = Grid(
    xmin=0,
    xmax=2,
    ymin=0,
    ymax=2,
    em_height=lower_grid.ascent,
    x_ratio=0.8,
    factory_stroke=lower_grid.stroke_width,
)

master_list = [
    (lower_grid, lower_letters),
    (upper_grid, upper_letters),
]

print(lower_grid.ascent, lower_grid.descent)

for grid, letters in master_list:
    grid: Grid
    for letter_key, letter in letters.items():
        letter: Letter
        # grid.xmin * grid.xstep, grid.ymin * grid.ystep, grid.x_ratio * grid.em_height, grid.em_height
        with cairo.SVGSurface(f"svgs/{letter_key}.svg", grid.width * grid.xstep + grid.stroke_width,
                              grid.height * grid.ystep + grid.stroke_width) as surface:
            context = cairo.Context(surface)
            context.translate(0, grid.ystep * grid.ymax + grid.stroke_width)
            context.scale(1, -1)
            context.set_line_width(grid.stroke_width)
            context.set_line_cap(cairo.LINE_CAP_SQUARE)
            for line in letter.lines:
                context.save()  # restore point for clip shit

                minx = min(grid.point_pos(p)[0] for p in line.points)
                maxx = max(grid.point_pos(p)[0] for p in line.points)
                miny = min(grid.point_pos(p)[1] for p in line.points)
                maxy = max(grid.point_pos(p)[1] for p in line.points)
                width = maxx - minx
                height = maxy - miny

                context.rectangle(minx - grid.hsw,
                                  miny - grid.hsw,
                                  width + grid.stroke_width,
                                  height + grid.stroke_width)
                context.clip()

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
                        offset_x = x - prev_normal[0] * grid.hsw - next_normal[0] * (
                            grid.hsw)
                        offset_y = y - prev_normal[1] * grid.hsw - next_normal[1] * (
                            grid.hsw)

                        a1 = math.atan2(prev_diff[1], prev_diff[0])
                        # a1 = min(math.tau - a1, a1)
                        a2 = math.atan2(next_diff[1], next_diff[0])
                        # a2 = min(math.tau - a2, a2)

                        if a1 < a2:
                            context.arc_negative(offset_x, offset_y, grid.hsw, a2, a1)
                        else:
                            context.arc(offset_x, offset_y, grid.hsw, a2, a1)
                    else:
                        context.line_to(x, y)
                context.stroke()
                # essentially leave the clipping mask?
                context.restore()
