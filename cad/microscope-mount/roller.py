import cadquery as cq
from ocp_vscode import *
from cq_queryabolt import nutData
from settings import Settings
from workplane import Workplane

wall_t =  Settings.wall_t
bearing_bolt = "M8"
bearing_od = 22
wheel_t = 3
bearing_t = 7
wheel_od = bearing_od + 2 * wheel_t

nut = nutData(bearing_bolt, kind="hexagon_lock")
nut_l = nut['thickness']
nut_w = nut['width']
print(nut)

def wheel():
    wheel = Workplane("YZ")
    wheel = wheel.circle(wheel_od  / 2).circle(bearing_od / 2).extrude(bearing_t)
    wheel = wheel.edges(cq.selectors.RadiusNthSelector(1)).chamfer(bearing_t / 8)
    return wheel

def roller_mount():
    mount_l = Settings.v_slot_d * 2
    mount = Workplane("XY").rect(mount_l + nut_l + wall_t, Settings.v_slot_d).extrude(wall_t)
    nut_block_l = nut_l + wall_t
    nut_block_h = wheel_od / 2 + nut_w / 2 + wall_t + Settings.loose_fit
    mount = mount.faces("<Z").workplane().move(mount_l / 2, 0).rect(nut_block_l, Settings.v_slot_d).extrude(nut_block_h)
    mount = (mount.faces("<X[1]").workplane(centerOption="CenterOfBoundBox")
             .center(0, -wall_t / 2 - ((wheel_od + Settings.loose_fit) - nut_block_h) / 2)
             .tag("nut")
             .nutcatchParallel(bearing_bolt))

    mount = mount.workplaneFromTagged("nut").boltHole(bearing_bolt)

    mount = mount.faces(">Z[1]").workplane(centerOption="CenterOfBoundBox").rarray(Settings.v_slot_d, 1, 2, 1).cboreBoltHole(Settings.frame_bolt, clearance=Settings.loose_fit, cboreDepth=0.1)
    
    mount = mount.faces(">Z[1]").edges(">X").chamfer(wall_t)
    mount = mount.edges("<Z and (>>Y or <<Y)").chamfer(Settings.v_slot_d / 4)
    mount = mount.edges("not %Circle").chamfer(wall_t / 8)

    return mount

wheel_ = wheel()
wheel_.export("wheel.step")
mount = roller_mount()
mount.export("roller-mount.step")
show_all()
