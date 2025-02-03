import math
import cadquery as cq
from settings import Settings
from workplane import Workplane

fit, bearingFit = Settings.fit, Settings.bearingFit
wallT, rodD = Settings.wallThickness, Settings.rodD
extD, bearingD = Settings.extD, Settings.bearingD
bearingH = Settings.bearingH

bearingOffY = (bearingD + bearingFit + wallT) / 2

# Technically this only needs:
# frame bolt head | wall | bearing | wall | frame bolt head
# But we're throwing in a loose wall there for aesthetic reasons,
# otherwise the mount sticks out of the aluminium extrusion.
bearingMountW = bearingD + wallT * 3 + 2 * Settings.frameBoltHeadD 

def rodMount():
    bD = bearingD + bearingFit

    rD = rodD + fit
    rW = rD / 2+ wallT

    w = bearingMountW
    bearingWallT = (bD - rD) / 2 + wallT

    rm = (Workplane("XY")
          .sketch()
          .circle(rW)
          .push([(0, bearingOffY- (bearingWallT - wallT) / 2)])
          .rect(w, bearingWallT)
          .push([(w / 4, rD / 4)])
          .rect(w / 2, rD)
          .reset()
          .circle(rD / 2, mode='s')
          .push([(w / 4, rD / 4)])
          .rect(w / 2, Settings.compliance, mode='s')
          .reset()
          .finalize()
          .extrude(extD + wallT)
    )
    rm = (rm.faces(">Y[3]").workplane(centerOption="CenterOfBoundBox")
          .move(0, wallT / 2)
          .cboreBoltHole(Settings.frameBolt, clearance=Settings.boltFit)
          )
    rm = (rm.faces(">Y[0]").workplane(centerOption="CenterOfBoundBox")
          .move(0, wallT / 2)
          .cboreBoltHole(Settings.frameBolt, clearance=Settings.boltFit, cboreDepth = 0.2)
          )
    return (rm, w, bearingWallT)

def bracket():
    w = extD * 3
    br = (Workplane("XY")
          .sketch()
          .rect(extD, w)
          .push([(w / 2 - extD / 2, -w / 2 + extD / 2)])
          .rect(w, extD)
          .reset()
          .push([(extD, 0)])
          .rarray(extD, extD, 3, 3)
          .circle(Settings.frameBoltR, mode='s')
          .finalize()
          .extrude(wallT)
          )

    (rm, rmW, rmT) = rodMount()

    br = br + rm.translate((rmW / 2 - extD / 2, -extD * 1.5 - (bearingD + bearingFit + 2 * wallT) / 2 ))

    brace = (cq.Workplane("XY")
            .rect(wallT / 2, 2 * rmT)
            .extrude(rmT * 2).translate((-extD / 2 - wallT / 4, -extD * 1.5))
            .edges(">Y and >Z").chamfer(rmT)
             )
    br = br + brace

    br = (br.faces(">>Z[1]").edges("|Z").chamfer(wallT / 4))
    br = br.faces("<Z or >Z").edges("not %Circle").chamfer(wallT / 8)
    br = (br.faces(">Z[2]").edges(">X").chamfer(wallT / 10))
    br = (br.faces("<X").chamfer(wallT / 8))

    return br

def bearingMount():
    bD = bearingD + bearingFit

    rm = (Workplane("XY")
          .sketch()
          .circle(bD / 2 + wallT)
          .circle(bD / 2, mode='s')
          .push([(0, bearingOffY)])
          .rect(bearingMountW + fit, wallT)
          .finalize()
          .extrude(bearingH)
    )
    extOff = (bearingH - extD) / 2
    rm = (rm.faces(">Y[0]").workplane(centerOption="CenterOfBoundBox")
          .center(0, -extOff)
          .rarray((bearingMountW - Settings.frameBoltHeadD - wallT / 2), 1, 2, 1)
          .cboreBoltHole(Settings.frameBolt, clearance=Settings.boltFit, cboreDepth=0.2)
          )

    rm = rm.edges(">Z and |Y and (>X or <X)").chamfer(wallT * 2)
    rm = (rm.edges("|Z").edges("<<Y[1] and (not (>>X or <<X))").fillet(wallT / 2))
    rm = rm.edges(">Z or <Z or (>>X and >>Y) or (<<X and >>Y)").chamfer(wallT / 8)

    return (rm, bearingMountW)

br = bracket()
br.export("TOP_Z_AXIS_BRACKET.step")
(bm, _) = bearingMount()
bm.export("TOP_Z_AXIS_BEARING_MOUNT.step")

if 'show_object' in globals():
    show_object(br)
    show_object(bm.translate((0, 0, bearingH)), name="bearingMount")
