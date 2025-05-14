import cadquery as cq
from ocp_vscode import *

top_d = 8
bot_d = 16
pin_d = 2.4
pin_h = 5
h = 14.4

def support():
    support = (cq.Workplane("front")
               .circle(bot_d / 2)
               .workplane(offset=h)
               .circle(top_d / 2)
               .loft(combine=True))
    support = support.faces("<Z").workplane().circle(pin_d / 2).extrude(pin_h)
    return support

support_ = support()
support_.export("board-support.step")
show_all()
