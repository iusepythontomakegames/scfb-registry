# filex — file I/O extension (ext <filex>)
import os

VERSION = "1.0"


def on_load(rt):
    def read(path):
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()

    def write(path, text):
        with open(path, "w", encoding="utf-8") as f:
            f.write(str(text))
        return len(str(text))

    def append(path, text):
        with open(path, "a", encoding="utf-8") as f:
            f.write(str(text))
        return len(str(text))

    rt.register_ext_func("read", read)
    rt.register_ext_func("write", write)
    rt.register_ext_func("append", append)
    rt.register_ext_func("exists", lambda p: os.path.exists(str(p)))
    rt.register_ext_func("files", lambda p=".": ", ".join(sorted(os.listdir(str(p)))))
