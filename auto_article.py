#!/usr/bin/env python3
"""Auto Artikel Pipeline — VeniceLab
Generate artikel via opencode, wrap pake tema, sitemap, deploy.

opencode run akan bikin file .html di direktori saat ini.
Kita baca file itu, parse structured output, lalu create
file final di blog/ dengan tema VenusLab lengkap.
"""

import os, sys, re, json, subprocess, random, textwrap, shutil, glob
from datetime import datetime
from pathlib import Path

SITE = Path(os.path.dirname(os.path.abspath(__file__)))
BLOG = SITE / 'blog'
SITEMAP = SITE / 'sitemap.xml'
DEPLOY_SCRIPT = Path(os.path.expanduser('~/.hermes/scripts/auto-deploy'))

# ── Rotating Topics ──────────────────────────────────────
TOPICS = [
    "AI untuk content creator 2026 — tools wajib",
    "Cara pakai AI agent buat otomatisasi kerjaan",
    "Perbandingan ChatGPT vs Claude vs Gemini 2026",
    "Coding pake AI: dari nol sampai deploy website",
    "AI image generator gratis terbaik 2026",
    "Masa depan AI di Indonesia — peluang karier",
    "Prompt engineering dasar untuk pemula",
    "AI buat bisnis kecil — modal kecil hasil maksimal",
    "Cara dapet passive income dari AI 2026",
    "Airdrop crypto yang masih gacor 2026",
    "Strategi farming airdrop pakai multi-akun",
    "Website monetisasi: adsense vs monetag vs adsterra",
    "Cara bikin blog yang menghasilkan $500/bulan",
    "Crypto trading untuk pemula — jangan FOMO",
    "NFT masih worth it? Analisis 2026",
    "Auto traffic buat website — aman atau risky?",
    "Cara hosting website gratis pake Cloudflare Pages",
    "Tutorial Python otomatisasi untuk pemula",
    "Bikin bot Telegram pake Python — step by step",
    "Cara pake proxy buat scraping dan farming",
    "Tips hemat kuota VPS buat automation",
    "Setup Selenium/Playwright di VPS murah",
    "Cara daftar domain gratis .com .my.id",
    "Optimasi SEO buat blog pemula 2026",
    "Cara lolos Monetag/Adsterra buat pemula Indonesia",
    "YouTube automation pake AI — masih kerja?",
    "Remote job 2026: skill yang paling dicari",
    "Dropshipping vs Affiliate marketing 2026",
    "Buat landing page yang konversi tinggi",
    "Cara dapet google adsense di Indonesia 2026",
    "Side hustle dengan AI tools — modal laptop",
    "Digital product yang laris di pasaran 2026",
    "Cara daftar akun Grok AI dari Indonesia 2026",
    "Bot Telegram auto-reply pake Python gratis",
    "Cara bypass captcha pake AI 2026",
    "Multi akun farming — tips anti-banned",
    "Cara bikin SaaS modal kecil pake AI",
    "Affiliate marketing untuk pemula Indonesia 2026",
    "Cara analisis kompetitor blog pake AI tools",
    "Strategi konten evergreen yang menghasilkan",
]

def make_slug(title):
    s = title.lower().strip()
    s = re.sub(r'[^\w\s-]', '', s)
    s = re.sub(r'[-\s]+', '-', s)
    return s[:80]

def pick_topic(slot=None):
    """Pick topic deterministically.
    slot: 0=pagi (08), 1=siang (14), 2=malam (20).
    Auto-detect from current hour if not specified.
    """
    if slot is None:
        h = datetime.now().hour
        if h < 11:
            slot = 0  # pagi
        elif h < 17:
            slot = 1  # siang
        else:
            slot = 2  # malam
    day = datetime.now().timetuple().tm_yday
    idx = (day * 3 + slot) % len(TOPICS)
    return TOPICS[idx]

def clean_temp_files():
    """Hapus file .html di root tutorial-site dari opencode."""
    for f in SITE.glob('*.html'):
        if f.parent == BLOG:
            continue
        f.unlink()
        print(f'  🧹 Clean: {f.name}')

def generate_article(topic):
    """Generate artikel via opencode run.
    opencode akan bikin file .html di current dir.
    Kita baca file termuda, parse structured output."""
    
    prompt = textwrap.dedent(f"""\
    Tugas lo: buat file artikel blog SEO-friendly bahasa Indonesia tentang:
    {topic}
    
    FORMAT FILE (tulis persis seperti ini di file):
    
    JUDUL: <judul artikel max 60 karakter>
    KATEGORI: <Ai | Crypto | Tutorial | Passive Income>
    DESKRIPSI: <meta description max 155 karakter>
    KEYWORDS: <keyword1, keyword2, keyword3>
    
    KONTEN:
    <Tulis artikel lengkap minimal 600 kata dengan HTML>
    - Bahasa santai Indonesia (Lo/Gue) tapi informatif
    - Minimal 4 paragraf + 3 sub-heading pake <h2>
    - Paragraf pake <p>, list pake <ul>/<li>
    - Akhiri dengan kesimpulan
    - LANGSUNG HTML — jangan pake markdown
    
    Contoh format konten:
    <p>Paragraf pembuka...</p>
    <h2>Sub Topik 1</h2>
    <p>Penjelasan detail...</p>
    <ul>
      <li>Point 1</li>
      <li>Point 2</li>
    </ul>
    <h2>Sub Topik 2</h2>
    <p>Penjelasan...</p>
    <h2>Kesimpulan</h2>
    <p>Kesimpulan...</p>
    
    TULIS FILE dengan nama: artikel-{make_slug(topic)}-{datetime.now().strftime('%m%d')}.html
    JANGAN pake markdown, langsung tulis file.
    """)
    
    result = subprocess.run(
        ['opencode', 'run', '--model', 'opencode/deepseek-v4-flash-free'],
        input=prompt,
        capture_output=True,
        text=True,
        timeout=180,
        env={**os.environ, 'OPENCODE_HEADLESS': 'true'}
    )
    
    # Cari file termuda di SITE yang .html (bukan di blog/)
    html_files = sorted(SITE.glob('*.html'), key=lambda f: f.stat().st_mtime, reverse=True)
    if not html_files:
        print('❌ opencode gak bikin file HTML!')
        print('STDOUT:', result.stdout[-500:])
        print('STDERR:', result.stderr[-500:])
        return None
    
    newest = html_files[0]
    content = newest.read_text(encoding='utf-8')
    print(f'📄 File generated: {newest.name} ({len(content)} chars)')
    
    article = {'topic': topic}
    
    # Parse structured fields
    for field in ['JUDUL', 'KATEGORI', 'DESKRIPSI', 'KEYWORDS']:
        m = re.search(rf'^{field}:\s*(.+?)$', content, re.MULTILINE)
        article[field.lower()] = m.group(1).strip() if m else ''
    
    # Extract content after KONTEN:
    konten_match = re.search(r'KONTEN:\s*\n(.*?)$', content, re.DOTALL)
    if konten_match:
        article['konten_html'] = konten_match.group(1).strip()
    else:
        article['konten_html'] = content.strip()
    
    # Fallback title
    if not article.get('judul'):
        h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', article['konten_html'])
        article['judul'] = h1_match.group(1) if h1_match else topic[:80]
    
    article['slug'] = make_slug(article['judul'])
    article['date'] = datetime.now().strftime('%Y-%m-%d')
    article['image_url'] = f"https://picsum.photos/seed/{article['slug']}/800/400"
    
    # Hapus file temp
    newest.unlink()
    
    return article

def build_html(article):
    """Build complete themed HTML page."""
    date_obj = datetime.now()
    month_names = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni',
                   'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember']
    date_display = f"{date_obj.day} {month_names[date_obj.month-1]} {date_obj.year}"
    year = date_obj.year
    cat = article.get('kategori', 'Ai')
    judul = article['judul']
    deskripsi = article.get('deskripsi', judul)
    keywords = article.get('keywords', 'venicelab, tutorial, 2026')
    slug = article['slug']
    img = article['image_url']
    konten = article.get('konten_html', '<p>Artikel sedang diperbarui.</p>')
    
    # Escape for HTML (prevent XSS)
    judul_esc = judul.replace('"', '&quot;').replace('&', '&amp;')
    deskripsi_esc = deskripsi.replace('"', '&quot;').replace('&', '&amp;')
    
    html = f'''<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{judul_esc} | VeniceLab</title>
<meta name="description" content="{deskripsi_esc}">
<meta name="keywords" content="{keywords}">
<meta property="og:title" content="{judul_esc}">
<meta property="og:description" content="{deskripsi_esc}">
<meta property="og:image" content="{img}">
<meta property="og:type" content="article">
<meta property="og:url" content="https://venicelab.web.id/blog/{slug}.html">
<script async src="https://www.googletagmanager.com/gtag/js?id=G-0770R5SEN7"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','G-0770R5SEN7');</script>
<script src="https://quge5.com/88/tag.min.js" data-zone="259806" async data-cfasync="false"></script>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#f8fafc;color:#1e293b;line-height:1.8}}
.container{{max-width:760px;margin:0 auto;padding:24px}}
header{{background:linear-gradient(135deg,#2563eb,#1e40af);color:#fff;padding:40px 24px;text-align:center}}
header h1{{font-size:2em;margin-bottom:8px}}
.meta{{color:#94a3b8;font-size:.9em;margin:16px 0}}
.cover{{width:100%;height:auto;aspect-ratio:2/1;border-radius:12px;margin:24px 0}}
.content{{font-size:1.05em}}
.content h2{{font-size:1.4em;margin:32px 0 12px;color:#2563eb}}
.content p{{margin-bottom:16px}}
.content ul{{margin:16px 0;padding-left:24px}}
.content li{{margin-bottom:8px}}
.ad{{width:100%;min-height:280px;margin:32px 0;background:#f1f5f9;border-radius:8px}}
footer{{text-align:center;padding:40px;color:#94a3b8;font-size:.9em}}
a{{color:#2563eb}}
</style>
</head>
<body>
<header>
  <h1>{judul_esc}</h1>
  <p>VeniceLab — AI, Crypto & Passive Income</p>
</header>
<div class="container">
  <div class="meta">{date_display} · Kategori: {cat}</div>
  <img class="cover" src="{img}" alt="{judul_esc}" width="800" height="400" loading="lazy">
  <article class="content">
{konten}
  </article>
  <div class="ad"></div>
</div>
<footer>&copy; {year} VeniceLab — Powered by FIOLA AI</footer>
</body>
</html>'''
    return html

def save_article(html, slug):
    path = BLOG / f'{slug}.html'
    BLOG.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding='utf-8')
    print(f'✅ Artikel disimpan: blog/{slug}.html')
    return path

def update_sitemap():
    BLOG.mkdir(parents=True, exist_ok=True)
    entries = []
    for f in sorted(BLOG.glob('*.html'), reverse=True):
        lastmod = datetime.fromtimestamp(f.stat().st_mtime).strftime('%Y-%m-%d')
        slug = f.stem
        entries.append((lastmod, slug))
    
    urls = '\n'.join(
        f'''  <url>
    <loc>https://venicelab.web.id/blog/{slug}.html</loc>
    <lastmod>{lastmod}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>'''
        for lastmod, slug in entries[:100]
    )
    
    sitemap_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://venicelab.web.id/</loc>
    <lastmod>{datetime.now().strftime('%Y-%m-%d')}</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>
{urls}
</urlset>'''
    
    SITEMAP.write_text(sitemap_content, encoding='utf-8')
    print(f'✅ Sitemap: {len(entries)} entries')

def deploy():
    if not DEPLOY_SCRIPT.exists():
        print('⚠️ Deploy script not found')
        return
    result = subprocess.run(['bash', str(DEPLOY_SCRIPT)], capture_output=True, text=True, timeout=120)
    print(result.stdout)
    if result.returncode != 0:
        err = result.stderr[:300]
        if 'already up' in result.stdout.lower():
            print('⚠️ Git pull issue, deploying anyway')
        else:
            print(f'❌ Deploy error: {err}')

def main():
    topic = None
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg.isdigit():
            # Slot mode: 0=pagi, 1=siang, 2=malam
            topic = pick_topic(slot=int(arg))
        else:
            topic = arg
    else:
        topic = pick_topic()
    
    print(f'🔥 Generate artikel: {topic}')
    
    # Step 1: Generate via opencode
    article = generate_article(topic)
    if not article:
        sys.exit(1)
    
    print(f'📝 Judul: {article["judul"]}')
    print(f'📐 Slug: {article["slug"]}')
    print(f'📦 Konten: {len(article.get("konten_html", ""))} chars')
    
    # Step 2: Build themed HTML
    html = build_html(article)
    
    # Step 3: Save
    save_article(html, article['slug'])
    
    # Step 4: Sitemap
    update_sitemap()
    
    # Step 5: Deploy
    deploy()
    
    print(f'\n✅ SELESAI — {article["judul"]}')
    print(f'   URL: https://venicelab.web.id/blog/{article["slug"]}.html')

if __name__ == '__main__':
    main()
