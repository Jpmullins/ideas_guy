const log = document.getElementById('log');
const form = document.getElementById('form');
const input = document.getElementById('input');
const select = document.getElementById('character');
const modelSelect = document.getElementById('model');
const nameEl = document.getElementById('char-name');
const descEl = document.getElementById('char-desc');
const avatarEl = document.getElementById('avatar');

let currentCharacter = null;

function pushMsg(role, text) {
  const el = document.createElement('div');
  el.className = `msg ${role}`;
  const roleBadge = document.createElement('div');
  roleBadge.className = 'role';
  roleBadge.textContent = role === 'user' ? 'U' : 'IG';
  const bubble = document.createElement('div');
  bubble.className = 'bubble';
  // simple markdown-ish bullets
  const asHtml = text
    .replace(/\n\n/g, '\n')
    .replace(/\n- /g, '<br>• ')
    .replace(/\n/g, '<br>');
  bubble.innerHTML = asHtml;
  el.appendChild(roleBadge);
  el.appendChild(bubble);
  log.appendChild(el);
  log.scrollTo({ top: log.scrollHeight, behavior: 'smooth' });
}

async function send(text) {
  pushMsg('user', text);
  input.value = '';
  const res = await fetch('/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      character_id: currentCharacter?.id,
      model_provider: modelSelect.selectedOptions[0]?.dataset.provider,
      model_name: modelSelect.value,
      messages: [{ role: 'user', content: text }]
    })
  });
  if (!res.ok) {
    pushMsg('bot', 'Hmm. The idea machine coughed. Check the server logs.');
    return;
  }
  const data = await res.json();
  pushMsg('bot', data.reply);
}

form.addEventListener('submit', (e) => {
  e.preventDefault();
  const text = (input.value || '').trim();
  if (!text) return;
  send(text);
});

async function loadCharacters() {
  const res = await fetch('/api/characters');
  if (!res.ok) return;
  const chars = await res.json();
  select.innerHTML = '';
  for (const c of chars) {
    const opt = document.createElement('option');
    opt.value = c.id; opt.textContent = c.name;
    select.appendChild(opt);
  }
  // pick first character by default
  const firstId = chars[0]?.id;
  if (firstId) await setCharacter(firstId);
}

async function setCharacter(id) {
  const res = await fetch(`/api/characters/${id}`);
  if (!res.ok) return;
  currentCharacter = await res.json();
  nameEl.textContent = currentCharacter.name;
  descEl.textContent = currentCharacter.description;
  if (avatarEl) avatarEl.src = currentCharacter.avatar || '/assets/ideas_guy.png';
  log.innerHTML = '';
  if (currentCharacter.greeting) pushMsg('bot', currentCharacter.greeting);
}

select.addEventListener('change', (e) => setCharacter(e.target.value));

async function loadModels() {
  const res = await fetch('/api/models');
  if (!res.ok) return;
  const models = await res.json();
  modelSelect.innerHTML = '';
  for (const m of models) {
    const opt = document.createElement('option');
    opt.value = m.id;
    opt.dataset.provider = m.provider;
    opt.textContent = `${m.name} — ${m.provider}`;
    modelSelect.appendChild(opt);
  }
}

(async function init(){
  await Promise.all([loadModels(), loadCharacters()]);
})();
