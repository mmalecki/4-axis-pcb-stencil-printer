import math
import cadquery as cq
from settings import Settings
from ocp_vscode import *

width = Settings.topPlateWidth
length = Settings.topPlateLength
thickness = Settings.topPlateThickness

boltR = Settings.boltR
rotateBoltS = Settings.rotateBoltS
boltS = 30

def topPlate():
    sketch = (cq.Sketch()
        .rect(length, width)
        .parray(rotateBoltS, 0, 360, 5)
        .circle(boltR, mode='s')
        .reset()
    )

    if Settings.topPlateHolePattern:
        lengthBolts = math.floor(length / boltS)
        widthBolts = math.floor(width / boltS)
        sketch = (sketch
            .rarray(boltS, boltS, lengthBolts, widthBolts).circle(boltR, mode='s')
            .reset()
            .rarray(boltS, boltS, lengthBolts - 1, widthBolts - 1).circle(boltR, mode='s')
        )

    plate = cq.Workplane("XY").placeSketch(sketch).extrude(thickness)
    return plate

plate = topPlate()
plate.faces(">Z").workplane().section().export("output/top-plate-z.dxf")
plate.faces(">Y").workplane().section().export("output/top-plate-y.dxf")

if __name__ == '__main__':
    top_plate = topPlate()
    show(top_plate)
