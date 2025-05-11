import cadquery as cq
from ocp_vscode import *
from cq_queryabolt import boltData, nutData
from settings import Settings
from workplane import Workplane

bearing_od = 14
bearing_t = 5
bearing_id = 5

scope_d = 50
bolt_d = boltData(Settings.frame_bolt)['diameter']
wall_t = Settings.wall_t
v_slot_d = Settings.v_slot_d
d = scope_d + 2 * wall_t

rod = "M5"
rod_nut = nutData(rod)
rod_nut_t  = rod_nut['thickness']
rod_nut_w = rod_nut['width']

holder_bolt = "M3"
holder_bolt_d = boltData(holder_bolt)['diameter']

dovetail_h = 50
dovetail_w = 3 * wall_t
dovetail_t = rod_nut_w + wall_t
dovetail_neck_l = 20
dovetail_neck_w = 2 * wall_t
dovetail_neck_t = rod_nut_t + 2 * wall_t

running_fit = 0.121

dovetail_top_bolt = "M2"
heatset_d = 3.2
heatset_l = 4
heatset_wall_t = 1.3

dovetail_wall_t = heatset_d + heatset_wall_t * 2

shape = (cq.Sketch()
         .rect(d, d)
         .rarray(scope_d, 1, 2, 1).slot(d + v_slot_d * 2, Settings.v_slot_d / 2, angle=90)
         .reset().circle(scope_d / 2, mode='s'))

dovetail_shape = (cq.Sketch().trapezoid(dovetail_w, dovetail_t, 135))
dovetail_outer_shape = dovetail_shape.copy().wires().offset(dovetail_wall_t)

holder_bolt_offset = 5.5

slider_shape = (dovetail_shape.copy().wires().offset(-running_fit, mode='r')
                .push([(0, -dovetail_t / 2 - dovetail_neck_l / 2 + running_fit)])
                .rect(dovetail_neck_w - 2*running_fit, dovetail_neck_l)
                .push([(0, -dovetail_neck_l - scope_d / 2 - wall_t)])
                .circle(scope_d / 2 + wall_t)
                .circle(scope_d / 2, mode='s').reset())

def top():
    top = Workplane("XY")
    top = top.placeSketch(dovetail_outer_shape).extrude(bearing_t)

    # Top mount
    top = top.faces(">Z").workplane(centerOption="CenterOfBoundBox").tag("top").center(0, dovetail_t / 2).rarray(dovetail_w + 2 * dovetail_t + dovetail_wall_t , 1, 2, 1).boltHole(dovetail_top_bolt, clearance=Settings.fit)
    top = top.workplaneFromTagged("top").hole(bearing_od, bearing_t)

    top = top.edges(">Z and (not %Circle)").chamfer(bearing_t / 4)

    return top

def mount():
    # Create the dovetail
    mount = Workplane("XY")
    dovetail_wall_t = heatset_d + heatset_wall_t * 2
    mount = mount.placeSketch(dovetail_shape.copy().wires().offset(dovetail_wall_t)).extrude(dovetail_h)
    mount = mount.faces(">Z").workplane().placeSketch(dovetail_shape).cutThruAll()
    mount = mount.faces("<Y").workplane(centerOption="CenterOfBoundBox").rect(dovetail_neck_w, dovetail_h).cutBlind(until="next")

    # Top mount
    mount = mount.faces(">Z").workplane(centerOption="CenterOfBoundBox").tag("top").center(0, dovetail_t / 2).rarray(dovetail_w + 2 * dovetail_t + dovetail_wall_t , 1, 2, 1).hole(heatset_d, heatset_l)

    # Bottom mount
    bottom_h = bearing_t + wall_t / 2 # Mostly support for the dovetail bottom
    bb = mount.val().BoundingBox()
    mount = mount.faces("<Z").workplane(centerOption="CenterOfBoundBox").slot2D(bb.xlen + 2 * v_slot_d, dovetail_t + 2 * dovetail_wall_t).extrude(bottom_h)

    mount = mount.faces(">Z[1]").edges().fillet(0.4)

    mount = mount.faces("<Z").workplane(centerOption="CenterOfBoundBox").tag("bottom").hole(bearing_od, bearing_t)
    mount = mount.faces("<Z").workplane(centerOption="CenterOfBoundBox").tag("bottom").hole(bearing_id + Settings.loose_fit)
    mount = mount.faces("<Z[2]").workplane().rarray(bb.xlen + v_slot_d, 1, 2, 1).cboreBoltHole(Settings.frame_bolt, clearance=Settings.fit, cboreDepth=bottom_h - wall_t)

    return mount

def slider():
    slider = Workplane("XY")
    slider = slider.placeSketch(slider_shape).extrude(dovetail_neck_t)
    slider = slider.faces(">Z").workplane(offset=-dovetail_neck_t / 2 - rod_nut_t / 2).nutcatchSidecut(rod)
    slider = slider.faces(">Z").workplane().boltHole(rod, clearance = Settings.loose_fit)
    slider = slider.faces(">X[1] or <X[1]").edges("<<Y").fillet(dovetail_neck_w)

    slider = slider.workplane().move(0, 0).transformed((90, 0, 0), offset=(0, -d - dovetail_neck_l - dovetail_t / 2 + wall_t, dovetail_neck_t / 2 - holder_bolt_offset)).slot2D(d * 3 / 4, holder_bolt_d + Settings.loose_fit).cutBlind(-d / 2)

    return slider

def joiner():
    joiner = Workplane("XY")
    joiner_l = d * 2 # Sometimes mechanical engineering isn't exact mechanical engineering
    joiner = joiner.slot2D(joiner_l, bolt_d + 2 * wall_t, 90).slot2D(joiner_l - 2 * wall_t, bolt_d + Settings.loose_fit, 90).extrude(wall_t)
    return joiner

top_ = top()
mount_ = mount()
slider_ = slider()
joiner_ = joiner()
show(mount_, slider_, top_.translate((0, 0, dovetail_h)), joiner_.translate((50, -40, 0)))
top_.export("microscope-mount-top.step")
mount_.export("microscope-mount.step")
slider_.export("microscope-mount-holder.step")
joiner_.export("microscope-mount-joiner.step")
