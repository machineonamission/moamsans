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
font.layers.add("capless", False)
font.layers.add("rounded", False)
known_square_sizes = set()

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
            for i in range(0, len(line.points) - 1):
                p1 = line.points[i]
                p2 = line.points[i + 1]

                pixel1 = grid.point_pos(p1)
                pixel2 = grid.point_pos(p2)

                diff = pixel2 - pixel1

                # too little space for a normal line
                if p1.rounded and p2.rounded and diff.length / 2 < grid.stroke_width:
                    pass
                else:
                    contour = fontforge.contour()
                    contour.moveTo(*pixel1.as_tuple())
                    contour.lineTo(*pixel2.as_tuple())

                    angle = diff.angle
                    round_angle = round(radians_to_degrees(angle)) % 90

                    if round_angle == 0:
                        font_letter.foreground += contour
                    else:
                        size = grid.stroke_width / (abs(math.cos(angle)) + abs(math.sin(angle)))
                        if size not in known_square_sizes:
                            known_square_sizes.add(size)
                            font.layers.add(f"square {size}", False)
                        font_letter.layers[f"square {size}"] += contour



        # stroke layers appropriately
        font_letter.activeLayer = "Fore"
        font_letter.stroke("calligraphic", grid.stroke_width, grid.stroke_width, 0)

        font_letter.activeLayer = "rounded"
        font_letter.stroke("circular", grid.stroke_width, cap="butt")

        font_letter.activeLayer = "Fore"

        for s in known_square_sizes:
            font_letter.activeLayer = f"square {s}"
            font_letter.stroke("calligraphic", s, s, 0)

        for layer in ["rounded", "capless"] + [f"square {s}" for s in known_square_sizes]:
            font_letter.foreground += font_letter.layers[layer]
            font_letter.layers[layer] = fontforge.layer()

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
