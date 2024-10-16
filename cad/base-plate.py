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
    sketch.export("output/base-plate.dxf")
    plate = cq.Workplane("XY").placeSketch(sketch).extrude(thickness)
    return plate

show_object(basePlate(), name="basePlate")
