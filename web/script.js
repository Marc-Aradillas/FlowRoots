// Mobile nav toggle
const navToggle = document.getElementById('navToggle');
const mainNav = document.getElementById('mainNav');

navToggle?.addEventListener('click', () => {
  mainNav.classList.toggle('open');
  if (mainNav.classList.contains('open')) {
    mainNav.style.display = 'flex';
    navToggle.textContent = '✕';
  } else {
    mainNav.style.display = '';
    navToggle.textContent = '☰';
  }
});

// Simple intersection observer for reveal animations
const observer = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      e.target.classList.add('revealed');
      observer.unobserve(e.target);
    }
  });
}, {threshold: 0.12});

document.querySelectorAll('.reveal').forEach(el => observer.observe(el));

// Smooth internal link scrolling (for older browsers)
document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.addEventListener('click', function(e){
    const href = this.getAttribute('href');
    if(href.length > 1){
      e.preventDefault();
      const el = document.querySelector(href);
      el?.scrollIntoView({behavior: 'smooth', block: 'start'});
      // close mobile nav if open
      if (mainNav.classList.contains('open')) {
        mainNav.classList.remove('open');
        mainNav.style.display='';
        navToggle.textContent='☰';
      }
    }
  });
});

// Fetch events from Flask API and display with countdown
async function loadEvents() {
  try {
    const response = await fetch('/api/events');
    const events = await response.json();

    const container = document.getElementById('events-list');
    container.innerHTML = '';

    events.forEach(evt => {
      const card = document.createElement('article');
      card.className = 'card';

      // Calculate time left
      const eventDate = new Date(evt.date);
      const now = new Date();
      const diffTime = eventDate - now;
      let countdownText = '';

      if (diffTime > 0) {
        const days = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
        countdownText = `${days} day${days !== 1 ? 's' : ''} left`;
      } else {
        countdownText = 'Event has passed';
      }

      card.innerHTML = `
        <h3>${evt.title}</h3>
        <p><strong>Date:</strong> ${evt.date}</p>
        <p><strong>Location:</strong> ${evt.location}</p>
        <p><strong>Instructor:</strong> ${evt.instructor}</p>
        <p class="countdown">${countdownText}</p>
      `;

      container.appendChild(card);
    });
  } catch (err) {
    console.error('Error loading events:', err);
  }
}

// Load events when page loads
document.addEventListener('DOMContentLoaded', loadEvents);