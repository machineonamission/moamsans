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
    stroke_ratio=7 / 8,
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
font.layers.add("capless", False)

font.em = lower_grid.em_height
# these have to be rounded
font.ascent = round(lower_grid.ascent)
font.descent = round(lower_grid.descent)

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

                    # stupid fucking edge case where 2 curves can be sequential AND too close for a full stroke between them, so we have to connect them
                    prev_edge_case = prev_point.rounded and prev_diff.length / 2 <= grid.stroke_width
                    next_edge_case = next_point and next_point.rounded and next_diff.length / 2 <= grid.stroke_width

                    if prev_edge_case:
                        # connect to previous contour
                        curvetour = contour
                        # throw out and reset contour var if we made one
                        contour = fontforge.contour()
                        contour.moveTo(*post_curve.as_tuple())
                    else:
                        # create space in our normal contour for the curve (by making a new contour lol)
                        contour.lineTo(*pre_curve.as_tuple())
                        font_letter.foreground += contour
                        # start new contour
                        contour = fontforge.contour()
                        contour.moveTo(*post_curve.as_tuple())
                        # init arc (we start a little off to make "remove overlap" operation work better)
                        curvetour = fontforge.contour()
                        curvetour.moveTo(*pre_curve.as_tuple())

                    # bring curve to arc start
                    curvetour.lineTo(*curve_start.as_tuple())
                    # draw arc
                    curvetour.cubicTo(control_1.as_tuple(), control_2.as_tuple(), curve_end.as_tuple())

                    if next_edge_case:
                        # connect to next contour
                        contour = curvetour
                    else:
                        # add extra segment to make remove overlap work better
                        curvetour.lineTo(*post_curve.as_tuple())
                        # save arc
                        font_letter.layers["rounded"] += curvetour

                else:
                    contour.lineTo(*pixel.as_tuple())
            font_letter.foreground += contour

        # stroke layers appropriately
        font_letter.activeLayer = "Fore"
        font_letter.stroke("calligraphic", grid.stroke_width, grid.stroke_width, 0)

        font_letter.activeLayer = "rounded"
        font_letter.stroke("circular", grid.stroke_width, cap="butt")

        font_letter.activeLayer = "Fore"

        # merge rounded into foreground
        font_letter.foreground += font_letter.layers["rounded"]
        font_letter.layers["rounded"] = fontforge.layer()

        font_letter.foreground += font_letter.layers["capless"]
        font_letter.layers["capless"] = fontforge.layer()

        # merge and clean up
        font_letter.removeOverlap()
        font_letter.round()
        font_letter.simplify()

font.selection.all()

# clean up font
font.round()
font.addExtrema()
font.autoHint()

# auto glyph width
font.autoWidth(round(lower_grid.stroke_width))

# auto kern
font.addLookup("kern", "gpos_pair", None, (("kern", (("latn", ("dflt")),)),))
font.addKerningClass("kern", "kern-1", round(lower_grid.stroke_width), 5)
#
# # metadata
# name = "MoaM Sans"
#
# font.familyname = name
# font.fontname = name
# font.fullname = name
# font.copyright = """Copyright (c) 2026, Machine on a Mission (https://machineonamission.me),
# with Reserved Font Name MoaM Sans."""
# font.version = "1.0"
#
# # extra metadata
# lang = "English (US)"
#
# font.appendSFNTName(lang, "Designer URL", "https://machineonamission.me/")
# font.appendSFNTName(lang, "Designer", "Machine on a Mission")
# font.appendSFNTName(lang, "Sample Text", "Machine on a Mission")
# font.appendSFNTName(lang, "License URL", "http://scripts.sil.org/OFL")
# font.appendSFNTName(lang, "License", """This Font Software is licensed under the SIL Open Font License, Version 1.1.
# This license is copied below, and is also available with a FAQ at:
# http://scripts.sil.org/OFL
#
#
# -----------------------------------------------------------
# SIL OPEN FONT LICENSE Version 1.1 - 26 February 2007
# -----------------------------------------------------------
#
# PREAMBLE
# The goals of the Open Font License (OFL) are to stimulate worldwide
# development of collaborative font projects, to support the font creation
# efforts of academic and linguistic communities, and to provide a free and
# open framework in which fonts may be shared and improved in partnership
# with others.
#
# The OFL allows the licensed fonts to be used, studied, modified and
# redistributed freely as long as they are not sold by themselves. The
# fonts, including any derivative works, can be bundled, embedded,
# redistributed and/or sold with any software provided that any reserved
# names are not used by derivative works. The fonts and derivatives,
# however, cannot be released under any other type of license. The
# requirement for fonts to remain under this license does not apply
# to any document created using the fonts or their derivatives.
#
# DEFINITIONS
# "Font Software" refers to the set of files released by the Copyright
# Holder(s) under this license and clearly marked as such. This may
# include source files, build scripts and documentation.
#
# "Reserved Font Name" refers to any names specified as such after the
# copyright statement(s).
#
# "Original Version" refers to the collection of Font Software components as
# distributed by the Copyright Holder(s).
#
# "Modified Version" refers to any derivative made by adding to, deleting,
# or substituting -- in part or in whole -- any of the components of the
# Original Version, by changing formats or by porting the Font Software to a
# new environment.
#
# "Author" refers to any designer, engineer, programmer, technical
# writer or other person who contributed to the Font Software.
#
# PERMISSION & CONDITIONS
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of the Font Software, to use, study, copy, merge, embed, modify,
# redistribute, and sell modified and unmodified copies of the Font
# Software, subject to the following conditions:
#
# 1) Neither the Font Software nor any of its individual components,
# in Original or Modified Versions, may be sold by itself.
#
# 2) Original or Modified Versions of the Font Software may be bundled,
# redistributed and/or sold with any software, provided that each copy
# contains the above copyright notice and this license. These can be
# included either as stand-alone text files, human-readable headers or
# in the appropriate machine-readable metadata fields within text or
# binary files as long as those fields can be easily viewed by the user.
#
# 3) No Modified Version of the Font Software may use the Reserved Font
# Name(s) unless explicit written permission is granted by the corresponding
# Copyright Holder. This restriction only applies to the primary font name as
# presented to the users.
#
# 4) The name(s) of the Copyright Holder(s) or the Author(s) of the Font
# Software shall not be used to promote, endorse or advertise any
# Modified Version, except to acknowledge the contribution(s) of the
# Copyright Holder(s) and the Author(s) or with their explicit written
# permission.
#
# 5) The Font Software, modified or unmodified, in part or in whole,
# must be distributed entirely under this license, and must not be
# distributed under any other license. The requirement for fonts to
# remain under this license does not apply to any document created
# using the Font Software.
#
# TERMINATION
# This license becomes null and void if any of the above conditions are
# not met.
#
# DISCLAIMER
# THE FONT SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO ANY WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT
# OF COPYRIGHT, PATENT, TRADEMARK, OR OTHER RIGHT. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# INCLUDING ANY GENERAL, SPECIAL, INDIRECT, INCIDENTAL, OR CONSEQUENTIAL
# DAMAGES, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF THE USE OR INABILITY TO USE THE FONT SOFTWARE OR FROM
# OTHER DEALINGS IN THE FONT SOFTWARE.""")


if not fontforge.hasUserInterface():
    font.save("moamsans.sfd")
    import subprocess

    subprocess.Popen([r"C:\Program Files (x86)\FontForgeBuilds\bin\fontforge.exe", "moamsans.sfd"],
                     start_new_session=True)
