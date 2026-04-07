self.addEventListener('install', function(e) {
    e.waitUntil(
        caches.open('hangarin-cache-v1').then(function(cache) {
            return cache.addAll(['/']);
        })
    );
});

self.addEventListener('fetch', function(e) {
    // Skip non-GET requests and Chrome extension requests
    if (e.request.method !== 'GET') return;
    if (!e.request.url.startsWith('http')) return;

    e.respondWith(
        caches.match(e.request).then(function(response) {
            if (response) return response;

            return fetch(e.request).catch(function() {
                // Silently fail — don't break the page
                return new Response('', { status: 503 });
            });
        })
    );
});