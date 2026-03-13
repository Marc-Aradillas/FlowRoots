document.addEventListener('DOMContentLoaded', () => {
    // 1. Navigation Toggle
    const navToggle = document.getElementById('navToggle');
    const mainNav = document.getElementById('mainNav');

    navToggle?.addEventListener('click', () => {
        mainNav.classList.toggle('open');
        navToggle.textContent = mainNav.classList.contains('open') ? '✕' : '☰';
    });

    // 2. Intersection Observer for Reveals
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(e => {
            if (e.isIntersecting) {
                e.target.classList.add('revealed');
                observer.unobserve(e.target);
            }
        });
    }, { threshold: 0.1 });

    // 3. Load Dynamic Events
    async function loadEvents() {
        try {
            const response = await fetch('/api/events');
            const events = await response.json();
            const container = document.getElementById('events-list');
            if (!container) return;

            container.innerHTML = '';
            events.forEach(evt => {
                const card = document.createElement('article');
                card.className = 'card reveal';
                
                const eventDate = new Date(evt.date);
                const diffTime = eventDate - new Date();
                const countdown = diffTime > 0 
                    ? `${Math.ceil(diffTime / (1000 * 60 * 60 * 24))} days left` 
                    : 'Event passed';

                card.innerHTML = `
                    <h3>${evt.title}</h3>
                    <p>${evt.description || 'Dallas Popping Session'}</p>
                    <p><strong>Instructor:</strong> ${evt.instructor || evt.teacher}</p>
                    <div class="countdown">${countdown}</div>
                `;
                container.appendChild(card);
                observer.observe(card); // Observe the newly created card
            });
        } catch (err) { console.error('Events failed:', err); }
    }

    // Initialize
    loadEvents();
    document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
});