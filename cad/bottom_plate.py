import math
import cadquery as cq
from settings import Settings
from build123d import *
from ocp_vscode import *

width = Settings.bottomPlateWidth
length = Settings.bottomPlateLength
thickness = Settings.bottomPlateThickness

access_hole_d = 10

boltR = Settings.boltR
boltS = 30

mountD = 122

def bottom_plate():
    with BuildPart() as part:
        with BuildSketch():
            Rectangle(length, width)

            # Access holes
            with PolarLocations(Settings.rotateBoltS, 5):
                Circle(access_hole_d / 2, mode=Mode.SUBTRACT)

            # Mounting (tapped) holes
            with PolarLocations(mountD / 2, 4):
                Circle(boltR, mode=Mode.SUBTRACT)

            # Bearing mounts
            with GridLocations(67.5 * 2,61 * 2, 2,2):
                with GridLocations(29, 18, 2, 2):
                    Circle(boltR, mode=Mode.SUBTRACT)

            # Alpha-axis driven rod mount
            with Locations((-83.55, 0)):
                with GridLocations(0, 180, 2, 2):
                    with GridLocations(20.3, 12, 2, 2):
                        Circle(boltR, mode=Mode.SUBTRACT)

            # Central tapped hole (unused at the moment)
            Circle(boltR, mode=Mode.SUBTRACT)

        extrude(amount=thickness)
    return part

if __name__ == '__main__':
    bottom_plate_ = bottom_plate()
    show(bottom_plate_)
