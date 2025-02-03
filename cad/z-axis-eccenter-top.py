import cadquery as cq
from settings import Settings
from workplane import Workplane

tightFit = Settings.tightFit
wallT, rodD = Settings.wallThickness, Settings.rodD
extD, bearingD = Settings.extD, Settings.bearingD
bearingH = Settings.bearingH

def backEccenterTop():
    ec = cq.importers.importStep("ECCF_TOP.step")
    tf = ec.faces(">Y").first().val().BoundingBox()
    w = (tf.zmax - tf.zmin)
    l = (tf.xmax- tf.xmin)
    t = (extD - w) / 2 + tightFit
    ec = ec.faces(">Y").workplane().move(0,  w/ 2 + t/2).rect(l, t).extrude(extD)
    ec = (ec.faces("<Z[1]").workplane(centerOption="CenterOfBoundBox").rarray((l - wallT) / 2, 1, 2, 1).hole(Settings.frameBoltR * 2))
    ec = ec.faces(">Y").edges(">X or <X").chamfer(extD / 4)
    return ec

ec = backEccenterTop()
ec.export("ECCB_TOP.step")

if 'show_object' in globals():
    show_object(ec)
