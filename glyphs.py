import math

from structs import Letter, Line, Point

lower_letters = {

    'a': Letter([
        Line([
            Point(0, 2),
            Point(2, 2, True),
            Point(2, 0),
            Point(0, 0, True),
            Point(0, 1, True),
            Point(2, 1),
        ]),
    ]),
    'b': Letter([
        Line([
            Point(0, 3),
            Point(0, 0),
            Point(2, 0, True),
            Point(2, 2, True),
            Point(0, 2),
        ]),
    ]),
    'c': Letter([
        Line([
            Point(2, 2),
            Point(0, 2, True),
            Point(0, 0, True),
            Point(2, 0),
        ]),
    ]),
    'd': Letter([
        Line([
            Point(2, 3),
            Point(2, 0),
            Point(0, 0, True),
            Point(0, 2, True),
            Point(2, 2),
        ]),
    ]),
    'e': Letter([
        Line([
            Point(2, 0),
            Point(0, 0, True),
            Point(0, 2, True),
            Point(2, 2, True),
            Point(2, 1, True),
            Point(0, 1),
        ]),
    ]),
    'f': Letter([
        Line([
            Point(1, 0),
            Point(1, 3, True),
            Point(2, 3),
        ]),
        Line([
            Point(0, 2),
            Point(2, 2),
        ]),
    ]),
    'g': Letter([
        Line([
            Point(0, -1),
            Point(2, -1, True),
            Point(2, 2),
            Point(0, 2, True),
            Point(0, 0, True),
            Point(2, 0),
        ]),
    ]),
    'h': Letter([
        Line([
            Point(0, 0),
            Point(0, 3),
        ]),
        Line([
            Point(0, 2),
            Point(2, 2, True),
            Point(2, 0),
        ]),
    ]),
    'i': Letter([
        Line([
            Point(1, 0),
            Point(1, 2),
        ]),
        Line([
            Point(1, 3),
        ]),
    ]),
    'j': Letter([
        Line([
            Point(0, -1),
            Point(1, -1, True),
            Point(1, 2),
        ]),
        Line([
            Point(1, 3),
        ]),
    ]),
    'k': Letter([
        Line([
            Point(0, 0),
            Point(0, 3),
        ]),
        Line([
            Point(2, 2),
            Point(0, 1),
            Point(2, 0),
        ]),
    ]),
    'l': Letter([
        Line([
            Point(1, 3),
            Point(1, 0, True),
            Point(2, 0),
        ]),
    ]),
    'm': Letter([
        Line([
            Point(0, 0),
            Point(0, 2),
            Point(3, 2, True),
            Point(3, 0),
        ]),
        Line([
            Point(1.5, 0),
            Point(1.5, 2),
        ]),
    ]),
    'n': Letter([
        Line([
            Point(0, 0),
            Point(0, 2),
            Point(2, 2, True),
            Point(2, 0),
        ]),
    ]),
    'o': Letter([
        Line([
            # technically i dont support starting or ending with curves, so evil hack
            Point(0, 1),
            Point(0, 2, True),
            Point(2, 2, True),
            Point(2, 0, True),
            Point(0, 0, True),
            Point(0, 1),
        ]),
    ]),
    'p': Letter([
        Line([
            Point(0, -1),
            Point(0, 2),
            Point(2, 2, True),
            Point(2, 0, True),
            Point(0, 0),
        ]),
    ]),
    'q': Letter([
        Line([
            Point(2, -1),
            Point(2, 2),
            Point(0, 2, True),
            Point(0, 0, True),
            Point(2, 0),
        ]),
    ]),
    'r': Letter([
        Line([
            Point(0, 0),
            Point(0, 2),
            Point(1, 2),
        ]),
    ]),
    's': Letter([
        Line([
            Point(0, 0),
            Point(2, 0, True),
            Point(2, 1, True),
            Point(0, 1, True),
            Point(0, 2, True),
            Point(2, 2),
        ]),
    ]),
    't': Letter([
        Line([
            Point(1, 3),
            Point(1, 0, True),
            Point(2, 0),
        ]),
        Line([
            Point(0, 2),
            Point(2, 2),
        ]),
    ]),
    'u': Letter([
        Line([
            Point(0, 2),
            Point(0, 0, True),
            Point(2, 0),
            Point(2, 2),
        ]),
    ]),
    'v': Letter([
        Line([
            Point(0, 2),
            Point(1, 0),
            Point(2, 2),
        ]),
    ]),
    'w': Letter([
        Line([
            Point(0, 2),
            Point(0, 0, True),
            Point(3, 0),
            Point(3, 2),
        ]),
        Line([
            Point(1.5, 0),
            Point(1.5, 2),
        ]),
    ]),
    'x': Letter([
        Line([
            Point(0, 0),
            Point(2, 2),
        ]),
        Line([
            Point(2, 0),
            Point(0, 2),
        ]),
    ]),
    'y': Letter([
        Line([
            Point(0, -1),
            Point(2, -1, True),
            Point(2, 2),
        ]),
        Line([
            Point(0, 2),
            Point(0, 0, True),
            Point(2, 0),
        ]),
    ]),
    'z': Letter([
        Line([
            Point(0, 2),
            Point(2, 2),
            Point(0, 0),
            Point(2, 0),
        ]),
    ]),
    # symbols
    r"'": Letter([
        Line([
            Point(0, 3),
            Point(0, 2),
        ]),
    ]),
    r'"': Letter([
        Line([
            Point(0, 3),
            Point(0, 2),
        ]),
        Line([
            Point(2, 3),
            Point(2, 2),
        ]),
    ]),
    r'.': Letter([
        Line([
            Point(0, 0),
        ]),
    ]),
    r':': Letter([
        Line([
            Point(0, 0),
        ]),
        Line([
            Point(0, 2),
        ]),
    ]),
    r',': Letter([
        Line([
            Point(0, 0),
            Point(0, -1),
        ]),
    ]),
    r';': Letter([
        Line([
            Point(0, 0),
            Point(0, -1),
        ]),
        Line([
            Point(0, 2),
        ]),
    ]),
    r'(': Letter([
        Line([
            Point(1, 0),
            Point(0, 0, True),
            Point(0, 3, True),
            Point(1, 3),
        ]),
    ]),
    r'!': Letter([
        Line([
            Point(0, 0),
        ]),
        Line([
            Point(0, 1),
            Point(0, 3),
        ]),
    ]),
    r'?': Letter([
        Line([
            Point(1, 0),
        ]),
        Line([
            Point(1, 1),
            Point(1, 2, True),
            Point(2, 2, True),
            Point(2, 3, True),
            Point(0, 3, True),
            Point(0, 2),
        ], restrictive_trim_end=True),
    ]),
    r')': Letter([
        Line([
            Point(0, 0),
            Point(1, 0, True),
            Point(1, 3, True),
            Point(0, 3),
        ]),
    ]),
    r'+': Letter([
        Line([
            Point(1, 2.5),
            Point(1, 0.5),
        ]),
        Line([
            Point(0, 1.5),
            Point(2, 1.5),
        ]),
    ]),
    r'-': Letter([
        Line([
            Point(0, 1.5),
            Point(2, 1.5),
        ]),
    ]),
    r'*': Letter([
        Line([
            Point(1, 2),
            Point(1 + math.sin(math.tau / 5 * i), 2 + math.cos(math.tau / 5 * i)),
        ]) for i in range(1, 6)
    ]),
    r'/': Letter([
        Line([
            Point(0, 0),
            Point(2, 3),
        ]),
    ]),
    '\\': Letter([
        Line([
            Point(0, 3),
            Point(2, 0),
        ]),
    ]),
    r'=': Letter([
        Line([
            Point(0, 0.5),
            Point(2, 0.5),
        ]),
        Line([
            Point(0, 2.5),
            Point(2, 2.5),
        ]),
    ]),
    r'<': Letter([
        Line([
            Point(2, 2),
            Point(0, 1),
            Point(2, 0),
        ]),
    ]),
    r'>': Letter([
        Line([
            Point(0, 2),
            Point(2, 1),
            Point(0, 0),
        ]),
    ]),
    r'@': Letter([
        Line([
            Point(2.5, 0),
            Point(2.5, 2),
            Point(1, 2, True),
            Point(1, 0, True),
            Point(4, 0, True),
            Point(4, 3, True),
            Point(-0.5, 3, True),
            Point(-0.5, -1, True),
            Point(4, -1),
        ]),
    ]),
    r'[': Letter([
        Line([
            Point(1, 0),
            Point(0, 0),
            Point(0, 3),
            Point(1, 3),
        ]),
    ]),
    r']': Letter([
        Line([
            Point(0, 0),
            Point(1, 0),
            Point(1, 3),
            Point(0, 3),
        ]),
    ]),
    r'^': Letter([
        Line([
            Point(0, 2),
            Point(1, 3),
            Point(2, 2),
        ]),
    ]),
    r'_': Letter([
        Line([
            Point(0, -1),
            Point(2, -1),
        ]),
    ]),
    r'`': Letter([
        Line([
            Point(0, 3),
            Point(1, 2),
        ]),
    ]),
    r'{': Letter([
        Line([
            Point(2, -1),
            Point(1, -1, True),
            Point(1, 0, True),
            Point(0, 1),
            Point(1, 2, True),
            Point(1, 3, True),
            Point(2, 3),
        ]),
    ]),
    r'}': Letter([
        Line([
            Point(0, -1),
            Point(1, -1, True),
            Point(1, 0, True),
            Point(2, 1),
            Point(1, 2, True),
            Point(1, 3, True),
            Point(0, 3),
        ]),
    ]),
    r'|': Letter([
        Line([
            Point(0, -1),
            Point(0, 3)
        ]),
    ]),
    r'~': Letter([
        Line([
            Point(0, 1),
            Point(0, 2, True),
            Point(1, 2, True),
            Point(1, 1, True),
            Point(2, 1, True),
            Point(2, 2)
        ], ),
    ]),
    '$': Letter([
        Line([
            Point(0, 0),
            Point(2.5, 0, True),
            Point(2.5, 1, True),
            Point(0, 1, True),
            Point(0, 2, True),
            Point(2.5, 2),
        ]),
        Line([
            Point(1.25, -1),
            Point(1.25, 3),
        ]),
    ]),
    '%': Letter([
        Line([
            Point(0, 2.5),
            Point(0, 3, True),
            Point(1, 3, True),
            Point(1, 2, True),
            Point(0, 2, True),
            Point(0, 2.5),

        ], restrictive_trim_end=True, restrictive_trim_start=True),
        Line([
            Point(2, 0.5),
            Point(2, 1, True),
            Point(3, 1, True),
            Point(3, 0, True),
            Point(2, 0, True),
            Point(2, 0.5),

        ], restrictive_trim_end=True, restrictive_trim_start=True),
        Line([
            Point(0, 0),
            Point(3, 3),
        ]),
    ]),
    '#': Letter([
        Line([
            Point(0, 0.5),
            Point(3, 0.5),
        ]),
        Line([
            Point(0, 2.5),
            Point(3, 2.5),
        ]),
        Line([
            Point(0.5, 0),
            Point(0.5, 3),
        ]),
        Line([
            Point(2.5, 0),
            Point(2.5, 3),
        ]),
    ]),
}

upper_letters = {
    'A': Letter([
        Line([
            Point(0, 0),
            Point(0, 2, True),
            Point(2, 2, True),
            Point(2, 0),
        ]),
        Line([
            Point(0, 1),
            Point(2, 1),
        ]),
    ]),
    'B': Letter([
        Line([
            Point(0, 2),
            Point(2, 2, True),
            Point(2, 0, True),
            Point(0, 0),
            Point(0, 2),
        ]),
        Line([
            Point(0, 1),
            Point(2, 1),
        ]),
    ]),
    'C': Letter([
        Line([
            Point(2, 2),
            Point(0, 2, True),
            Point(0, 0, True),
            Point(2, 0),
        ]),
    ]),
    'D': Letter([
        Line([
            Point(0, 2),
            Point(2, 2, True),
            Point(2, 0, True),
            Point(0, 0),
            Point(0, 2),
        ]),
    ]),
    'E': Letter([
        Line([
            Point(2, 2),
            Point(0, 2),
            Point(0, 0),
            Point(2, 0),
        ]),
        Line([
            Point(0, 1),
            Point(1, 1),
        ]),
    ]),
    'F': Letter([
        Line([
            Point(2, 2),
            Point(0, 2),
            Point(0, 0),
        ]),
        Line([
            Point(0, 1),
            Point(1, 1),
        ]),
    ]),
    'G': Letter([
        Line([
            Point(2, 2),
            Point(0, 2, True),
            Point(0, 0, True),
            Point(2, 0),
        ]),
        Line([
            Point(2, 0),
            Point(2, 1),
            Point(1, 1),
        ])
    ]),
    'H': Letter([
        Line([
            Point(0, 2),
            Point(0, 0),
        ]),
        Line([
            Point(0, 1),
            Point(2, 1),
        ]),
        Line([
            Point(2, 2),
            Point(2, 0),
        ])
    ]),
    'I': Letter([
        Line([
            Point(2, 0),
            Point(0, 0),
        ]),
        Line([
            Point(1, 0),
            Point(1, 2),
        ]),
        Line([
            Point(2, 2),
            Point(0, 2),
        ])
    ]),
    'J': Letter([
        Line([
            Point(2, 2),
            Point(0, 2),
        ]),
        Line([
            Point(0, 0),
            Point(1, 0, True),
            Point(1, 2),
        ]),
    ]),
    'K': Letter([
        Line([
            Point(0, 0),
            Point(0, 2),
        ]),
        Line([
            Point(2, 2),
            Point(0, 1),
            Point(2, 0),
        ]),
    ]),
    'L': Letter([
        Line([
            Point(0, 2),
            Point(0, 0),
            Point(2, 0),
        ]),
    ]),
    'M': Letter([
        Line([
            Point(0, 0),
            Point(0, 2),
            Point(2, 2, True),
            Point(2, 0),
        ]),
        Line([
            Point(1, 0),
            Point(1, 2),
        ]),
    ]),
    'N': Letter([
        Line([
            Point(0, 0),
            Point(0, 2),
            Point(2, 0),
            Point(2, 2),
        ]),
    ]),
    'O': Letter([
        Line([
            # technically i dont support starting or ending with curves, but technically this is 4 all rounded corners,
            # so evil hack
            Point(0, 1),
            Point(0, 2, True),
            Point(2, 2, True),
            Point(2, 0, True),
            Point(0, 0, True),
            Point(0, 1),
        ]),
    ]),
    'P': Letter([
        Line([
            Point(0, 0),
            Point(0, 2),
            Point(2, 2, True),
            Point(2, 1, True),
            Point(0, 1),
        ]),
    ]),
    'Q': Letter([
        Line([
            Point(2, 0),
            Point(0, 0, True),
            Point(0, 2, True),
            Point(2, 2, True),
            Point(2, 0),
        ]),
        Line([
            Point(2, 0),
            Point(1, 1),
        ], restrictive_clip_entire_line=True),
    ]),
    'R': Letter([
        Line([
            Point(0, 0),
            Point(0, 2),
            Point(2, 2, True),
            Point(2, 1, True),
            Point(0, 1),
        ]),
        Line([
            Point(1, 1),
            Point(2, 0),
        ]),
    ]),
    'S': Letter([
        Line([
            Point(0, 0),
            Point(2, 0, True),
            Point(2, 1, True),
            Point(0, 1, True),
            Point(0, 2, True),
            Point(2, 2),
        ]),
    ]),
    'T': Letter([
        Line([
            Point(0, 2),
            Point(2, 2),
        ]),
        Line([
            Point(1, 2),
            Point(1, 0),
        ]),
    ]),
    'U': Letter([
        Line([
            Point(0, 2),
            Point(0, 0, True),
            Point(2, 0, True),
            Point(2, 2),
        ]),
    ]),
    'V': Letter([
        Line([
            Point(0, 2),
            Point(1, 0),
            Point(2, 2),
        ]),
    ]),
    'W': Letter([
        Line([
            Point(0, 2),
            Point(0, 0, True),
            Point(2, 0),
            Point(2, 2),
        ]),
        Line([
            Point(1, 0),
            Point(1, 2),
        ]),
    ]),
    'X': Letter([
        Line([
            Point(0, 0),
            Point(2, 2),
        ]),
        Line([
            Point(2, 0),
            Point(0, 2),
        ]),
    ]),
    'Y': Letter([
        Line([
            Point(0, 2),
            Point(1, 1),
            Point(2, 2),
        ]),
        Line([
            Point(1, 0),
            Point(1, 1),
        ]),
    ]),
    'Z': Letter([
        Line([
            Point(0, 2),
            Point(2, 2),
            Point(0, 0),
            Point(2, 0),
        ]),
    ]),
    # digits
    '0': Letter([
        Line([
            # technically i dont support starting or ending with curves, so evil hack
            Point(0, 1),
            Point(0, 2, True),
            Point(2, 2, True),
            Point(2, 0, True),
            Point(0, 0, True),
            Point(0, 1),
        ]),
        Line([
            Point(0, 2),
            Point(2, 0),
        ], restrictive_clip_entire_line=True),
    ]),
    '1': Letter([
        Line([
            Point(0, 2),
            Point(1, 2),
            Point(1, 0),
        ]),
        Line([
            Point(0, 0),
            Point(2, 0),
        ]),
    ]),
    '2': Letter([
        Line([
            Point(2, 0),
            Point(0, 0),
            Point(0, 1, True),
            Point(2, 1, True),
            Point(2, 2, True),
            Point(0, 2),
        ]),
    ]),
    '3': Letter([
        Line([
            Point(0, 2),
            Point(2, 2, True),
            Point(2, 0, True),
            Point(0, 0),
        ]),
        Line([
            Point(0, 1),
            Point(2, 1),
        ]),
    ]),
    '4': Letter([
        Line([
            Point(0, 2),
            Point(0, 1),
            Point(2, 1),
        ]),
        Line([
            Point(2, 0),
            Point(2, 2),
        ]),
    ]),
    '5': Letter([
        Line([
            Point(0, 0),
            Point(2, 0, True),
            Point(2, 1, True),
            Point(0, 1),
            Point(0, 2),
            Point(2, 2),
        ]),
    ]),
    '6': Letter([
        Line([
            Point(2, 2),
            Point(0, 2, True),
            Point(0, 0, True),
            Point(2, 0, True),
            Point(2, 1, True),
            Point(0, 1),
        ]),
    ]),
    '7': Letter([
        Line([
            Point(0, 2),
            Point(2, 2),
            Point(2, 0),
        ]),
    ]),
    '8': Letter([
        Line([
            # technically i dont support starting or ending with curves, but we can make the 8 without that
            Point(0, 1),
            Point(0, 2, True),
            Point(2, 2, True),
            Point(2, 0, True),
            Point(0, 0, True),
            Point(0, 1),
            Point(2, 1),
        ]),
    ]),
    '9': Letter([
        Line([
            Point(0, 0),
            Point(2, 0, True),
            Point(2, 2, True),
            Point(0, 2, True),
            Point(0, 1, True),
            Point(2, 1),
        ]),
    ]),
    # symbols
    '&': Letter([
        Line([
            Point(2, 0),
            Point(0.25, 2, True),
            Point(1.75, 2, True),
            Point(0, 0, True),
            Point(1, 0, True),
            Point(2, 1),
        ]),
    ]),
    # '$': Letter([
    #     Line([
    #         Point(0, 0),
    #         Point(2, 0, True),
    #         Point(2, 1, True),
    #         Point(0, 1, True),
    #         Point(0, 2, True),
    #         Point(2, 2),
    #     ]),
    #     Line([
    #         Point(1, 0),
    #         Point(1, 2),
    #     ]),
    # ]),
}
