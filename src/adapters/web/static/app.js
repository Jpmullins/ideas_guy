const log = document.getElementById('log');
const form = document.getElementById('form');
const input = document.getElementById('input');

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
    body: JSON.stringify({ messages: [{ role: 'user', content: text }] })
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

// Starter line to set the tone
pushMsg('bot', 'Idea blast: drop me a problem and I’ll pitch 5 spicy solutions.');

