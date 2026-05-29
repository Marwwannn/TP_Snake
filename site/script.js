/* =========================================================
   TP Snake - Compte rendu | interactions
   ========================================================= */
'use strict';

const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

/* ---------- Menu mobile ---------- */
const menuBtn = document.getElementById('menuBtn');
const sidebar = document.getElementById('sidebar');
const overlay = document.getElementById('overlay');

function setMenu(open) {
  sidebar.classList.toggle('open', open);
  menuBtn.setAttribute('aria-expanded', String(open));
  overlay.hidden = !open;
  requestAnimationFrame(() => overlay.classList.toggle('show', open));
}
menuBtn.addEventListener('click', () => setMenu(!sidebar.classList.contains('open')));
overlay.addEventListener('click', () => setMenu(false));
sidebar.querySelectorAll('nav a').forEach(a => a.addEventListener('click', () => setMenu(false)));

/* ---------- Barre de progression de lecture ---------- */
const progress = document.getElementById('progress');
function updateProgress() {
  const h = document.documentElement;
  const scrollable = h.scrollHeight - h.clientHeight;
  progress.style.width = scrollable > 0 ? (h.scrollTop / scrollable) * 100 + '%' : '0%';
}
document.addEventListener('scroll', updateProgress, { passive: true });
updateProgress();

/* ---------- Scrollspy ---------- */
const links = [...document.querySelectorAll('.sidebar nav a')];
const sections = links.map(a => document.querySelector(a.getAttribute('href'))).filter(Boolean);
const spy = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      const id = '#' + e.target.id;
      links.forEach(l => l.classList.toggle('active', l.getAttribute('href') === id));
    }
  });
}, { rootMargin: '-45% 0px -50% 0px', threshold: 0 });
sections.forEach(s => spy.observe(s));

/* ---------- Reveal au scroll ---------- */
const revealEls = [...document.querySelectorAll('.reveal')];
if (reduceMotion) {
  revealEls.forEach(el => el.classList.add('in'));
} else {
  const revObs = new IntersectionObserver((entries, obs) => {
    entries.forEach(e => {
      if (e.isIntersecting) { e.target.classList.add('in'); obs.unobserve(e.target); }
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });
  revealEls.forEach(el => revObs.observe(el));
}

/* ---------- Compteurs animes ---------- */
const counters = [...document.querySelectorAll('[data-count]')];
const countObs = new IntersectionObserver((entries, obs) => {
  entries.forEach(e => {
    if (!e.isIntersecting) return;
    obs.unobserve(e.target);
    const el = e.target;
    const target = parseInt(el.dataset.count, 10);
    const prefix = el.dataset.prefix || '';
    if (reduceMotion) { el.textContent = prefix + target; return; }
    const dur = 1100; const start = performance.now();
    (function tick(now) {
      const p = Math.min((now - start) / dur, 1);
      const eased = 1 - Math.pow(1 - p, 3);
      el.textContent = prefix + Math.round(target * eased);
      if (p < 1) requestAnimationFrame(tick);
    })(start);
  });
}, { threshold: 0.5 });
counters.forEach(c => countObs.observe(c));

/* ---------- Visionneuse de code ---------- */
const tabs = document.getElementById('tabs');
const codeView = document.getElementById('codeView');
const gutter = document.getElementById('gutter');

function escapeHtml(s) {
  return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}
function showFile(name) {
  const content = (typeof SOURCES !== 'undefined' && SOURCES[name]) || '// fichier indisponible';
  const lines = content.replace(/\n$/, '').split('\n');
  gutter.textContent = lines.map((_, i) => i + 1).join('\n');
  codeView.innerHTML = escapeHtml(lines.join('\n'));
  [...tabs.children].forEach(b => b.classList.toggle('active', b.dataset.file === name));
  codeView.parentElement.scrollTop = 0;
}
if (typeof SOURCES !== 'undefined' && tabs) {
  const order = ['Entity.py', 'MovingEntity.py', 'Snake.py', 'Food.py',
                 'Game.py', 'GameAI.py', 'SnakeAI.py', 'train.py', 'play.py', 'requirements.txt'];
  const files = order.filter(f => f in SOURCES).concat(
    Object.keys(SOURCES).filter(f => !order.includes(f)));
  files.forEach(name => {
    const btn = document.createElement('button');
    btn.textContent = name;
    btn.dataset.file = name;
    btn.addEventListener('click', () => showFile(name));
    tabs.appendChild(btn);
  });
  if (files.length) showFile(files[0]);
}

/* =========================================================
   Mini-Snake jouable (canvas)
   ========================================================= */
(function miniSnake() {
  const canvas = document.getElementById('board');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');

  const GRID = 17;          // cellules par cote
  const COLORS = {
    bg: '#0e1320', grid: '#171f33',
    head: '#34d77f', body: '#16a05a', bodyDark: '#0f7d45',
    food: '#ff5d5d', foodGlow: 'rgba(255,93,93,.35)'
  };

  let cell, snake, dir, nextDir, food, score, best, timer, running = false, dead = false;

  best = parseInt(localStorage.getItem('tpsnake-best') || '0', 10);
  const elScore = document.getElementById('hsScore');
  const elBest = document.getElementById('hsBest');
  const overlayEl = document.getElementById('boardOverlay');
  const ovTitle = document.getElementById('ovTitle');
  const ovSub = document.getElementById('ovSub');
  const ovBtn = document.getElementById('ovBtn');
  elBest.textContent = best;

  function resize() {
    const size = canvas.clientWidth || 420;
    const dpr = window.devicePixelRatio || 1;
    canvas.width = size * dpr;
    canvas.height = size * dpr;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    cell = size / GRID;
    draw();
  }

  function spawnFood() {
    let p;
    do {
      p = { x: Math.floor(Math.random() * GRID), y: Math.floor(Math.random() * GRID) };
    } while (snake.some(s => s.x === p.x && s.y === p.y));
    food = p;
  }

  function reset() {
    snake = [{ x: 8, y: 8 }, { x: 7, y: 8 }, { x: 6, y: 8 }];
    dir = { x: 1, y: 0 }; nextDir = { x: 1, y: 0 };
    score = 0; dead = false;
    elScore.textContent = '0';
    spawnFood();
  }

  function step() {
    dir = nextDir;
    const head = { x: snake[0].x + dir.x, y: snake[0].y + dir.y };

    // collisions murs ou corps
    if (head.x < 0 || head.y < 0 || head.x >= GRID || head.y >= GRID ||
        snake.some(s => s.x === head.x && s.y === head.y)) {
      gameOver();
      return;
    }
    snake.unshift(head);
    if (head.x === food.x && head.y === food.y) {
      score++;
      elScore.textContent = score;
      spawnFood();
    } else {
      snake.pop();
    }
    draw();
  }

  const hasRoundRect = typeof ctx.roundRect === 'function';
  function roundRect(x, y, w, h, r) {
    ctx.beginPath();
    if (hasRoundRect) {
      ctx.roundRect(x, y, w, h, r);
    } else {
      r = Math.min(r, w / 2, h / 2);
      ctx.moveTo(x + r, y);
      ctx.arcTo(x + w, y, x + w, y + h, r);
      ctx.arcTo(x + w, y + h, x, y + h, r);
      ctx.arcTo(x, y + h, x, y, r);
      ctx.arcTo(x, y, x + w, y, r);
    }
    ctx.fill();
  }

  function draw() {
    const size = GRID * cell;
    ctx.fillStyle = COLORS.bg;
    ctx.fillRect(0, 0, size, size);

    // grille
    ctx.strokeStyle = COLORS.grid; ctx.lineWidth = 1;
    for (let i = 1; i < GRID; i++) {
      ctx.beginPath(); ctx.moveTo(i * cell, 0); ctx.lineTo(i * cell, size); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(0, i * cell); ctx.lineTo(size, i * cell); ctx.stroke();
    }

    if (!snake) return;

    // pomme
    const fx = food.x * cell, fy = food.y * cell;
    ctx.fillStyle = COLORS.foodGlow;
    roundRect(fx + 1, fy + 1, cell - 2, cell - 2, cell * 0.45);
    ctx.fillStyle = COLORS.food;
    roundRect(fx + cell * 0.18, fy + cell * 0.18, cell * 0.64, cell * 0.64, cell * 0.3);

    // serpent
    const pad = Math.max(1, cell * 0.12);
    snake.forEach((s, i) => {
      ctx.fillStyle = i === 0 ? COLORS.head : (i % 2 ? COLORS.body : COLORS.bodyDark);
      roundRect(s.x * cell + pad, s.y * cell + pad, cell - pad * 2, cell - pad * 2, cell * 0.28);
    });

    // yeux sur la tete
    const h = snake[0];
    ctx.fillStyle = '#0e1320';
    const ex = h.x * cell, ey = h.y * cell, e = cell * 0.13;
    const off = cell * 0.28;
    let e1, e2;
    if (dir.x !== 0) {
      const cx = dir.x > 0 ? ex + cell - off : ex + off;
      e1 = [cx, ey + off]; e2 = [cx, ey + cell - off];
    } else {
      const cy = dir.y > 0 ? ey + cell - off : ey + off;
      e1 = [ex + off, cy]; e2 = [ex + cell - off, cy];
    }
    ctx.beginPath(); ctx.arc(e1[0], e1[1], e, 0, 7); ctx.fill();
    ctx.beginPath(); ctx.arc(e2[0], e2[1], e, 0, 7); ctx.fill();
  }

  function loop() {
    if (!running) return;
    step();
    if (dead) return;
    const speed = Math.max(70, 150 - score * 4); // accelere avec le score
    timer = setTimeout(() => requestAnimationFrame(loop), speed);
  }

  function start() {
    reset();
    running = true;
    overlayEl.classList.add('hide');
    clearTimeout(timer);
    loop();
  }

  function gameOver() {
    dead = true; running = false;
    clearTimeout(timer);
    if (score > best) { best = score; localStorage.setItem('tpsnake-best', best); elBest.textContent = best; }
    ovTitle.textContent = 'Game Over';
    ovSub.textContent = 'Score : ' + score + '  -  Record : ' + best;
    ovBtn.textContent = 'Rejouer';
    overlayEl.classList.remove('hide');
  }

  function setDir(x, y) {
    if (!running) return;
    if (dir.x + x === 0 && dir.y + y === 0) return; // pas de demi-tour
    nextDir = { x, y };
  }

  // Clavier (fleches + ZQSD + WASD), sans bloquer le scroll hors-jeu
  const KEYS = {
    ArrowUp: [0, -1], ArrowDown: [0, 1], ArrowLeft: [-1, 0], ArrowRight: [1, 0],
    z: [0, -1], s: [0, 1], q: [-1, 0], d: [1, 0],
    w: [0, -1], a: [-1, 0]
  };
  // Le clavier ne pilote le jeu que si le plateau est visible a l'ecran,
  // pour ne jamais bloquer le scroll de la page avec les fleches.
  let boardVisible = false;
  new IntersectionObserver((ents) => {
    boardVisible = ents[0].isIntersecting;
  }, { threshold: 0.5 }).observe(canvas);

  window.addEventListener('keydown', (e) => {
    if (!boardVisible) return;
    const k = KEYS[e.key] || KEYS[e.key.toLowerCase()];
    if (!k) return;
    if (dead) return;
    if (!running) start();
    e.preventDefault();
    setDir(k[0], k[1]);
  });

  // Pave directionnel tactile
  document.querySelectorAll('.dpad button').forEach(b => {
    b.addEventListener('click', () => {
      if (!running) { start(); return; }
      const m = { up: [0, -1], down: [0, 1], left: [-1, 0], right: [1, 0] }[b.dataset.dir];
      setDir(m[0], m[1]);
    });
  });

  // Swipe sur le canvas
  let touch = null;
  canvas.addEventListener('touchstart', (e) => { touch = e.touches[0]; }, { passive: true });
  canvas.addEventListener('touchend', (e) => {
    if (!touch) return;
    if (!running) { start(); touch = null; return; }
    const t = e.changedTouches[0];
    const dx = t.clientX - touch.clientX, dy = t.clientY - touch.clientY;
    if (Math.abs(dx) > Math.abs(dy)) setDir(dx > 0 ? 1 : -1, 0);
    else setDir(0, dy > 0 ? 1 : -1);
    touch = null;
  }, { passive: true });

  ovBtn.addEventListener('click', start);

  // Pause quand l'onglet est cache
  document.addEventListener('visibilitychange', () => {
    if (document.hidden && running) { running = false; clearTimeout(timer); }
  });

  window.addEventListener('resize', resize);
  reset();
  resize();
})();
