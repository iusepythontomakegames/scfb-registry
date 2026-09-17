# mathx — math extension (ext <mathx>)
import math
import random

VERSION = "1.0"


def on_load(rt):
    rt.entities["pi"] = math.pi
    rt.entities["tau"] = math.tau
    rt.register_ext_func("rnd", lambda a=0, b=100: random.randint(int(a), int(b)))
    rt.register_ext_func("sqrt", lambda x: math.sqrt(x) if x >= 0 else 0.0)
    rt.register_ext_func("sin", lambda d: round(math.sin(math.radians(d)), 6))
    rt.register_ext_func("cos", lambda d: round(math.cos(math.radians(d)), 6))
    rt.register_ext_func("tan", lambda d: round(math.tan(math.radians(d)), 6))
    rt.register_ext_func("floor", lambda x: math.floor(float(x)))
    rt.register_ext_func("ceil", lambda x: math.ceil(float(x)))
    rt.register_ext_func("round", lambda x, n=0: round(float(x), int(n)))
    rt.register_ext_func("abs", lambda x: abs(x))
    rt.register_ext_func("pow", lambda a, b: float(a) ** float(b))
    rt.register_ext_func("min", lambda *a: min(a))
    rt.register_ext_func("max", lambda *a: max(a))
