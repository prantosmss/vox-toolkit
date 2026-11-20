import sys, urllib.parse
from common import *

API = "https://commons.wikimedia.org/w/api.php"
BAD_WORDS = ("logo", "signature", "autograph", "map", "flag", "coat of arms")


def find_photo(name, hint):
    q = name + (" " + hint if hint else "")
    params = urllib.parse.urlencode({
        "action": "query", "format": "json", "generator": "search",
        "gsrsearch": q, "gsrnamespace": 6, "gsrlimit": 10,
        "prop": "imageinfo", "iiprop": "url|extmetadata|size", "iiurlwidth": 2000,
    })
    pages = http_json(API + "?" + params).get("query", {}).get("pages", {})
    ranked = sorted(pages.values(), key=lambda p: p.get("index", 99))
    for page in ranked:
        title = page["title"].lower()
        info = page["imageinfo"][0]
        if not title.endswith((".jpg", ".jpeg", ".png")):
            continue
        if any(b in title for b in BAD_WORDS):
            continue
        if info.get("width", 0) < 400 or info.get("height", 0) < 400:
            continue
        meta = info.get("extmetadata", {})
        lic = meta.get("LicenseShortName", {}).get("value", "see source page")
        return info.get("thumburl") or info["url"], info["descriptionurl"], lic
    return None


def main():
    name = sys.argv[1]
    opts = parse_options(sys.argv[2:])
    result = find_photo(name, opts.get("hint", ""))
    if not result:
        print("NOT FOUND on Commons: " + name + ". Ask the user for a photo to use.", file=sys.stderr)
        sys.exit(1)
    link, page_url, lic = result
    raw = ASSETS / "people" / (slug(name) + "_raw.jpg")
    out = ASSETS / "people" / (slug(name) + ".png")
    download(link, raw)
    try:
        from rembg import remove
        from PIL import Image
        img = Image.open(raw).convert("RGBA")
        remove(img).save(out)
    except ImportError:
        print("rembg not installed. Run: python init.py", file=sys.stderr)
        sys.exit(2)
    log_asset(out, "wikimedia-commons", page_url, lic, name)
    print(out)


if __name__ == "__main__":
    main()
