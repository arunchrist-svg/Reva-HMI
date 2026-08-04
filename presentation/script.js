// Subtle scroll reveal + active nav

document.addEventListener('DOMContentLoaded', () => {
  const sections = document.querySelectorAll('.content-section, .pull-quote, .stats-band, .deliverable-band, .closing');
  const navLinks = document.querySelectorAll('.nav-links a');

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.style.opacity = '1';
          entry.target.style.transform = 'translateY(0)';
        }
      });
    },
    { threshold: 0.1, rootMargin: '0px 0px -40px 0px' }
  );

  sections.forEach((section) => {
    section.style.opacity = '0';
    section.style.transform = 'translateY(16px)';
    section.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(section);
  });

  // Highlight active nav link on scroll
  const sectionIds = ['approach', 'projects', 'tasks', 'about'];

  window.addEventListener('scroll', () => {
    let current = '';
    sectionIds.forEach((id) => {
      const el = document.getElementById(id);
      if (el && el.getBoundingClientRect().top < 120) {
        current = id;
      }
    });

    navLinks.forEach((link) => {
      link.style.color = link.getAttribute('href') === `#${current}`
        ? 'var(--text)'
        : '';
      link.style.fontWeight = link.getAttribute('href') === `#${current}`
        ? '600'
        : '';
    });
  });
});
