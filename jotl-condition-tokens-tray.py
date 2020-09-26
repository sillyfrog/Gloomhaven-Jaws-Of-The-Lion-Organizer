#!/usr/bin/env python3
from solid import cube, use, scad_render_to_file, translate, rotate, cylinder

SHOW_EXTRAS = True

use("MCAD/boxes.scad")

FLOOR = 1
WALL = 1
TEXT_D = 0.4

TOKEN_W = 15
TOKEN_H = 2.25

TOKENS = {
    "Poison": 12,
    "Strengthen": 8,
    "Wound": 10,
    "Muddle": 10,
    "Immobilize": 8,
    "Stun": 6,
    "Disarm": 6,
}
TRAY_1 = ["Immobilize", "Stun", "Disarm"]
TOKEN_END = "Muddle"
END_TOKEN_BUF = 1.5

TOKEN_SLOT_W = 56
TOKEN_SLOT_D = 56
TOKEN_SLOT_H = 20
TOKEN_SLOT_CORNER_R = 2
MAX_TOKENS_STACK = 8

TOKEN_HOLDER_H = FLOOR + MAX_TOKENS_STACK * TOKEN_H

CUTOUT_MOVE = 3

for token in TOKENS.keys():
    use(f"images/{token.lower()}.scad")


def roundedCube(size, radius, sidesonly):
    return translate([size[0] / 2, size[1] / 2, size[2] / 2])(
        roundedBox(size, radius, sidesonly)
    )


def tokencutout(tokenname, cutout_top=False):

    cutout = globals()[tokenname.lower()](FLOOR).set_modifier("#")
    if cutout_top:
        y = TOKEN_W
        cutout = rotate([0, 0, 180])(cutout)
        cutout = translate([0, -CUTOUT_MOVE, 0])(cutout)
    else:
        y = 0
        cutout = translate([0, CUTOUT_MOVE, 0])(cutout)
    cutout = translate([TOKEN_W / 2, TOKEN_W / 2, -TEXT_D])(cutout)
    o = translate([0, 0, FLOOR])(
        roundedCube([TOKEN_W, TOKEN_W, TOKEN_HOLDER_H], 0.5, True) + cutout
    )
    o += translate([TOKEN_W / 2, y, -0.1])(
        cylinder(d=TOKEN_W * .7, h=TOKEN_HOLDER_H * 2)
    )
    return o


def fingertab():
    o = translate([0, WALL, TOKEN_SLOT_H / 2])(
        rotate([90, 0, 0])(cylinder(d=TOKEN_SLOT_H, h=WALL))
    )
    return o


def token_tray_1():
    # Just 3 token stacks
    o = roundedCube(
        [TOKEN_W * 3 + WALL * 4, TOKEN_W + WALL * 2, TOKEN_HOLDER_H],
        TOKEN_SLOT_CORNER_R,
        True,
    )
    offset = WALL
    for token in TRAY_1:
        o = o - translate([offset, WALL, 0])(tokencutout(token))
        offset += WALL + TOKEN_W
    o += translate([(TOKEN_W * 3 + WALL * 4) / 2, TOKEN_W + WALL, 0])(fingertab())
    return o


def token_tray_2():
    # The remaining 6 tokens, with slots for singles at the end
    total_width = TOKEN_W * 3 + WALL * 5 + TOKEN_H * END_TOKEN_BUF
    assert total_width <= TOKEN_SLOT_W
    o = roundedCube(
        [total_width, TOKEN_W * 2 + WALL * 3, TOKEN_HOLDER_H], TOKEN_SLOT_CORNER_R, True
    )
    # Get all of the stacks required
    tokens = []
    for tokenname, height in TOKENS.items():
        if tokenname in TRAY_1:
            continue
        if tokenname == TOKEN_END:
            pass
        elif height > MAX_TOKENS_STACK:
            tokens.append((tokenname))
        tokens.append((tokenname))

    # Make sure we have 6 stacks
    assert len(tokens) == 6

    offset = WALL
    for token in tokens[:3]:
        o = o - translate([offset, WALL, 0])(tokencutout(token))
        offset += WALL + TOKEN_W
    offset = WALL
    for token in tokens[3:]:
        o = o - translate([offset, WALL * 2 + TOKEN_W, 0])(
            tokencutout(token, cutout_top=True)
        )
        offset += WALL + TOKEN_W
    o += translate([(TOKEN_W * 3 + WALL * 4) / 2, TOKEN_W + WALL, 0])(fingertab())

    # End slots
    for y in (WALL, WALL * 2 + TOKEN_W):
        o -= translate(
            [total_width - TOKEN_H * END_TOKEN_BUF - WALL, y, TOKEN_HOLDER_H - TOKEN_W]
        )(cube([TOKEN_H * END_TOKEN_BUF, TOKEN_W, TOKEN_W * 2]))
        o -= translate(
            [total_width - TOKEN_H * END_TOKEN_BUF - WALL, y + TOKEN_W * .5 / 2, -0.1]
        )(
            roundedCube(
                [TOKEN_H * END_TOKEN_BUF + WALL * 2, TOKEN_W * .5, TOKEN_HOLDER_H * 2],
                1,
                True,
            )
        )
        d = TOKEN_W * .7
        o -= translate([total_width - WALL, y + TOKEN_W / 2, TOKEN_HOLDER_H])(
            rotate([0, 90, 0])(cylinder(d=d, h=WALL * 2))
        )
        # The cutouts for the end
        cutout = globals()[TOKEN_END.lower()](WALL)
        o -= translate(
            [
                total_width - WALL - TOKEN_H * END_TOKEN_BUF - TEXT_D,
                y + TOKEN_W / 2,
                TOKEN_HOLDER_H - TOKEN_W / 2 + CUTOUT_MOVE,
            ]
        )(rotate([0, 90, 0])(cutout))

    return o


def main():
    fn = 200
    scad_render_to_file(
        token_tray_1(), "condition_tokens_tray_1.scad", file_header=f"$fn = {fn};\n"
    )
    scad_render_to_file(
        token_tray_2(), "condition_tokens_tray_2.scad", file_header=f"$fn = {fn};\n"
    )


if __name__ == "__main__":
    main()
