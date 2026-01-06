import fontforge
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
    "u": Letter([
        Line([
            Point(0, 2),
            Point(0, 0, True),
            Point(2, 0, True),
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
print(lower_grid.stroke_width)

fontforge.runInitScripts()
font = fontforge.font()
font.layers.add("rounded", False)

circle_constant = (4 / 3) * (math.sqrt(2) - 1)  # for bezier circle approximation

for grid, letters in master_list:
    grid: Grid
    for letter_key, letter in letters.items():
        letter: Letter
        font_letter: fontforge.glyph = font.createMappedChar(letter_key)
        for line_no, line in enumerate(letter.lines):
            line: Line
            contour = fontforge.contour()
            contour.moveTo(*grid.point_pos(line.points[0]).as_tuple())
            for i in range(1, len(line.points)):
                point = line.points[i]

                pixel = grid.point_pos(point)

                if point.rounded:
                    # we need the prev and next points to do a proper arc
                    prev_point = line.points[i - 1]
                    next_point = line.points[i + 1] if i + 1 < len(line.points) else None

                    prev_pixel = grid.point_pos(prev_point)
                    next_pixel = grid.point_pos(next_point) if next_point else (None, None)

                    # get the direction from the rounded point to the prev and next points
                    # this should probably only ever be up down left or right but eh
                    prev_diff = pixel - prev_pixel
                    next_diff = pixel - next_pixel
                    prev_normal = prev_diff.normalize()
                    next_normal = next_diff.normalize()

                    # edges of the arc itself
                    curve_start = pixel - (prev_normal * grid.hsw)
                    curve_end = pixel - (next_normal * grid.hsw)

                    # more spaced from the curve, so the calligraphic stroke can end before the curve starts
                    pre_curve = pixel - (prev_normal * grid.stroke_width)
                    post_curve = pixel - (next_normal * grid.stroke_width)

                    # control points for bezier curve
                    circle_offset = grid.hsw * (1 - circle_constant)
                    control_1 = pixel - prev_normal * circle_offset
                    control_2 = pixel - next_normal * circle_offset

                    # create space in our normal contour for the curve (by making a new contour lol)
                    contour.lineTo(*pre_curve.as_tuple())
                    font_letter.foreground += contour
                    contour = fontforge.contour()
                    contour.moveTo(*post_curve.as_tuple())

                    # curve, different layer so it will be stroked differently
                    curvetour = fontforge.contour()
                    curvetour.moveTo(*pre_curve.as_tuple())
                    curvetour.lineTo(*curve_start.as_tuple())
                    curvetour.cubicTo(control_1.as_tuple(), control_2.as_tuple(), curve_end.as_tuple())
                    curvetour.lineTo(*post_curve.as_tuple())
                    font_letter.layers["rounded"] += curvetour
                else:
                    contour.lineTo(*pixel.as_tuple())
            font_letter.foreground += contour

        # stroke layers appropriately
        font_letter.activeLayer = "Fore"
        font_letter.stroke("calligraphic", grid.stroke_width, grid.stroke_width, 0)

        font_letter.activeLayer = "rounded"
        font_letter.stroke("circular", grid.stroke_width, "butt")

        font_letter.activeLayer = "Fore"

        # merge rounded into foreground
        font_letter.foreground += font_letter.layers["rounded"]
        font_letter.layers["rounded"] = fontforge.layer()

        # merge and clean up
        font_letter.removeOverlap()
        font_letter.round()
        font_letter.simplify()

font.save("moamsans.sfd")

import subprocess

subprocess.Popen([r"C:\Program Files (x86)\FontForgeBuilds\bin\fontforge.exe", "moamsans.sfd"], start_new_session=True)
