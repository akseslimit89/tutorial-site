# Cara Nambah Artikel Baru + Gambar

## 1. Buat file artikel

```bash
nano ~/tutorial-site/blog/judul-artikel-baru.html
```

## 2. Template artikel (copy-paste)

```html
<!DOCTYPE html>
<html><head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Judul Artikel — VeniceLab</title>
<!-- Google tag -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-0770R5SEN7"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}gtag('js',new Date());gtag('config','G-0770R5SEN7');</script>
<!-- quge5 ad -->
<script src="https://quge5.com/88/tag.min.js" data-zone="259806" async data-cfasync="false"></script>
<link rel="stylesheet" href="../assets/style.css">
<style>
body{font-family:Inter,sans-serif;max-width:800px;margin:0 auto;padding:24px;line-height:1.8;color:#0f172a}
img{max-width:100%;border-radius:16px;margin:24px 0}
h1{font-size:2em;margin-bottom:8px}
.article-meta{color:#64748b;font-size:.85em;margin-bottom:32px}
.back{display:inline-block;margin-bottom:24px;color:#2563EB;text-decoration:none;font-weight:600}
</style>
</head><body>

<a href="../" class="back">← Back to VeniceLab</a>

<!-- ========== GAMBAR ARTIKEL ========== -->
<!-- Ganti seed sesuai topik:
     AI/ai → seed/ai-neural-network
     Airdrop/crypto → seed/crypto-airdrops
     Earn/money → seed/passive-income
     Telegram/bot → seed/telegram-bots
     Tutorial → seed/earn-tutorial
     Ads/PTC → seed/earn-ads-revenue
     Faucet → seed/crypto-faucet
     Generic → seed/venice-article
-->
<img src="https://picsum.photos/seed/ai-neural-network/800/400" alt="AI Tools" loading="lazy">

<h1>Judul Artikel Kamu</h1>
<div class="article-meta">📅 Jul 20, 2026 · ✍️ Venice Lab</div>

<!-- Konten artikel -->
<p>Mulai nulis disini...</p>

</body></html>
```

## 3. Daftar seed gambar per topik

| Topik | Seed | Contoh URL |
|-------|------|-----------|
| AI / Robot | `ai-neural-network` | `https://picsum.photos/seed/ai-neural-network/800/400` |
| Crypto / Airdrop | `crypto-airdrops` | `https://picsum.photos/seed/crypto-airdrops/800/400` |
| Earn / Money | `passive-income` | `https://picsum.photos/seed/passive-income/800/400` |
| Telegram / Bot | `telegram-bots` | `https://picsum.photos/seed/telegram-bots/800/400` |
| Tutorial | `earn-tutorial` | `https://picsum.photos/seed/earn-tutorial/800/400` |
| Ads / PTC | `earn-ads-revenue` | `https://picsum.photos/seed/earn-ads-revenue/800/400` |
| Faucet | `crypto-faucet` | `https://picsum.photos/seed/crypto-faucet/800/400` |
| Automation | `telegram-automation` | `https://picsum.photos/seed/telegram-automation/800/400` |
| Generic | `venice-article` | `https://picsum.photos/seed/venice-article/800/400` |

**PENTING:** Setiap seed selalu nampilin gambar yang SAMA — jadi topik yang sama dapet gambar konsisten.

## 4. Update sitemap

Sitemap **auto-update** pas commit (pre-commit hook). Tinggal jalanin:

```bash
cd ~/tutorial-site && git add blog/judul-artikel.html && git commit -m "tambah artikel: judul" && git push
```

## 5. Link artikel baru ke homepage

Edit `index.html` — tambahin ke bagian `<!-- ═══════════ LATEST POSTS ═══════════ -->`

Gunakan `articleImage()` biar auto milih gambar:
```html
<a href="/blog/judul-artikel.html" class="post-sidebar-item fade-up">
  <img src="https://picsum.photos/seed/ai-neural-network/160/160" alt="..." loading="lazy">
  <div class="post-sidebar-body">
    <span class="post-tag">🤖 AI Tools</span>
    <h4>Judul Artikel</h4>
  </div>
</a>
```

Ukuran gambar:
- **Featured** (besar): `800/400`
- **Sidebar** (kecil): `160/160`
