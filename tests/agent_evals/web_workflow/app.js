const query = document.querySelector('#query');
const category = document.querySelector('#category');
const entries = [...document.querySelectorAll('article[data-topic]')];
function update() {
  let count = 0;
  for (const entry of entries) {
    const matches = entry.querySelector('h2').textContent.toLowerCase().includes(query.value.toLowerCase()) && (category.value === 'all' || entry.dataset.topic === category.value);
    entry.hidden = !matches;
    if (matches) count++;
  }
  document.querySelector('#count').textContent = `${count} journal ${count === 1 ? 'entry' : 'entries'}`;
  document.querySelector('#empty').hidden = count !== 0;
}
query.addEventListener('input', update);
category.addEventListener('change', update);
update();
