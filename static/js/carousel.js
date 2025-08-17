// 🧵 Carousel Scroll Logic
const track = document.getElementById('galleryTrack');
const prevBtn = document.querySelector('.prev-btn');
const nextBtn = document.querySelector('.next-btn');

let scrollIndex = 0;

// Wait for items to load before calculating width
window.addEventListener('load', () => {
  const itemWidth = track.children[0]?.offsetWidth || 0;

  prevBtn.addEventListener('click', () => {
    scrollIndex = Math.max(scrollIndex - 3, 0);
    track.style.transform = `translateX(-${scrollIndex * itemWidth}px)`;
  });

  nextBtn.addEventListener('click', () => {
    const maxIndex = track.children.length - 3;
    scrollIndex = Math.min(scrollIndex + 3, maxIndex);
    track.style.transform = `translateX(-${scrollIndex * itemWidth}px)`;
  });
});

// 🧩 Load Footer Items from JSON
const footerItems = JSON.parse(document.getElementById('footerItemsData').textContent);

footerItems.forEach(item => {
  const galleryItem = document.createElement('div');
  galleryItem.className = 'gallery-item';
  galleryItem.innerHTML = `
    <img src="/static/images/gallery/${item.image}" alt="${item.label}">
    <div class="label">${item.label}</div>
    <div class="price">$${item.price}</div>
  `;
  galleryItem.onclick = () => openRemedyModal(item.id);
  track.appendChild(galleryItem);
});

// 🌀 Modal Logic
function openRemedyModal(id) {
  const item = footerItems.find(p => p.id === id);
  if (!item) return;

  document.getElementById('modalLabel').textContent = item.label;
  document.getElementById('modalImage').src = `/static/images/gallery/${item.image}`;
  document.getElementById('modalDescription').textContent = item.description;
  document.getElementById('modalPrice').textContent = `$${item.price}`;
  document.getElementById('modalLink').href = item.link;

  document.getElementById('remedyModal').style.display = 'flex';
}

function closeRemedyModal() {
  document.getElementById('remedyModal').style.display = 'none';
}

// ⌨️ Escape Key to Close Modal
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') closeRemedyModal();
});
