# netx — fetch text from a URL (ext <netx>)

VERSION = "1.0"


def on_load(rt):
    def fetch(url, limit=2000):
        import urllib.request
        req = urllib.request.Request(str(url), headers={"User-Agent": "SCFB-basic/1.2"})
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.read(int(limit)).decode("utf-8", errors="replace")

    rt.register_ext_func("fetch", fetch)
