document.addEventListener('DOMContentLoaded', () => {
    // 1. Navigation Toggle & Mobile Menu Drawer
    const navToggle = document.getElementById('navToggle');
    const mainNav = document.getElementById('mainNav');

    if (navToggle && mainNav) {
        navToggle.addEventListener('click', () => {
            const isOpen = mainNav.classList.toggle('active');
            mainNav.classList.toggle('open', isOpen);
            navToggle.textContent = isOpen ? '✕' : '☰';
            navToggle.setAttribute('aria-expanded', isOpen);
        });

        // Close mobile drawer automatically when tapping any nav link
        mainNav.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                mainNav.classList.remove('active', 'open');
                navToggle.textContent = '☰';
                navToggle.setAttribute('aria-expanded', 'false');
            });
        });
    }

    // 2. Intersection Observer for Smooth Scroll Reveals
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('revealed');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });

    // Helper: Safely escape user/API strings against XSS
    function escapeHTML(str) {
        if (!str) return '';
        return String(str)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#39;');
    }

    // 3. Dynamic Events Loader with Fallback State
    async function loadEvents() {
        const container = document.getElementById('events-list');
        if (!container) return;

        try {
            const response = await fetch('/api/events');
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const events = await response.json();
            container.innerHTML = '';

            // Render fallback if database returns no events
            if (!Array.isArray(events) || events.length === 0) {
                container.innerHTML = `
                    <div class="card reveal" style="grid-column: 1 / -1; text-align: center;">
                        <h3>Upcoming Workshops Dropping Soon</h3>
                        <p>Follow us on Instagram <a href="https://instagram.com/flowrootsdallas" target="_blank" rel="noopener">@flowrootsdallas</a> for immediate schedule updates!</p>
                    </div>
                `;
                container.querySelectorAll('.reveal').forEach(el => observer.observe(el));
                return;
            }

            // Render dynamic workshop cards
            events.forEach(evt => {
                const card = document.createElement('article');
                card.className = 'card reveal';
                
                // Ensure date parses in local time
                const rawDate = evt.date || '';
                const eventDate = new Date(rawDate.includes('T') ? rawDate : `${rawDate}T00:00:00`);
                const now = new Date();
                const diffTime = eventDate - now;
                
                let countdown = 'Event passed';
                if (diffTime > 0) {
                    const days = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
                    countdown = `${days} day${days === 1 ? '' : 's'} left`;
                }

                const title = escapeHTML(evt.title || 'Flow Workshop');
                const desc = escapeHTML(evt.description || 'Dallas Popping Session');
                const instructor = escapeHTML(evt.instructor || evt.teacher || 'Flow Roots Staff');

                card.innerHTML = `
                    <h3>${title}</h3>
                    <p>${desc}</p>
                    <p style="margin-top: 8px;"><strong>Instructor:</strong> ${instructor}</p>
                    <div class="countdown" style="margin-top: 10px;">${countdown}</div>
                `;

                container.appendChild(card);
                observer.observe(card);
            });

        } catch (err) {
            console.error('Events load failed:', err);
            container.innerHTML = `
                <div class="card reveal" style="grid-column: 1 / -1; text-align: center;">
                    <h3>Workshops & Sessions</h3>
                    <p>Check back shortly or DM us on Instagram for current drop-in pricing!</p>
                </div>
            `;
            container.querySelectorAll('.reveal').forEach(el => observer.observe(el));
        }
    }

    // Initialize Page Observers and Event Loading
    loadEvents();
    document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
});