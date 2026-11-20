import sys, urllib.parse
from common import *


def pixabay(query, orientation):
    key = os.environ.get("PIXABAY_API_KEY")
    if not key:
        return None
    url = "https://pixabay.com/api/?" + urllib.parse.urlencode(
        {"key": key, "q": query, "per_page": 5, "image_type": "photo",
         "orientation": "horizontal" if orientation == "horizontal" else "vertical",
         "safesearch": "true"})
    hits = http_json(url).get("hits", [])
    if not hits:
        return None
    h = hits[0]
    return h.get("largeImageURL") or h["webformatURL"], h["pageURL"], "Pixabay Content License"


def pexels(query, orientation):
    key = os.environ.get("PEXELS_API_KEY")
    if not key:
        return None
    url = "https://api.pexels.com/v1/search?" + urllib.parse.urlencode(
        {"query": query, "per_page": 5, "orientation": "landscape" if orientation == "horizontal" else "portrait"})
    photos = http_json(url, {"Authorization": key}).get("photos", [])
    if not photos:
        return None
    p = photos[0]
    return p["src"]["large2x"], p["url"], "Pexels License"


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
            dest = ASSETS / "images" / (slug(query) + ".jpg")
            download(link, dest)
            log_asset(dest, name, page, lic, query)
            print(dest)
            return
    print("NOT FOUND: " + query, file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()
