import fontforge
import math

from glyphs import lower_letters, upper_letters
from structs import *

lower_grid = Grid(
    xmin=0,
    xmax=2,
    ymin=-1,
    ymax=3,
    em_height=1000,
    x_ratio=0.8,
    stroke_ratio=1,
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

# print(lower_grid.ascent, lower_grid.descent)
# print(lower_grid.stroke_width)

fontforge.runInitScripts()
font = fontforge.font()
font.layers.add("scratch", False)

font.em = lower_grid.em_height
# these have to be rounded
font.ascent = round(lower_grid.ascent)
font.descent = round(lower_grid.descent)

font.encoding = "UnicodeFull"

circle_constant = (4 / 3) * (math.sqrt(2) - 1)  # for bezier circle approximation


def rect_at(bottom_left: PixelPoint, top_right: PixelPoint):
    contour = fontforge.contour()
    contour.moveTo(*bottom_left.as_tuple())
    contour.lineTo(bottom_left.x, top_right.y)
    contour.lineTo(*top_right.as_tuple())
    contour.lineTo(top_right.x, bottom_left.y)
    contour.lineTo(*bottom_left.as_tuple())
    contour.closed = True
    return contour


def box_at(center: PixelPoint, radius: float):
    bottom_left = center - radius
    top_right = center + radius
    return rect_at(bottom_left, top_right)


def circle_angle_to_square_size(angle_rad: float, radius: float) -> float:
    return radius / (abs(math.cos(angle_rad)) + abs(math.sin(angle_rad)))


def scract_to_foreground():
    font_letter.foreground += font_letter.layers["scratch"]
    font_letter.layers["scratch"] = fontforge.layer()


for grid, letters in master_list:
    grid: Grid
    for letter_key, letter in letters.items():
        print(letter_key)
        letter: Letter
        font_letter: fontforge.glyph = font.createMappedChar(letter_key)
        for orig_line in letter.lines:
            orig_line: Line
            if len(orig_line.points) == 1:  # special case: just a dot, strokes dont work, draw directly
                point = orig_line.points[0]
                pixel = grid.point_pos(point)

                font_letter.foreground += box_at(pixel, grid.hsw)
            else:
                # hack to get ends to work properly
                lines = [
                    (orig_line, orig_line.restrictive_clip_entire_line)
                ]
                # if we restrictive clip the entire line, these ends are pointless
                if not orig_line.restrictive_clip_entire_line:
                    # explicitly extend the caps, we will clip them off later per each endpoint
                    for (end_p, next_p, extend) in [
                        (orig_line.points[0], orig_line.points[1], orig_line.restrictive_trim_start),
                        (orig_line.points[-1], orig_line.points[-2], orig_line.restrictive_trim_end)]:
                        dx = end_p.x - next_p.x
                        dy = end_p.y - next_p.y
                        midpx = end_p.x - (dx / 2)
                        midpy = end_p.y - (dy / 2)
                        super_end_x = end_p.x + (dx * 10)
                        super_end_y = end_p.y + (dy * 10)
                        super_end = Point(super_end_x, super_end_y, exclude_from_clip_box=True)
                        lines.append((Line([
                            super_end, end_p, Point(midpx, midpy)
                        ]), extend))

                for (line, restrictive_clip) in lines:
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

                            # control points for bezier curve
                            circle_offset = grid.hsw * (1 - circle_constant)
                            control_1 = pixel - prev_normal * circle_offset
                            control_2 = pixel - next_normal * circle_offset

                            # bring curve to arc start
                            contour.lineTo(*curve_start.as_tuple())
                            # draw arc
                            contour.cubicTo(control_1.as_tuple(), control_2.as_tuple(), curve_end.as_tuple())
                        else:
                            contour.lineTo(*pixel.as_tuple())
                    # complete contour
                    font_letter.layers["scratch"] += contour

                    # stroke it
                    font_letter.activeLayer = "scratch"
                    font_letter.stroke("circular", grid.stroke_width, cap="butt", join="miter",
                                       extendcap=0)

                    # clip the path in a nice way that preserves sharp corners

                    # construct bounding box
                    pixels = [grid.point_pos(p) for p in line.points if not p.exclude_from_clip_box]
                    offset = 0 if restrictive_clip or line.restrictive_clip_entire_line else grid.hsw
                    min_x = min(p.x for p in pixels) - offset
                    max_x = max(p.x for p in pixels) + offset
                    min_y = min(p.y for p in pixels) - offset
                    max_y = max(p.y for p in pixels) + offset

                    # sometimes we want a restrictive clip on a vertical/horizontal line, so make that actually work
                    if min_x == max_x:
                        min_x -= grid.hsw
                        max_x += grid.hsw
                    if min_y == max_y:
                        min_y -= grid.hsw
                        max_y += grid.hsw

                    font_letter.layers["scratch"] += rect_at(PixelPoint(min_x, min_y), PixelPoint(max_x, max_y))

                    # do this otherwise there's odd behavior with like float epsilon garbage, we have to do it
                    # eventually anyways
                    font_letter.round()
                    # AND operation of our box and stuff
                    font_letter.intersect()

                    # merge with foreground
                    scract_to_foreground()

        # merge and clean up
        font_letter.activeLayer = "Fore"

        font_letter.removeOverlap()
        font_letter.simplify()

font.selection.all()

# clean up font
font.round()
font.addExtrema()
font.autoHint()
font.correctDirection()

spacing = round(lower_grid.xstep / 2)

# auto glyph width
font.autoWidth(spacing)

font.selection.all()

# auto kern
font.addLookup("kern", "gpos_pair", None, (("kern", (("latn", ("dflt")),)),))
font.addLookupSubtable("kern", "kern-1")
# cl = font.addKerningClass("kern", "kern-1", round(spacing), 1)
font.autoKern("kern-1", round(spacing), touch=True)

space: fontforge.glyph = font.createMappedChar(" ")
space.width = spacing * 3

font.reencode("Compacted")

# metadata
name = "MoaM Sans"

font.familyname = name
font.fontname = name
font.fullname = name
font.copyright = """Copyright (c) 2026, Machine on a Mission (https://machineonamission.me),
with Reserved Font Name MoaM Sans."""
font.version = "2.2"

# extra metadata
lang = "English (US)"

font.appendSFNTName(lang, "Designer URL", "https://machineonamission.me/")
font.appendSFNTName(lang, "Designer", "Machine on a Mission")
font.appendSFNTName(lang, "Sample Text", "Machine on a Mission")
font.appendSFNTName(lang, "License URL", "http://scripts.sil.org/OFL")
font.appendSFNTName(lang, "License", """This Font Software is licensed under the SIL Open Font License, Version 1.1.
This license is copied below, and is also available with a FAQ at:
http://scripts.sil.org/OFL


-----------------------------------------------------------
SIL OPEN FONT LICENSE Version 1.1 - 26 February 2007
-----------------------------------------------------------

PREAMBLE
The goals of the Open Font License (OFL) are to stimulate worldwide
development of collaborative font projects, to support the font creation
efforts of academic and linguistic communities, and to provide a free and
open framework in which fonts may be shared and improved in partnership
with others.

The OFL allows the licensed fonts to be used, studied, modified and
redistributed freely as long as they are not sold by themselves. The
fonts, including any derivative works, can be bundled, embedded,
redistributed and/or sold with any software provided that any reserved
names are not used by derivative works. The fonts and derivatives,
however, cannot be released under any other type of license. The
requirement for fonts to remain under this license does not apply
to any document created using the fonts or their derivatives.

DEFINITIONS
"Font Software" refers to the set of files released by the Copyright
Holder(s) under this license and clearly marked as such. This may
include source files, build scripts and documentation.

"Reserved Font Name" refers to any names specified as such after the
copyright statement(s).

"Original Version" refers to the collection of Font Software components as
distributed by the Copyright Holder(s).

"Modified Version" refers to any derivative made by adding to, deleting,
or substituting -- in part or in whole -- any of the components of the
Original Version, by changing formats or by porting the Font Software to a
new environment.

"Author" refers to any designer, engineer, programmer, technical
writer or other person who contributed to the Font Software.

PERMISSION & CONDITIONS
Permission is hereby granted, free of charge, to any person obtaining
a copy of the Font Software, to use, study, copy, merge, embed, modify,
redistribute, and sell modified and unmodified copies of the Font
Software, subject to the following conditions:

1) Neither the Font Software nor any of its individual components,
in Original or Modified Versions, may be sold by itself.

2) Original or Modified Versions of the Font Software may be bundled,
redistributed and/or sold with any software, provided that each copy
contains the above copyright notice and this license. These can be
included either as stand-alone text files, human-readable headers or
in the appropriate machine-readable metadata fields within text or
binary files as long as those fields can be easily viewed by the user.

3) No Modified Version of the Font Software may use the Reserved Font
Name(s) unless explicit written permission is granted by the corresponding
Copyright Holder. This restriction only applies to the primary font name as
presented to the users.

4) The name(s) of the Copyright Holder(s) or the Author(s) of the Font
Software shall not be used to promote, endorse or advertise any
Modified Version, except to acknowledge the contribution(s) of the
Copyright Holder(s) and the Author(s) or with their explicit written
permission.

5) The Font Software, modified or unmodified, in part or in whole,
must be distributed entirely under this license, and must not be
distributed under any other license. The requirement for fonts to
remain under this license does not apply to any document created
using the Font Software.

TERMINATION
This license becomes null and void if any of the above conditions are
not met.

DISCLAIMER
THE FONT SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO ANY WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT
OF COPYRIGHT, PATENT, TRADEMARK, OR OTHER RIGHT. IN NO EVENT SHALL THE
COPYRIGHT HOLDER BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
INCLUDING ANY GENERAL, SPECIAL, INDIRECT, INCIDENTAL, OR CONSEQUENTIAL
DAMAGES, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF THE USE OR INABILITY TO USE THE FONT SOFTWARE OR FROM
OTHER DEALINGS IN THE FONT SOFTWARE.""")

font.generate("MoaM Sans.otf")

if not fontforge.hasUserInterface():
    font.save("moamsans.sfd")
    import subprocess

    subprocess.Popen([r"C:\Program Files (x86)\FontForgeBuilds\bin\fontforge.exe", "moamsans.sfd"],
                     start_new_session=True)
