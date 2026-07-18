#!/usr/bin/env python3
"""
Sitemap & SEO Auto-Generator untuk VeniceLab
Cara pakai:  python3 generate_sitemap.py
Jalanin setiap kali nambah halaman baru, atau pasang pre-commit hook.
"""

import os, datetime
from xml.sax.saxutils import escape

BASE = os.path.dirname(os.path.abspath(__file__))
DOMAIN = "https://venicelab.web.id"
TODAY = datetime.date.today().isoformat()

# ── Konfigurasi prioritas ──
PRIORITY = {
    "/index.html": 1.0,
    "/blog/index.html": 0.9,
}
FREQ = {
    "/index.html": "weekly",
    "/blog/index.html": "daily",
}

# Default untuk halaman biasa
DEFAULT_PRIORITY = 0.6
DEFAULT_FREQ = "monthly"

# Halaman yang TIDAK boleh masuk sitemap
EXCLUDE_PREFIXES = [
    "/tg-game/",
    "/assets/",
]


def should_include(rel_path: str) -> bool:
    """Cek apakah file .html layak masuk sitemap."""
    if not rel_path.endswith(".html"):
        return False
    for prefix in EXCLUDE_PREFIXES:
        if rel_path.startswith(prefix):
            return False
    return True


def get_priority(path: str) -> float:
    # Exact match dulu
    if path in PRIORITY:
        return PRIORITY[path]
    return DEFAULT_PRIORITY


def get_freq(path: str) -> str:
    if path in FREQ:
        return FREQ[path]
    return DEFAULT_FREQ


def scan_html_files() -> list[str]:
    """Scan semua .html di folder site (recursive)."""
    pages = []
    for root, dirs, files in os.walk(BASE):
        # Skip folder yang di-exclude
        rel_root = root.replace(BASE, "").lstrip("/")
        if rel_root.startswith("tg-game") or rel_root.startswith("assets"):
            # Skip folder ini tapi jangan break walk — tetap explore subfolders
            dirs[:] = []  # gak usah masuk lebih dalam
            continue
        for f in sorted(files):
            if not f.endswith(".html"):
                continue
            # skip .html doang (no folder)
            rel_path = os.path.join(rel_root, f) if rel_root else f
            rel_path = "/" + rel_path
            if should_include(rel_path):
                pages.append(rel_path)
    # Urutkan: root first, sisanya alphabetical
    pages.sort(key=lambda p: (0 if p == "/index.html" else 1, p))
    return pages


def generate_sitemap(pages: list[str]) -> str:
    """Generate XML sitemap."""
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for path in pages:
        # /index.html → / (SEO canonical)
        loc_path = path
        if loc_path.endswith("/index.html"):
            loc_path = loc_path[:-10]  # hapus "index.html"
        if not loc_path:
            loc_path = "/"
        loc = DOMAIN + loc_path
        priority = get_priority(path)
        freq = get_freq(path)
        lines.append("  <url>")
        lines.append(f"    <loc>{escape(loc)}</loc>")
        lines.append(f"    <lastmod>{TODAY}</lastmod>")
        lines.append(f"    <changefreq>{freq}</changefreq>")
        lines.append(f"    <priority>{priority}</priority>")
        lines.append("  </url>")
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


def generate_robots() -> str:
    return f"""User-agent: *
Allow: /
Disallow: /tg-game/

Sitemap: {DOMAIN}/sitemap.xml
"""


def main():
    print(f"🔍 Scanning .html files in {BASE}...")
    pages = scan_html_files()

    if not pages:
        print("❌ No .html files found!")
        return

    print(f"📄 Found {len(pages)} pages:")
    for p in pages:
        print(f"   ✅ {p}")

    # Sitemap
    sitemap = generate_sitemap(pages)
    sitemap_path = os.path.join(BASE, "sitemap.xml")
    with open(sitemap_path, "w") as f:
        f.write(sitemap)
    print(f"\n📦 sitemap.xml generated ({len(sitemap)} bytes)")

    # Robots
    robots = generate_robots()
    robots_path = os.path.join(BASE, "robots.txt")
    with open(robots_path, "w") as f:
        f.write(robots)
    print(f"📦 robots.txt generated")

    print(f"\n✅ SEO files updated! Run:")
    print(f"   cd {BASE} && git add sitemap.xml robots.txt && git commit -m 'update sitemap' && git push")


if __name__ == "__main__":
    main()
