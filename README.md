# scfb-registry

The package registry for **SCFB basic** (SCFB Studio). Managed with `spm`,
the SCFB package manager — no manual downloads needed.

## From your terminal (PowerShell or Command Prompt)

    py scfb_studio.py spm available            list everything in this registry
    py scfb_studio.py spm install all          install every library and extension
    py scfb_studio.py spm install math mathx   install specific packages
    py scfb_studio.py spm update all           refresh installed packages
    py scfb_studio.py spm remove math          uninstall
    py scfb_studio.py spm list                 show what's installed

Packages install to `%LOCALAPPDATA%\scfb\libs` and `%LOCALAPPDATA%\scfb\ext`.

## Then in SCFB basic

    lib <math>      // loads an installed LIBRARY (SCFB basic source)
    ext <mathx>     // loads an installed EXTENSION (Python plugin)

    var 1 = 6
    call sq()
    print(var 9)         // 36
    print(rnd(1, 100))   // extension function call

## What's the difference?

- **Library** (`.scb`): pure SCFB basic — functions, checkpoints, entities.
  Its top-level `def`s/cvars run on load **up to its first checkpoint**; code after
  a checkpoint (like `anim`'s spin loops) only runs when you `jump` to it.
  Its functions are called with `call name()`.
- **Extension** (`.py`): a Python plugin with an `on_load(rt)` hook. It registers
  functions callable *inside expressions*: `print(rnd(1, 100))`, `var 8 = spinby("cube", 2, 1, 0)`.

## Conventions used by the libraries

- math / calc: inputs in `var 1` (and `var 2`), result in `var 9`
- color: sets `var 1, var 2, var 3` (RGB — used by draws automatically)
- shapes: `var 4` = size, `var 5`, `var 6` = x, y position
- anim: angles in `var 6, 7, 8`; jump `.spin3d` / `.spin2d`, Stop halts

## Writing your own extension

```python
# myext.py — install as ext/myext.py, then: ext <myext>
def on_load(rt):
    rt.register_ext_func("shout", lambda s: str(s).upper() + "!!!")
    rt.entities["mydata"] = 42          # printable via print(mydata)
    # runtime API: rt.out(text, tone), rt.obj(name), rt.redraw(),
    #              rt.objects, rt.entities, rt.vars
```
