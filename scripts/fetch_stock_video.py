import sys, urllib.parse
from common import *


def pixabay(query, orientation):
    key = os.environ.get("PIXABAY_API_KEY")
    if not key:
        return None
    url = "https://pixabay.com/api/videos/?" + urllib.parse.urlencode(
        {"key": key, "q": query, "per_page": 5, "safesearch": "true"})
    hits = http_json(url).get("hits", [])
    if not hits:
        return None
    h = hits[0]
    v = h["videos"].get("large") or h["videos"]["medium"]
    return v["url"], h["pageURL"], "Pixabay Content License"


def pexels(query, orientation):
    key = os.environ.get("PEXELS_API_KEY")
    if not key:
        return None
    url = "https://api.pexels.com/videos/search?" + urllib.parse.urlencode(
        {"query": query, "per_page": 5, "orientation": "landscape" if orientation == "horizontal" else "portrait"})
    vids = http_json(url, {"Authorization": key}).get("videos", [])
    if not vids:
        return None
    files = sorted(vids[0]["video_files"], key=lambda f: f.get("width", 0), reverse=True)
    hd = [f for f in files if f.get("width", 0) <= 1920] or files
    return hd[0]["link"], vids[0]["url"], "Pexels License"


def main():
    load_env()
    query = sys.argv[1]
    opts = parse_options(sys.argv[2:])
    orientation = opts.get("orientation", "horizontal")
    order = [opts["source"]] if "source" in opts else ["pixabay", "pexels"]
    for name in order:
        result = {"pixabay": pixabay, "pexels": pexels}[name](query, orientation)
        if result:
            link, page, lic = result
            dest = ASSETS / "video" / (slug(query) + ".mp4")
            download(link, dest)
            log_asset(dest, name, page, lic, query)
            print(dest)
            return
    print("NOT FOUND: " + query, file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()
