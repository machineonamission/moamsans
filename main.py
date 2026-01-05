import fontforge
import psMat
import string

font = fontforge.font()

dir = r"C:\Users\Melody\PycharmProjects\moamsans\SVG"

def make(svg, ch):
    return font.createMappedChar(ch).importOutlines(f"{dir}\\{svg}.svg", scale=False, simplify=False)

# fairly arbitrary font size values that i used in illustrator
ai_ascent=170
ai_descent=50
ai_dist=20

ai_em=ai_ascent+ai_descent

# "ttf has to be power of 2" ok man
em=1024

# scale from ai size to em size
ratio = em/ai_em

font.em = em
# these have to be rounded
font.ascent = round(ai_ascent*ratio)
font.descent = round(ai_descent*ratio)

# go off the rounded ratio
round_ratio = font.ascent/ai_ascent

# use the first lowercase and first uppercase to move the lower left bound to 0,0, and copy that bound to all letters of its type
# just so happens that a and A don't have descents
# scale seems to fuck with it, so this is easier and more precise
lbound = None
ubound = None

for letter in string.ascii_lowercase:
    # scale to size
    r = make(f"low {letter}", letter).transform(psMat.scale(round_ratio))
    # use first letter as origin (a and A happen to have no descents so this is fine)
    if lbound is None:
        lbound = r.boundingBox()[:2]
    # move to 0,0
    r.transform(psMat.translate(-lbound[0], -lbound[1]))

for letter in string.ascii_uppercase:
    r = make(f"cap {letter}", letter).transform(psMat.scale(round_ratio))
    if ubound is None:
        ubound = r.boundingBox()[:2]
    r.transform(psMat.translate(-ubound[0], -ubound[1]))

for letter in string.digits:
    r = make(letter, letter).transform(psMat.scale(round_ratio))
    if ubound is None:
        ubound = r.boundingBox()[:2]
    r.transform(psMat.translate(-ubound[0], -ubound[1]))

font.selection.all()

# clean up font
font.round()
font.addExtrema()
font.autoHint()

# auto glyph width
font.autoWidth(round(ai_dist*round_ratio))

# auto kern
font.addLookup("kern", "gpos_pair", None, (("kern",(("latn",("dflt")),)),))
font.addKerningClass("kern", "kern-1", round(ai_dist*round_ratio), 5)

# metadata
name = "MoaM Sans"

font.familyname = name
font.fontname = name
font.fullname = name
font.copyright = """Copyright (c) 2026, Machine on a Mission (https://machineonamission.me),
with Reserved Font Name MoaM Sans."""
font.version = "1.0"

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