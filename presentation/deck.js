const slides = [...document.querySelectorAll('.slide')];
const counter = document.querySelector('.counter');
const progress = document.querySelector('.progress span');
const previous = document.querySelector('.prev');
const next = document.querySelector('.next');
let current = 0;

function showSlide(index) {
  current = Math.max(0, Math.min(index, slides.length - 1));
  slides.forEach((slide, slideIndex) => {
    slide.classList.toggle('is-active', slideIndex === current);
    slide.setAttribute('aria-hidden', slideIndex === current ? 'false' : 'true');
  });
  counter.textContent = `${String(current + 1).padStart(2, '0')} / ${String(slides.length).padStart(2, '0')}`;
  progress.style.width = `${((current + 1) / slides.length) * 100}%`;
  document.title = `${slides[current].dataset.title}: HCI for M.Arch`;
  previous.disabled = current === 0;
  next.disabled = current === slides.length - 1;
}

previous.addEventListener('click', () => {
  if (current > 0) showSlide(current - 1);
});
next.addEventListener('click', () => {
  if (current < slides.length - 1) showSlide(current + 1);
});

window.addEventListener('keydown', (event) => {
  if (['ArrowRight', 'ArrowDown', 'PageDown', ' '].includes(event.key)) {
    event.preventDefault();
    if (current < slides.length - 1) showSlide(current + 1);
  }
  if (['ArrowLeft', 'ArrowUp', 'PageUp'].includes(event.key)) {
    event.preventDefault();
    if (current > 0) showSlide(current - 1);
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
  if (Math.abs(delta) <= 60) return;
  if (delta < 0 && current < slides.length - 1) showSlide(current + 1);
  if (delta > 0 && current > 0) showSlide(current - 1);
}, { passive: true });

showSlide(0);
