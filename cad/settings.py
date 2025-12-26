import cq_queryabolt as queryabolt

class Settings:
    # This is an inherited project, so lots of dimensions will
    # be put in as-is.
    topPlateLength = 240
    topPlateWidth = 200
    topPlateThickness = 6
    # Whether to create a LumenPnP-like hole pattern in the top plate
    topPlateHolePattern = True

    bottomPlateLength = 200
    bottomPlateWidth = bottomPlateLength
    bottomPlateThickness = 6

    basePlateLength = 257
    basePlateWidth = 162
    basePlateThickness = 2

    # Fits and design constraints
    pressFit = 0.05
    tightFit = 0.1
    fit = 0.2
    looseFit = 0.5
    wallThickness = 4

    # Bolts
    bolt = "M3"
    frameBolt = "M4"
    boltFit = fit

    # Bolt helpers
    boltR = (queryabolt.boltData(bolt)["diameter"] + boltFit) / 2
    frameBoltR = (queryabolt.boltData(frameBolt)["diameter"] + boltFit) / 2
    frameBoltHeadD = queryabolt.boltData(frameBolt, kind="socket_head")["head_diameter"] + looseFit

    # Motion system
    rodD = 8
    rotateBoltS = 75.450

    bearingD = 15
    bearingFit = tightFit
    bearingH = 24
    extD = 20

    # Others parameters
    compliance = 1
