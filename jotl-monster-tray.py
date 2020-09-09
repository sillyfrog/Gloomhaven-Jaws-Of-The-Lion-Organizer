#!/usr/bin/env python3
from solid import (
    cube,
    use,
    scad_render_to_file,
    translate,
    linear_extrude,
    text,
    rotate,
    hull,
    difference,
    cylinder,
    union,
)
from solid.utils import down, up, left, right, back, forward
import pathlib
import math

SHOW_EXTRAS = True
MODIFIER = ""

use("MCAD/boxes.scad")


def objsum(objs):
    ret = objs[0]
    for o in objs[1:]:
        ret += o
    return ret


WALL = 0.8
WALL_L = 1.6
WALL_R = 0.8
END_WALL = 1.6
CARD_WALL = 0.4
FLOOR = 1
TEXT_D = 0.4

Cards = 1
CardStack = 2
CardSplitL = 4
CardSplitR = 5
CardSide = 6
Exclude = -1

LEFT = 0b000001
RIGHT = 0b000010
TOP = 0x000100
BOTTOM = 0x001000
DOUBLE = 0x010000
TRIPLE = 0x100000


def roundedCube(size, radius, sidesonly):
    return translate([size[0] / 2, size[1] / 2, size[2] / 2])(
        roundedBox(size, radius, sidesonly)
    )


STACK_SIZE = {5: 11, 2: 5, 3: 7, 6: 13.5, 0: 0, 10: 22, 4: 10}

CARD_STACK_D = {12: 4, 8: 3, 4: 2, 6: 3, 0: 0}

# To make it slightly shorter to fit in the allocated space, abbreviate Monstrosity
MONSTROSITY = "Monstrsty"

STACKS = [
    {
        "name": "Boss",
        "cards": 6,
        "standees": 3,
        "split_stack": Exclude,
        "width": 57,
        "token": BOTTOM,
    },
    {
        "name": "Stone Golem",
        "cards": 8,
        "standees": 6,
        "split_stack": Exclude,
        "width": 53,
        "token": BOTTOM,
    },
    {
        "name": "Imp",
        "cards": 8,
        "standees": 0,
        "split_stack": Exclude,
        "width": 0,
        "location_include": ["Black Imp", "Blood Imp"],
    },
    {
        "name": "Black Imp",
        "cards": 0,
        "standees": 10,
        "split_stack": CardSplitL,
        "width": 25,
        "left_padding": 5,
        "token": LEFT,
    },
    {
        "name": "Blood Imp",
        "cards": 0,
        "standees": 10,
        "split_stack": CardSplitR,
        "width": 25,
        "left_padding": 5,
        "token": RIGHT,
    },
    {
        "name": "Card Stack",
        "cards": None,
        "standees": None,
        "split_stack": Cards,
        "width": None,
    },
    {
        "name": "Black Sludge",
        "cards": 8,
        "standees": 6,
        "split_stack": CardSide,
        "width": 27,
        "token": RIGHT,
    },
    {
        "name": "Vermling Raider",
        "cards": 8,
        "standees": 10,
        "split_stack": CardSplitL,
        "width": 22,
        "token": RIGHT,
    },
    {
        "name": f"Blood {MONSTROSITY}",
        "cards": 0,
        "standees": 6,
        "split_stack": Exclude,  # Stored outside this holder
        "width": 0,
    },
    {
        "name": "Chaos Demon",
        "cards": 8,
        "standees": 4,
        "split_stack": CardStack,
        "width": 35,
        "left_padding": 4,
        "token": LEFT,
    },
    {
        "name": "Basic Cards",
        "cards": 4 * 3,
        "standees": 0,
        "split_stack": False,
        "width": None,
        "location_include": ["Zealot", "Vermling Raider", "Giant Viper"],
    },
    # {
    #     "name": "Basic Zealot",
    #     "cards": 4,
    #     "standees": 0,
    #     "split_stack": False,
    #     "width": None,
    # },
    # {
    #     "name": "Basic Vermling Raider",
    #     "cards": 4,
    #     "standees": 0,
    #     "split_stack": False,
    #     "width": None,
    # },
    # {
    #     "name": "Basic Giant Viper",
    #     "cards": 4,
    #     "standees": 0,
    #     "split_stack": False,
    #     "width": None,
    # },
    {
        "name": "Living Corpse",
        "cards": 8,
        "standees": 6,
        "split_stack": CardSide,
        "width": 28,
        "token": RIGHT,
    },
    {
        "name": "Zealot",
        "cards": 8,
        "standees": 6,
        "split_stack": CardSide,
        "width": 33,
        "token": 0,
        "token_include": ["Vermling Scout"],
    },
    {
        "name": "Vermling Scout",
        "cards": 8,
        "standees": 6,
        "split_stack": CardSide,
        "width": 26,
        "token": RIGHT | DOUBLE | BOTTOM,
    },
    {
        "name": f"{MONSTROSITY}",
        "cards": 8,
        "standees": 0,
        "split_stack": Exclude,
        "width": 0,
        "location_include": [f"Rat {MONSTROSITY}"],
        # Special case for the Blood Monstrosity off to the side
        "location": [-14, 108 - 45, 40, 14],
    },
    {
        "name": "Living Spirit",
        "cards": 8,
        "standees": 4,
        "split_stack": Exclude,
        "width": 25,
        "token": TOP | TRIPLE,
    },
    {
        "name": f"Rat {MONSTROSITY}",
        "cards": 0,
        "standees": 10,
        "split_stack": Exclude,
        "width": 25.5,
        "token_include": ["Living Spirit"],
    },
    {
        "name": "Giant Viper",
        "cards": 8,
        "standees": 10,
        "split_stack": CardSplitR,
        "width": 22,
        "token": RIGHT | BOTTOM,
    },
]

H_BELOW_DIAL = 42

CARD_W = 69
CARD_H = 45


def card_stack_o(d):
    o = cube([CARD_W, d, CARD_H])
    return o


# def label(txt):
#     if SHOW_EXTRAS:
#         return translate([0, 0, CARD_H])(
#             linear_extrude(1)(
#                 text(
#                     txt, size=3, font="Arial:style=Bold", halign="left", valign="bottom"
#                 )
#             )
#         ).set_modifier("#")
#     else:
#         return cube([1, 1, 1])


def label(txt, h=1, z=-TEXT_D, point_size=3):
    """Generates the object(s) for the given text, up to 3 lines
    """
    LINE_H = point_size + 1
    txt = txt.upper()
    parts = txt.split(" ")
    t = []
    if len(parts) == 1:
        offsets = [0]
    elif len(parts) == 2:
        offsets = [-LINE_H / 2, LINE_H / 2]
    else:
        offsets = [-LINE_H, 0, LINE_H]
    for part in parts:
        t.append(
            translate([0, offsets.pop(), 0])(
                linear_extrude(h)(
                    text(
                        part,
                        size=point_size,
                        font="Arial:style=Bold",
                        halign="center",
                        valign="center",
                    )
                )
            )
        )
    return up(z)(objsum(t).set_modifier(""))


TOKEN_W = 8.9
TOKEN_D = 2.5


def gen_cutout(stack, x, y):
    x_padding = stack.get("left_padding", 0)
    thisstack = STACK_SIZE[stack["standees"]]
    standees = cube([stack["width"], thisstack, CARD_H]).set_modifier(MODIFIER)
    o = standees
    o += translate([stack["width"] / 2, thisstack / 2, 0])(label(stack["name"]))
    # Add the token if required
    token = up(22 - 27 / 2 - FLOOR)(cube([TOKEN_W, TOKEN_D, 27])).set_modifier("")
    if "token" in stack:
        stack.setdefault("token_locations", [])
        if stack["token"] & LEFT:
            if stack["token"] & BOTTOM:
                y = 0
            else:
                y = thisstack - TOKEN_W
            stack["token_locations"].append([-WALL - TOKEN_D, y, TOKEN_W, TOKEN_D])
            o += translate([-WALL, y, 0])(rotate([0, 0, 90])(token))
        elif stack["token"] & RIGHT:
            if stack["token"] & BOTTOM:
                y = 0
            else:
                y = thisstack - TOKEN_W
            stack["token_locations"].append(
                [stack["width"] + WALL, y, TOKEN_W, TOKEN_D]
            )
            o += translate([stack["width"] + WALL + TOKEN_D, y, 0])(
                rotate([0, 0, 90])(token)
            )
            if stack["token"] & DOUBLE:
                stack["token_locations"].append(
                    [stack["width"] + WALL + TOKEN_D, y, TOKEN_W, TOKEN_D]
                )
                o += translate([stack["width"] + WALL + TOKEN_D + TOKEN_D, y, 0])(
                    rotate([0, 0, 90])(token)
                )
        elif stack["token"] & TOP:
            # We know top is only the Living Spirit, so manually rotate here
            stack["token_locations"].append(
                [-WALL - TOKEN_D, stack["width"] - TOKEN_W, TOKEN_W, TOKEN_D]
            )
            o += translate([stack["width"] - TOKEN_W, WALL + thisstack, 0])(token)
            if stack["token"] & TRIPLE:
                stack["token_locations"].append(
                    [-WALL - TOKEN_D * 2, stack["width"] - TOKEN_W, TOKEN_W, TOKEN_D]
                )
                o += translate(
                    [stack["width"] - TOKEN_W, WALL + thisstack + TOKEN_D, 0]
                )(token)
                stack["token_locations"].append(
                    [-WALL - TOKEN_D * 3, stack["width"] - TOKEN_W, TOKEN_W, TOKEN_D]
                )
                o += translate(
                    [stack["width"] - TOKEN_W, WALL + thisstack + TOKEN_D * 2, 0]
                )(token)
        elif stack["token"] & BOTTOM:
            stack["token_locations"].append([0, -WALL - TOKEN_D, TOKEN_D, TOKEN_W])
            o += translate([0, -WALL - TOKEN_D, 0])(token)
    return right(x_padding)(o)


def monster_tray():
    # 12 card stacks
    # 48mm for cards
    d = 0
    card_stack = 0
    card_side = 0

    max_side = 0
    widest_split = 0
    for stack in STACKS:
        thisstack = 0
        if stack["standees"]:
            if stack["split_stack"] in (CardSplitL, CardSplitR):
                thisstack += STACK_SIZE[stack["standees"]]
                thisstack += WALL
                widest_split = max(widest_split, stack["width"])
            elif stack["split_stack"] == CardSide:
                card_side += STACK_SIZE[stack["standees"]]
                card_side += WALL
                max_side = max(max_side, stack["width"])
            else:
                thisstack += STACK_SIZE[stack["standees"]]
                thisstack += WALL
        if stack["cards"]:
            card_stack += CARD_STACK_D[stack["cards"]]
            card_stack += CARD_WALL
        if d + thisstack >= 104:
            print(f"******** Depth of stack: {d}, at: {stack}")
            d = thisstack
        else:
            d += thisstack
        print(stack, thisstack)
    print(
        f"Depth of stacks: {d}mm, Card Stacks: {card_stack}mm, Standee Side: {card_side}mm"
    )
    print(
        f"Total: {d+card_stack+card_side}, Remaining: {(d+card_stack+card_side)-104*2}"
    )
    print(f"Cards: {d+card_stack:.1f}, Card Side: {card_side:.1f}mm")
    print()

    o = roundedCube([108, 108, 22], 6, True)
    edgewalls = (108 - max_side - CARD_W) / 3

    card_offset = END_WALL
    card_l_offset = END_WALL
    card_r_offset = END_WALL
    side_offset = END_WALL

    for_svg = []
    for stack in STACKS:
        if stack["split_stack"] in (Cards,):
            # This is the actual stack of cards
            o -= translate([edgewalls, card_offset, FLOOR])(
                card_stack_o(card_stack).set_modifier(MODIFIER)
            )
            o -= translate(
                [edgewalls + CARD_W / 2, card_offset + card_stack / 2, FLOOR]
            )(label("Cards"))
            card_offset += card_stack + WALL_L
            card_l_offset = card_offset
            card_r_offset = card_offset
            cards_right = edgewalls + CARD_W + WALL_L
            for_svg.append(
                {"text": stack["name"], "width": CARD_W, "depth": card_stack}
            )

        elif stack["split_stack"] in (CardSplitL, CardSplitR):
            thisstack = STACK_SIZE[stack["standees"]]
            if stack["split_stack"] in (CardSplitL,):
                stack["location"] = [
                    edgewalls,
                    card_l_offset,
                    thisstack,
                    stack["width"],
                ]
                o -= translate([edgewalls, card_l_offset, FLOOR])(
                    gen_cutout(stack, stack["width"], thisstack)
                )
                card_l_offset += WALL_L + thisstack
            else:
                stack["location"] = [
                    edgewalls + widest_split + WALL_L,
                    card_r_offset,
                    thisstack,
                    stack["width"],
                ]
                o -= translate(
                    [edgewalls + widest_split + WALL_L, card_r_offset, FLOOR]
                )(gen_cutout(stack, stack["width"], thisstack))
                card_r_offset += WALL_L + thisstack
            card_offset = max(card_offset, card_l_offset, card_r_offset)
            for_svg.append(
                {"text": stack["name"], "width": stack["width"], "depth": thisstack}
            )

        elif stack["split_stack"] in (CardSide,):
            thisstack = STACK_SIZE[stack["standees"]]
            stack["location"] = [
                edgewalls * 2 + CARD_W,
                side_offset,
                thisstack,
                stack["width"],
            ]
            o -= translate([edgewalls * 2 + CARD_W, side_offset, FLOOR])(
                gen_cutout(stack, stack["width"], thisstack)
            )
            side_offset += WALL_R + thisstack
            for_svg.append(
                {"text": stack["name"], "width": stack["width"], "depth": thisstack}
            )

        elif stack["split_stack"] == CardStack:
            thisstack = STACK_SIZE[stack["standees"]]
            card_offset = max(card_offset, card_l_offset, card_r_offset)
            stack["location"] = [edgewalls, card_offset, thisstack, stack["width"]]
            o -= translate([edgewalls, card_offset, FLOOR])(
                gen_cutout(stack, stack["width"], thisstack)
            )
            card_offset += WALL_R + thisstack
            for_svg.append(
                {"text": stack["name"], "width": stack["width"], "depth": thisstack}
            )

        elif stack["split_stack"] == Exclude:
            # Special handling for these
            if stack["name"] == "Boss":
                thisstack = STACK_SIZE[stack["standees"]]
                stack["location"] = [
                    43,
                    108 - END_WALL - thisstack,
                    thisstack,
                    stack["width"],
                ]
                o -= translate([43, 108 - END_WALL - thisstack, FLOOR])(
                    gen_cutout(stack, stack["width"], thisstack)
                )
                boss_stack = thisstack
            elif stack["name"] == "Stone Golem":
                thisstack = STACK_SIZE[stack["standees"]]
                stack["location"] = [
                    108 - edgewalls - stack["width"],
                    108 - END_WALL - thisstack - WALL_R - boss_stack,
                    thisstack,
                    stack["width"],
                ]
                o -= translate(
                    [
                        108 - edgewalls - stack["width"],
                        108 - END_WALL - thisstack - WALL_R - boss_stack,
                        FLOOR,
                    ]
                )(gen_cutout(stack, stack["width"], thisstack))
                stoneg_stack = 108 - END_WALL - thisstack - WALL_R - boss_stack

            elif stack["name"] == "Living Spirit":
                thisstack = STACK_SIZE[stack["standees"]]
                stack["location"] = [
                    cards_right,
                    stoneg_stack - WALL_R - stack["width"],
                    stack["width"],
                    thisstack,
                ]
                o -= translate(
                    [
                        cards_right + thisstack,
                        stoneg_stack - WALL_R - stack["width"],
                        FLOOR,
                    ]
                )(rotate([0, 0, 90])(gen_cutout(stack, stack["width"], thisstack)))
                livingspirit_right = cards_right + thisstack

            elif stack["name"] == f"Rat {MONSTROSITY}":
                thisstack = STACK_SIZE[stack["standees"]]
                stack["location"] = [
                    livingspirit_right,
                    stoneg_stack - WALL_R - stack["width"],
                    thisstack,
                    stack["width"],
                ]
                o -= translate(
                    [
                        livingspirit_right + WALL_R + thisstack,
                        stoneg_stack - WALL_R - stack["width"],
                        FLOOR,
                    ]
                )(rotate([0, 0, 90])(gen_cutout(stack, stack["width"], thisstack)))

            else:
                thisstack = 0
                print(f"Skipping: {stack}")
            if thisstack:
                for_svg.append(
                    {"text": stack["name"], "width": stack["width"], "depth": thisstack}
                )

    # Generate the SVG
    elements = []
    offseto = 10
    offsete = 10
    odds = True
    for item in for_svg:
        item["name"] = item["text"].replace(" ", "_")
        if odds:
            item["posx"] = 5
            item["posy"] = offseto
            offseto += item["depth"] + 10
        else:
            item["posx"] = 100
            item["posy"] = offsete
            offsete += item["depth"] + 10
        odds = not odds
        elements.append(SVG_TEMPLATE.format(**item))

    f = open("outlines.svg", "w")
    f.write(SVG_OUTLINE.format("\n".join(elements)))
    f.close()

    return o


def getstackbyname(txt):
    for stack in STACKS:
        if stack["name"] == txt:
            return stack


def generate_card_dividers():
    LOCATION_SCALE = 0.35
    LOCATION_LINE = 0.8
    LOCATION_THICK = 0.2
    H = 44
    W = 68
    THICK = 0.4
    TAB_H = 10

    RAD = 2.5

    PAD = 0.1

    labels = []
    for stack in STACKS:
        if stack["cards"]:
            labels.append(stack["name"])
    labels.sort()

    def rounded(width, height):
        w = width - RAD * 2
        h = height - RAD * 2
        return hull()(
            translate([RAD, RAD, 0])(cube([w, h, THICK])),
            translate([RAD, RAD, 0])(cylinder(r=RAD, h=THICK)),
            translate([RAD + w, RAD, 0])(cylinder(r=RAD, h=THICK)),
            translate([RAD, RAD + h, 0])(cylinder(r=RAD, h=THICK)),
            translate([RAD + w, RAD + h, 0])(cylinder(r=RAD, h=THICK)),
        )

    def getstacklocations(stackname):
        stack = getstackbyname(stackname)
        locations = []
        if "location" in stack:
            thislocation = stack["location"]
            if stack["split_stack"] in (CardStack, CardSplitL, CardSplitR):
                # Put in some padding to the left to show more blank space between lines
                thislocation[0] += LOCATION_LINE * 3

            locations.append(thislocation)
            locations += gettokenlocations(stackname)

        for incstackname in stack.get("location_include", []):
            locations += getstacklocations(incstackname)
        return locations

    def gettokenlocations(stackname):
        stack = getstackbyname(stackname)
        thislocation = stack["location"]
        locations = []
        for location in stack.get("token_locations", []):
            locations.append(
                [
                    location[0] + thislocation[0],
                    location[1] + thislocation[1],
                    location[2],
                    location[3],
                ]
            )
        for inctokens in stack.get("token_include", []):
            locations += gettokenlocations(inctokens)
        return locations

    leftside = True
    for txt in labels:
        o = rounded(W, H).set_modifier("")
        txto = label(txt, THICK, 0, 3.7)
        if leftside:
            o += rounded(W / 2, H + TAB_H)
            o += translate([W / 2, H - PAD, 0])(
                difference()(
                    cube([RAD, RAD, THICK]),
                    translate([RAD, RAD, -1])(cylinder(r=RAD, h=THICK + 2)),
                )
            )
            o += translate([W / 2 / 2, H + TAB_H / 2, THICK])(txto)
        else:
            o += translate([W / 2, 0, 0])(rounded(W / 2, H + TAB_H))
            o += translate([W / 2 - RAD * 2, H - PAD, 0])(
                difference()(
                    translate([RAD, 0, 0])(cube([RAD, RAD, THICK])),
                    translate([RAD, RAD, -1])(cylinder(r=RAD, h=THICK + 2)),
                )
            )
            o += translate([W / 2 / 2 + W / 2, H + TAB_H / 2, THICK])(txto)

        stack = getstackbyname(txt)
        locations = getstacklocations(txt)

        outline = 108 * LOCATION_SCALE
        loc_outline = roundedCube(
            [outline, outline, LOCATION_THICK], 6 * LOCATION_SCALE, True
        ) - translate([LOCATION_LINE, LOCATION_LINE, -1])(
            roundedCube(
                [outline - LOCATION_LINE * 2, outline - LOCATION_LINE * 2, THICK + 2],
                6 * LOCATION_SCALE - 0.8,
                True,
            ).set_modifier("")
        )
        loc_parts = []
        loc_cutouts = []
        # Append the actual location block
        for location in locations:
            x, y, height, width = location
            x, y, width, height = (
                x * LOCATION_SCALE,
                y * LOCATION_SCALE,
                width * LOCATION_SCALE,
                height * LOCATION_SCALE,
            )

            loc_parts.append(
                translate([x, y, 0])(
                    cube([width, height, LOCATION_THICK])
                    - translate([LOCATION_LINE, LOCATION_LINE, -1])(
                        cube(
                            [
                                width - LOCATION_LINE * 2,
                                height - LOCATION_LINE * 2,
                                THICK + 2,
                            ]
                        )
                    )
                )
            )
            loc_cutouts.append(
                translate([x - LOCATION_LINE, y - LOCATION_LINE, -1])(
                    cube(
                        [
                            width + LOCATION_LINE * 2,
                            height + LOCATION_LINE * 2,
                            THICK + 2,
                        ]
                    )
                )
            )
        loc = loc_outline - union()(loc_cutouts) + union()(loc_parts)
        o += translate([W / 2 - outline / 2, H / 2 - outline / 2, THICK])(
            loc
        ).set_modifier("")

        scad_render_to_file(o, f"divider_{txt}.scad", file_header=f"$fn = 30;\n")
        leftside = not leftside


def main():
    fn = 50
    # saveasscad(test_bracket(), "test-bracket")
    scad_render_to_file(monster_tray(), file_header=f"$fn = {fn};\n")
    generate_card_dividers()


def saveasscad(obj, desc, fn=50):
    # pfn = pathlib.Path(__file__)
    # outfn = pfn.parent / ("{}.scad".format(desc))
    scad_render_to_file(obj, file_header=f"$fn = {fn};\n")


SVG_OUTLINE = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg
   xmlns:dc="http://purl.org/dc/elements/1.1/"
   xmlns:cc="http://creativecommons.org/ns#"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
   xmlns:svg="http://www.w3.org/2000/svg"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
   xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
   sodipodi:docname="drawing.svg"
   inkscape:version="1.0 (4035a4f, 2020-05-01)"
   id="svg8"
   version="1.1"
   viewBox="0 0 210 297"
   height="297mm"
   width="210mm">
  <defs
     id="defs2" />
  <sodipodi:namedview
     inkscape:window-maximized="0"
     inkscape:window-y="23"
     inkscape:window-x="0"
     inkscape:window-height="1155"
     inkscape:window-width="1920"
     showgrid="false"
     inkscape:document-rotation="0"
     inkscape:current-layer="layer1"
     inkscape:document-units="mm"
     inkscape:cy="225.4884"
     inkscape:cx="254.3746"
     inkscape:zoom="4.8057137"
     inkscape:pageshadow="2"
     inkscape:pageopacity="0.0"
     borderopacity="1.0"
     bordercolor="#666666"
     pagecolor="#ffffff"
     id="base" />
  <metadata
     id="metadata5">
    <rdf:RDF>
      <cc:Work
         rdf:about="">
        <dc:format>image/svg+xml</dc:format>
        <dc:type
           rdf:resource="http://purl.org/dc/dcmitype/StillImage" />
        <dc:title></dc:title>
      </cc:Work>
    </rdf:RDF>
  </metadata>
  <g
     id="layer1"
     inkscape:groupmode="layer"
     inkscape:label="Layer 1">
{}
  </g>
</svg>
"""

SVG_TEMPLATE = """    <g
       transform="translate({posx},{posy})"
       id="g860">
      <rect
         style="fill:none;stroke:#000000;stroke-width:0.2;stroke-miterlimit:4;stroke-dasharray:none"
         id="rect{name}"
         width="{width}"
         height="{depth}"
         x="0"
         y="0" />
      <text
         style="font-style:normal;font-weight:normal;font-size:3.175px;line-height:1.25;font-family:sans-serif;fill:#000000;fill-opacity:1;stroke:none;stroke-width:0.264583"
         x="0"
         y="4"
         id="text{name}"><tspan
           sodipodi:role="line"
           id="tspan853"
           style="font-size:3.175px;stroke-width:0.264583">{text}</tspan></text>
    </g>"""

if __name__ == "__main__":
    main()
