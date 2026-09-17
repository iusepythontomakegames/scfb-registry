# textx — text helpers (ext <textx>)

VERSION = "1.0"


def on_load(rt):
    def banner(s):
        t = str(s)
        rt.out("=" * (len(t) + 4), "out")
        rt.out("  " + t, "out")
        rt.out("=" * (len(t) + 4), "out")
        return t

    rt.register_ext_func("upper", lambda s: str(s).upper())
    rt.register_ext_func("lower", lambda s: str(s).lower())
    rt.register_ext_func("length", lambda s: len(str(s)))
    rt.register_ext_func("part", lambda s, a, b: str(s)[int(a):int(b)])
    rt.register_ext_func("rev", lambda s: str(s)[::-1])
    rt.register_ext_func("rep", lambda s, n: str(s) * max(0, min(int(n), 200)))
    rt.register_ext_func("banner", banner)
