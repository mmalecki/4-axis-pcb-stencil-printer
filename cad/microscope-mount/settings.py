from cq_queryabolt import boltData

class Settings:
    tight_fit = 0.1
    fit = 0.2
    loose_fit = 0.5

    bolt_fit = fit

    v_slot_d = 20
    wall_t = 4

    frame_bolt = "M5"
    frame_bolt_d = boltData(frame_bolt)['diameter']

    scope_d = 50
