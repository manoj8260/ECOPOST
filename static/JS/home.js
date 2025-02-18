const carousel = document.getElementById('carousel');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');
let scrollPosition = 0;
const itemWidth = 120;  // Adjust item width (including margin)

// Move carousel to the right
nextBtn.addEventListener('click', () => {
  scrollPosition -= itemWidth;
  carousel.style.transform = `translateX(${scrollPosition}px)`; // Smooth transition
  checkButtons();
});

// Move carousel to the left
prevBtn.addEventListener('click', () => {
  scrollPosition += itemWidth;
  carousel.style.transform = `translateX(${scrollPosition}px)`; // Smooth transition
  checkButtons();
});

// Check buttons to disable when at the end or beginning
function checkButtons() {
  prevBtn.disabled = scrollPosition === 0;
  nextBtn.disabled = scrollPosition <= -(carousel.scrollWidth - carousel.offsetWidth);
}

checkButtons(); // Initialize button states on page load



//  update or delete tweet
