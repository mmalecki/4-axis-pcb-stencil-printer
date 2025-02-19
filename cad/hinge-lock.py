import cadquery as cq
from settings import Settings
from workplane import Workplane
import cq_queryabolt as queryabolt

from ocp_vscode import *

fit, tightFit, looseFit = Settings.fit, Settings.tightFit, Settings.looseFit
wallT = Settings.wallThickness
extD = Settings.extD
frameBolt = Settings.frameBolt
bolt = Settings.bolt

lockBolt = bolt

frameBoltD = queryabolt.boltData(frameBolt)["diameter"]
nutD = queryabolt.nutData(frameBolt)["width"]
nutH = queryabolt.nutData(frameBolt)["thickness"]

def hingeLockBack():
    h = extD + tightFit + 2 * wallT
    boltL = frameBoltD * 2 + 4 * wallT
    l = boltL + 2 * wallT + nutD
    lck = Workplane("XY").rect(l, extD - tightFit).extrude(h)
    lck = lck.faces("<X").workplane(centerOption="CenterOfBoundBox").rect(extD + tightFit, extD + tightFit).cutBlind(-boltL)
    lck = lck.faces(">Z").workplane(centerOption="CenterOfBoundBox").tag("top").center(-(l - boltL) / 2, 0).rarray(boltL / 2, 1, 2, 1).boltHole(frameBolt, clearance=Settings.boltFit)
    lck = lck.faces(">Y").workplane(centerOption="CenterOfBoundBox").tag("nut").move(-boltL / 2, 0).boltHole(lockBolt, clearance=looseFit)
    lck = lck.workplaneFromTagged("nut").workplane(-extD + wallT).move(-boltL / 2, 0).nutcatchSidecut(lockBolt, heightClearance=Settings.boltFit)
    lck = lck.edges(">Y and >X").chamfer(extD / 4)
    lck = lck.edges("<X and |Z").chamfer(extD / 8)
    lck = lck.faces(">Z or <Z ").edges("not %Circle").chamfer(wallT / 4)
    lck = lck.faces(">X ").edges("<Y").chamfer(wallT / 4)
    return lck

def hingeLockFront():
    boltL = frameBoltD * 2 + 5 * wallT 
    l = boltL + extD
    lck = Workplane("XY").rect(wallT, l).extrude(extD)
    lck = lck.faces(">X").workplane(centerOption="CenterOfBoundBox").move((l - extD) / 2, 0).rect(extD,extD,  ).extrude(1 * wallT + nutD)
    lck = lck.faces(">Y[1]").workplane(centerOption="CenterOfBoundBox").move(-wallT / 2, 0).cboreBoltHole(lockBolt, clearance=looseFit, cboreDepth=extD - wallT, headClearance=looseFit)
    lck = lck.faces(">X[1]").workplane(centerOption="CenterOfBoundBox").center(-wallT / 2, 0).rarray(boltL / 2, 1, 2, 1).cboreBoltHole(frameBolt, clearance=Settings.boltFit, cboreDepth=0.2)
    lck = lck.faces(">Y[1]").edges("|Z and >Y").fillet(wallT / 2)
    lck = lck.faces(">Z or <Z or >Y or <Y").edges("not %Circle").chamfer(wallT / 4)
    return lck


back = hingeLockBack()
back.export("TOP_HINGE_LOCK_BACK.step")

front = hingeLockFront()
front.export("TOP_HINGE_LOCK_FRONT.step")

if 'show' in globals():
    # show(back)
    show(front)
