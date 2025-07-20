from build123d import *
from ocp_vscode import *
from settings import Settings
from workplane import Workplane

scope_d = 46 + 2 * Settings.loose_fit # Bottom lens diameter is smaller than 
wall_t = Settings.wall_t
od = scope_d + 2 * wall_t

led_strip_w = 8.5
led_strip_l = 50

heatsert_d = 4
heatsert_l = 4
heatsert_wall_t = 1.6
bolt_d = 3

with BuildPart() as mount:
    with BuildSketch(Plane.XY):
        Circle(od / 2)
        Circle(scope_d / 2, mode=Mode.SUBTRACT)
    extrude(amount=wall_t)

    with BuildSketch(Plane.XY):
        with PolarLocations(od / 2, 3):
            with Locations(((led_strip_w - wall_t) / 4, 0)):
                Rectangle(led_strip_w, led_strip_l)
    extrude(amount=wall_t * 2 / 3)
    chamfer(mount.edges(Select.LAST).group_by(Axis.Z)[1:3], length=wall_t / 4)

    heatsert_holder_t = heatsert_d + 2 * heatsert_wall_t

    with BuildSketch():
        with Locations((od/ 2, 0, 0)):
                Rectangle(2 * wall_t, heatsert_holder_t)
    extrude(amount=wall_t + heatsert_holder_t)

    with Locations(mount.faces(Select.LAST).sort_by(Axis.X)[3]):
        Hole(heatsert_d / 2, heatsert_l)

    with Locations(mount.faces(Select.LAST).sort_by(Axis.X)[-1]):
        Hole((bolt_d + Settings.fit) / 2)

    chamfer(mount.edges().group_by(Axis.Z)[-1], length = wall_t / 6)
    chamfer(mount.edges().group_by(Axis.Z)[-5], length = wall_t / 6)

export_step(mount.part, "lens-led-mount.step")
show_all()
