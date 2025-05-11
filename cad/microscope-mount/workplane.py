import cq_queryabolt as queryabolt
import cadquery as cq

class Workplane(queryabolt.WorkplaneMixin, cq.Workplane):
    pass
