import math
import cadquery as cq
from settings import Settings

width = Settings.basePlateWidth
length = Settings.basePlateLength
thickness = Settings.basePlateThickness

carriageWidth = 27
carriageWidthS= width - 1* carriageWidth
carriageBoltWidthS = 17

carriageLength = 35
carriageLengthS= length - 1 * carriageLength
carriageBoltLengthS = 26.7

def basePlate():
    sketch = (cq.Sketch()
        .rect(length, width)
        .rarray(carriageLengthS, carriageWidthS, 2, 2)
        .rarray(carriageBoltLengthS, carriageBoltWidthS, 2, 2).circle(Settings.boltR, mode='s')
        .reset()
    )
    plate = cq.Workplane("XY").placeSketch(sketch).extrude(thickness)
    return plate

plate = basePlate()
plate.faces(">Z").workplane().section().export("output/base-plate-z.dxf")
plate.faces(">Y").workplane().section().export("output/base-plate-y.dxf")

if 'show_object' in globals():
    show_object(plate, name="basePlate")
