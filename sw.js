/* Dictation Lab service worker: works offline after the first visit */
const VERSION = 'v23-202610141730';
const CORE = 'dlab-core-' + VERSION, FONTS = 'dlab-fonts', EXAM = 'dlab-exam';
const FILES = ['./', 'index.html', 'manifest.webmanifest', 'icons/icon-192.png', 'icons/icon-512.png', 'icons/icon-maskable-512.png', 'icons/apple-touch-icon.png', 'icons/favicon-32.png'];
self.addEventListener('install', e => { e.waitUntil(caches.open(CORE).then(c => c.addAll(FILES)).then(() => self.skipWaiting())); });
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k.startsWith('dlab-') && k !== CORE && k !== FONTS && k !== EXAM).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener('fetch', e => {
  const req = e.request; if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.hostname === 'fonts.googleapis.com' || url.hostname === 'fonts.gstatic.com') {
    e.respondWith(caches.open(FONTS).then(c => c.match(req).then(hit => hit || fetch(req).then(res => { if (res.ok || res.type === 'opaque') c.put(req, res.clone()); return res; }).catch(() => new Response('', { status: 504 })))));
    return;
  }
  if (url.origin !== location.origin) return;
  if (req.headers.has('range')) return;                     // media streaming: straight to the network
  if (url.pathname.includes('/exam/') && !url.pathname.endsWith('/exam/index.html')) {   // test data, pictures and audio: keep once downloaded
    e.respondWith(caches.open(EXAM).then(c => c.match(req).then(hit => hit || fetch(req).then(res => { if (res.ok && res.status === 200) c.put(req, res.clone()); return res; }))));
    return;
  }
  if (req.mode === 'navigate') {   // fresh page when online, cached page when offline
    const isExam = url.pathname.includes('/exam/');
    e.respondWith(fetch(req).then(res => { const copy = res.clone(); caches.open(CORE).then(c => c.put(isExam ? req : 'index.html', copy)); return res; })
      .catch(() => (isExam ? caches.match(req) : caches.match('index.html')).then(r => r || caches.match('./'))));
    return;
  }
  e.respondWith(caches.match(req).then(hit => hit || fetch(req).then(res => { if (res.ok) { const copy = res.clone(); caches.open(CORE).then(c => c.put(req, copy)); } return res; })));
});
