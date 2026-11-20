import sys, urllib.parse
from common import *

API = "https://commons.wikimedia.org/w/api.php"


def main():
    query = sys.argv[1]
    search = urllib.parse.urlencode({
        "action": "query", "format": "json", "generator": "search",
        "gsrsearch": query + " logo", "gsrnamespace": 6, "gsrlimit": 5,
        "prop": "imageinfo", "iiprop": "url|extmetadata", "iiurlwidth": 1600,
    })
    pages = http_json(API + "?" + search).get("query", {}).get("pages", {})
    ranked = sorted(pages.values(), key=lambda p: p.get("index", 99))
    for page in ranked:
        info = page["imageinfo"][0]
        meta = info.get("extmetadata", {})
        license_name = meta.get("LicenseShortName", {}).get("value", "see source page")
        link = info.get("thumburl") or info["url"]
        ext = ".png"
        dest = ASSETS / "logos" / (slug(query) + ext)
        download(link, dest)
        log_asset(dest, "wikimedia-commons", info["descriptionurl"], license_name, query)
        print(dest)
        return
    print("NOT FOUND on Commons: " + query + ". Ask the user for the press-kit logo.", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()
