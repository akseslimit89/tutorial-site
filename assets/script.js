/* ═══════════════════════════════════════════
   VENICELAB SHARED SCRIPTS — Premium
   ═══════════════════════════════════════════ */

// ── COMMENT SYSTEM ──
function submitComment() {
  const name = document.getElementById('comment-name')?.value?.trim() || 'Anonymous';
  const text = document.getElementById('comment-text')?.value?.trim();
  if (!text) return;

  const list = document.getElementById('comments-list');
  if (!list) return;

  const firstLetter = name.charAt(0).toUpperCase();
  const colors = ['#2563eb', '#f59e0b', '#10b981', '#ef4444', '#8b5cf6', '#ec4899'];
  const color = colors[Math.floor(Math.random() * colors.length)];

  const item = document.createElement('div');
  item.className = 'comment-item';
  item.style.opacity = '0';
  item.style.transition = 'opacity .3s';
  item.innerHTML = `
    <div class="comment-header">
      <div class="comment-avatar" style="background:${color}">${firstLetter}</div>
      <div>
        <span class="comment-name">${escapeHtml(name)}</span>
        <span class="comment-time">Just now</span>
      </div>
    </div>
    <p class="comment-text">${escapeHtml(text)}</p>
  `;

  list.insertBefore(item, list.firstChild);
  requestAnimationFrame(() => item.style.opacity = '1');

  document.getElementById('comment-name').value = '';
  document.getElementById('comment-text').value = '';
}

function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

// ── LANGUAGE TOGGLE ──
let currentLang = 'en';

const partsData = {
  en: [
    {id:1, title:"How to Create a Digital Wallet (FaucetPay)", desc:"Your first step — a free wallet in 5 minutes.", read:"3 min", ads:"Micro Wallet"},
    {id:2, title:"Auto Faucet Claim Using Your Phone", desc:"Set up a faucet bot to earn satoshis every hour.", read:"5 min", ads:"Crypto Earn"},
    {id:3, title:"Micro Tasks — Earn $0.5-1 Per Day", desc:"Complete small online tasks. No special skills needed.", read:"7 min", ads:"Task Hub"},
    {id:4, title:"Airdrop Farming for Beginners", desc:"Find, register, and claim free airdrops before listing.", read:"10 min", ads:"Airdrop Alert"},
    {id:5,title:"Tips to Cash Out Fast & Avoid Scams", desc:"What to do — and what NOT to do. Stay safe.", read:"4 min", ads:"Safe Earn"},
    {id:6, title:"10x Your Income — Advanced Strategy", desc:"Scale from $5 to $50-100/month. Multi-account & automation.", read:"8 min", ads:"Scale Up"},
  ],
  id: [
    {id:1, title:"Cara Bikin Dompet Digital (FaucetPay)", desc:"Langkah pertama — dompet gratis dalam 5 menit.", read:"3 mnt", ads:"Dompet"},
    {id:2, title:"Auto Claim Faucet Pake HP", desc:"Setel bot faucet buat dapet satoshi tiap jam.", read:"5 mnt", ads:"Crypto"},
    {id:3, title:"Micro Tasks — Dapet $0.5-1 Per Hari", desc:"Kerjakan tugas kecil online. Gak perlu skill khusus.", read:"7 mnt", ads:"Task"},
    {id:4, title:"Airdrop Farming untuk Pemula", desc:"Cari, daftar, dan klaim airdrop gratis sebelum listing.", read:"10 mnt", ads:"Airdrop"},
    {id:5,title:"Tips Cairkan Duit & Hindari Scam", desc:"Yang boleh & gak boleh dilakukan. Tetap aman.", read:"4 mnt", ads:"Aman"},
    {id:6, title:"10x Lipat Penghasilan — Strategi Lanjutan", desc:"Skalakan dari $5 ke $50-100/bulan. Multi-akun & otomatisasi.", read:"8 mnt", ads:"Scale Up"},
  ]
};

function renderParts(lang) {
  const parts = partsData[lang];
  const list = document.getElementById('partList');
  if (!list) return;

  list.innerHTML = '';
  parts.forEach(p => {
    const card = document.createElement('div');
    card.className = 'card-horizontal';
    card.onclick = () => window.location.href = 'parts/part'+p.id+(lang==='en'?'-en':'')+'.html';
    card.innerHTML = `
      <div class="card-num">${p.id}</div>
      <div class="card-body">
        <h3>${p.title}</h3>
        <div class="card-meta">
          <span>⏱ ${p.read}</span>
          <span>📢 ${p.ads}</span>
        </div>
        <div class="card-desc">${p.desc}</div>
      </div>
      <div class="card-arrow">→</div>
    `;
    list.appendChild(card);
  });

  const badge = document.getElementById('langBadge');
  if (badge) badge.textContent = lang === 'en' ? '🌍 English' : '🌍 Indonesia';
  currentLang = lang;
}

function toggleLang() {
  const newLang = currentLang === 'en' ? 'id' : 'en';
  renderParts(newLang);
}

// ── REAL VISITOR COUNTER ──
(function() {
    const totalEl = document.getElementById('totalCount');
    const liveEl = document.getElementById('liveCount');
    const countryEl = document.getElementById('countryCount');
    if (!totalEl) return;
    
    const today = new Date().toISOString().split('T')[0];
    const ts = Date.now(); // anti-cache
    
    // 1️⃣ Total visitors — dari visitor badge
    fetch(`https://visitor-badge.laobi.icu/badge?page_id=venicelab.web.id&_=${ts}`)
        .then(r => r.text())
        .then(svg => {
            const match = svg.match(/<text[^>]*x="571[^"]*"[^>]*>([^<]+)<\/text>/);
            totalEl.textContent = match ? match[1] : '1K+';
        })
        .catch(() => { totalEl.textContent = '1K+'; });
    
    // 2️⃣ Today — badge harian (auto reset tiap hari)
    fetch(`https://visitor-badge.laobi.icu/badge?page_id=venicelab.${today}&_=${ts}`)
        .then(r => r.text())
        .then(svg => {
            const match = svg.match(/<text[^>]*x="571[^"]*"[^>]*>([^<]+)<\/text>/);
            if (liveEl) liveEl.textContent = match ? match[1] : '0';
        })
        .catch(() => { if (liveEl) liveEl.textContent = '0'; });
    
    // 3️⃣ Country — deteksi real dari IP
    if (countryEl) {
        fetch('https://api.ipify.org?format=json')
            .then(r => r.json())
            .then(d => fetch(`http://ip-api.com/json/${d.ip}?fields=status,country,countryCode`))
            .then(r => r.json())
            .then(geo => {
                if (geo.status === 'success') {
                    const flags = {
                        'ID':'🇮🇩','US':'🇺🇸','GB':'🇬🇧','DE':'🇩🇪','FR':'🇫🇷',
                        'NL':'🇳🇱','SG':'🇸🇬','JP':'🇯🇵','KR':'🇰🇷','MY':'🇲🇾',
                        'VN':'🇻🇳','TH':'🇹🇭','CA':'🇨🇦','AU':'🇦🇺','RU':'🇷🇺',
                        'IN':'🇮🇳','CN':'🇨🇳','BR':'🇧🇷'
                    };
                    countryEl.textContent = `${flags[geo.countryCode]||'🌍'} ${geo.country}`;
                }
            })
            .catch(() => { countryEl.textContent = '🌍 Indonesia'; });
    }
    
})();

// ── INIT ──
document.addEventListener('DOMContentLoaded', () => {
  const list = document.getElementById('partList');
  if (list && typeof renderParts === 'function') renderParts('en');
});
