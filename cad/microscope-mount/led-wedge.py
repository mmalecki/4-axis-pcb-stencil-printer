import cadquery as cq
from ocp_vscode import *
from settings import Settings
from workplane import Workplane

wall_t =  Settings.wall_t * 3 / 5 # Not structural
v_slot_d = Settings.v_slot_d
led_strip_w = 8.5
zip_tie_d = 2

def led_wedge(length = 145):
    wedge = Workplane("YZ").lineTo(0, led_strip_w).lineTo(led_strip_w, led_strip_w).lineTo(0, 0).close().extrude(length)
    wedge = wedge.faces(">Z").workplane(centerOption="CenterOfBoundBox").slot2D(length + 4 * wall_t + 2 * Settings.frame_bolt_d, v_slot_d).extrude(wall_t)
    wedge = wedge.faces(">Z").workplane(centerOption="CenterOfBoundBox").tag("bottom").rarray(length + 2 * wall_t, 1, 2, 1).boltHole(Settings.frame_bolt, clearance = Settings.loose_fit)
    wedge = wedge.workplaneFromTagged("bottom").workplane(offset=-wall_t - v_slot_d).rarray(length + 2 * wall_t, 1, 2, 1).circle(1.5 * Settings.frame_bolt_d).cutBlind(v_slot_d)
    wedge = wedge.workplaneFromTagged("bottom").rarray(length / 2, led_strip_w + 2 * zip_tie_d, 2, 2).slot2D(length / 3, zip_tie_d).cutThruAll()
    wedge = wedge.edges("<<Z").chamfer(led_strip_w / 8)
    return wedge

def led_lens_mount():
    mount = Workplane("XY")
     
    return mount

led_wedge_ = led_wedge()
show_all()
led_wedge_.export("led-wedge.step")
