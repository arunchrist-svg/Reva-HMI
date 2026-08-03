const slides = [...document.querySelectorAll('.slide')];
const counter = document.querySelector('.counter');
const progress = document.querySelector('.progress span');
const previous = document.querySelector('.prev');
const next = document.querySelector('.next');
let current = 0;

function showSlide(index) {
  current = (index + slides.length) % slides.length;
  slides.forEach((slide, slideIndex) => {
    slide.classList.toggle('is-active', slideIndex === current);
    slide.setAttribute('aria-hidden', slideIndex === current ? 'false' : 'true');
  });
  counter.textContent = `${String(current + 1).padStart(2, '0')} / ${String(slides.length).padStart(2, '0')}`;
  progress.style.width = `${((current + 1) / slides.length) * 100}%`;
  document.title = `${slides[current].dataset.title} — HCI for M.Arch`;
}

previous.addEventListener('click', () => showSlide(current - 1));
next.addEventListener('click', () => showSlide(current + 1));

window.addEventListener('keydown', (event) => {
  if (['ArrowRight', 'ArrowDown', 'PageDown', ' '].includes(event.key)) {
    event.preventDefault();
    showSlide(current + 1);
  }
  if (['ArrowLeft', 'ArrowUp', 'PageUp'].includes(event.key)) {
    event.preventDefault();
    showSlide(current - 1);
  }
  if (event.key === 'Home') showSlide(0);
  if (event.key === 'End') showSlide(slides.length - 1);
});

let touchStartX = 0;
window.addEventListener('touchstart', (event) => {
  touchStartX = event.changedTouches[0].screenX;
}, { passive: true });
window.addEventListener('touchend', (event) => {
  const delta = event.changedTouches[0].screenX - touchStartX;
  if (Math.abs(delta) > 60) showSlide(current + (delta < 0 ? 1 : -1));
}, { passive: true });

showSlide(0);
