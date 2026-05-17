self.addEventListener('install', function(e) {
    self.skipWaiting();
});

self.addEventListener('activate', function(e) {
    e.waitUntil(
        caches.keys().then(function(keys) {
            return Promise.all(keys.map(function(key) {
                return caches.delete(key);
            }));
        })
    );
});

self.addEventListener('fetch', function(e) {
    if (e.request.method !== 'GET') return;
    if (!e.request.url.startsWith('http')) return;

    var url = new URL(e.request.url);

    // Never cache HTML pages — they contain CSRF tokens that go stale
    if (e.request.headers.get('accept') && e.request.headers.get('accept').includes('text/html')) {
        return;
    }

    // Cache-first for static assets only
    if (url.pathname.startsWith('/static/') || url.pathname.startsWith('/staticfiles/')) {
        e.respondWith(
            caches.open('hangarin-static-v2').then(function(cache) {
                return caches.match(e.request).then(function(response) {
                    if (response) return response;
                    return fetch(e.request).then(function(networkResponse) {
                        cache.put(e.request, networkResponse.clone());
                        return networkResponse;
                    }).catch(function() {
                        return new Response('', { status: 503 });
                    });
                });
            })
        );
    }
});
