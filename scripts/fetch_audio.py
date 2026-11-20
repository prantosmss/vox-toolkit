import sys, urllib.parse
from common import *

SEARCH = "https://freesound.org/apiv2/search/text/"
OK_LICENSES = ("creativecommons.org/publicdomain/zero", "creativecommons.org/licenses/by/")


def main():
    load_env()
    kind = sys.argv[1]
    query = sys.argv[2]
    key = os.environ.get("FREESOUND_API_KEY")
    if kind != "sfx":
        print("Only 'sfx' is supported. Music: ask the user for tracks in assets/music/.", file=sys.stderr)
        sys.exit(1)
    if not key:
        print("Missing FREESOUND_API_KEY in .env", file=sys.stderr)
        sys.exit(2)
    params = urllib.parse.urlencode({
        "query": query, "page_size": 15, "token": key,
        "fields": "id,name,username,license,duration,previews,url",
        "filter": "duration:[0.2 TO 6]",
    })
    results = http_json(SEARCH + "?" + params).get("results", [])
    for r in results:
        lic = r.get("license", "")
        if not any(ok in lic for ok in OK_LICENSES):
            continue
        link = r["previews"].get("preview-hq-mp3")
        if not link:
            continue
        dest = ASSETS / "sfx" / (slug(query) + ".mp3")
        download(link, dest)
        credit = "CC0" if "zero" in lic else "CC BY, credit: " + r["username"]
        log_asset(dest, "freesound", r["url"], credit, query)
        print(dest)
        return
    print("NOT FOUND: " + query, file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()
