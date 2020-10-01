#!/usr/bin/env python3
from solid import cube, use, scad_render_to_file, translate, rotate, cylinder, hole
from solid.objects import union
from solid.utils import up, down

SHOW_EXTRAS = True

use("MCAD/boxes.scad")

FLOOR = 1
WALL = 1
TEXT_D = 0.4

HP_1_D = 14.1
HP_3_D = 18.2
HP_10_D = 23.3

TRAY_W = 58
TRAY_D = 42
TRAY_H = 20


def roundedCube(size, radius, sidesonly):
    return translate([size[0] / 2, size[1] / 2, size[2] / 2])(
        roundedBox(size, radius, sidesonly)
    )


def makestack(dia):
    stack = union()(
        cylinder(d=dia + WALL * 2, h=TRAY_H - FLOOR)
        - up(FLOOR)(cylinder(d=dia, h=TRAY_H))
    )
    hole_pcg = 0.7
    stack -= hole()(down(1)(cylinder(d=dia * hole_pcg, h=TRAY_H)))
    stack -= hole()(
        translate([-dia / 2 - WALL, -dia / 2 * hole_pcg, -1])(
            cube([dia / 2 + WALL, dia * hole_pcg, TRAY_H * 3])
        )
    )

    return stack


def hitpoint_tray_1():
    # 4x single stacks
    stack = makestack(HP_1_D)

    loc1 = [HP_1_D / 2 + WALL, TRAY_W - (HP_1_D / 2)]
    loc2 = [TRAY_D - (HP_1_D / 2 + WALL), TRAY_W - (HP_1_D / 2)]
    loc3 = [loc2[0] + WALL, loc2[1] - (HP_1_D + WALL)]
    loc4 = [(loc1[0] + loc3[0]) / 2 - 0.1, (loc1[1] + loc3[1]) / 2 - 0.1]
    o = translate(loc1)(rotate([0, 0, -90])(stack))
    o += translate([loc2[0] + WALL / 2, loc2[1]])(rotate([0, 0, 180])(stack))
    o += translate(loc3)(rotate([0, 0, 180])(stack))
    o += translate(loc4)(rotate([0, 0, 50])(stack))

    return o


def hitpoint_tray_2():
    stack3 = makestack(HP_3_D)
    o = translate([HP_3_D / 2, HP_3_D / 2 + WALL])(stack3)
    o += translate([HP_3_D / 2, HP_3_D / 2 + WALL + HP_3_D + WALL])(stack3)

    stack10 = makestack(HP_10_D)
    o += translate([TRAY_D - (HP_10_D / 2), HP_10_D / 2 + WALL + 2.09])(
        rotate([0, 0, 180])(stack10)
    )

    return o


def main():
    fn = 200
    scad_render_to_file(
        hitpoint_tray_1(), "hit_points_tokens_tray_1.scad", file_header=f"$fn = {fn};\n"
    )
    scad_render_to_file(
        hitpoint_tray_2(), "hit_points_tokens_tray_2.scad", file_header=f"$fn = {fn};\n"
    )


if __name__ == "__main__":
    main()
