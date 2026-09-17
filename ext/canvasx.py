# canvasx — move/spin/recolor drawn objects (ext <canvasx>)
# targets need names: create NAME { def NAME type="box" }
# tip: drive them from a jump loop, e.g.
#   .l  var 1 = var 1 + 2  var 8 = spinby("cube", 2, 1, 0)  jump .l

VERSION = "1.0"


def on_load(rt):
    def _get(name):
        o = rt.obj(str(name))
        if o is None:
            raise RuntimeError("no object named %r — create/draw one first" % str(name))
        return o

    def moveto(name, x, y):
        o = _get(name)
        o["px"] = float(x)
        o["py"] = float(y)
        rt.redraw()
        return x

    def spinby(name, dx=1.0, dy=0.0, dz=0.0):
        o = _get(name)
        o["rot"][0] += float(dx)
        o["rot"][1] += float(dy)
        o["rot"][2] += float(dz)
        rt.redraw()
        return o["rot"][0]

    def setcolor(name, r, g, b):
        o = _get(name)
        o["rgb"] = (max(0, min(255, int(r))),
                    max(0, min(255, int(g))),
                    max(0, min(255, int(b))))
        rt.redraw()
        return o["rgb"][0]

    def setsize(name, w, h, d=None):
        o = _get(name)
        o["w"] = float(w)
        o["h"] = float(h)
        if d is not None:
            o["d"] = float(d)
        rt.redraw()
        return o["w"]

    def drop(name):
        o = _get(name)
        rt.objects.remove(o)
        if o.get("name") in rt.objects_by_name:
            del rt.objects_by_name[o["name"]]
        rt.redraw()
        return 0

    rt.register_ext_func("moveto", moveto)
    rt.register_ext_func("spinby", spinby)
    rt.register_ext_func("setcolor", setcolor)
    rt.register_ext_func("setsize", setsize)
    rt.register_ext_func("objs", lambda: len(rt.objects))
    rt.register_ext_func("drop", drop)
