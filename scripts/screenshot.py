import shutil, subprocess, sys
from common import *

COOKIE_BUTTONS = ["Accept all", "Accept", "I agree", "Agree", "Got it", "Allow all", "Close"]


def with_playwright(url, dest, opts):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1920, "height": 1080}, device_scale_factor=2)
        page.goto(url, wait_until="networkidle", timeout=60000)
        for label in COOKIE_BUTTONS:
            try:
                page.get_by_role("button", name=label).first.click(timeout=1000)
                break
            except Exception:
                pass
        hl = opts.get("highlight")
        if hl:
            page.evaluate(
                """(t) => {
                    const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
                    let n;
                    while ((n = w.nextNode())) {
                        const i = n.nodeValue.indexOf(t);
                        if (i >= 0) {
                            const r = document.createRange();
                            r.setStart(n, i); r.setEnd(n, i + t.length);
                            const m = document.createElement('mark');
                            m.style.background = '#ffe600';
                            r.surroundContents(m);
                            m.scrollIntoView({block: 'center'});
                            break;
                        }
                    }
                }""", hl)
        sel = opts.get("selector")
        if sel:
            page.locator(sel).first.screenshot(path=str(dest))
        else:
            page.screenshot(path=str(dest), full_page=opts.get("fullpage") == "true")
        browser.close()


def with_headless_chrome(url, dest):
    chrome = (shutil.which("google-chrome") or shutil.which("chrome") or shutil.which("chromium")
              or "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
    subprocess.run([chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    "--window-size=1920,1080", "--virtual-time-budget=8000",
                    f"--screenshot={dest}", url], check=True)


def main():
    url = sys.argv[1]
    opts = parse_options(sys.argv[2:])
    parsed = urllib.parse.urlparse(url)
    dest = ASSETS / "screenshots" / (slug(parsed.netloc + "-" + parsed.path) + ".png")
    dest.parent.mkdir(parents=True, exist_ok=True)
    try:
        with_playwright(url, dest, opts)
    except ImportError:
        with_headless_chrome(url, str(dest))
    log_asset(dest, "screenshot", url, "Screenshot for commentary; check fair use", url)
    print(dest)


if __name__ == "__main__":
    main()
