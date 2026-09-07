cd "/home/fd/Bureau/py/impact de monntreal" && cat << 'EOF' > chat_serveur.py
import os
from datetime import datetime
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

messages = [
    {
        "user": "Admin CF Montréal",
        "text": "Bienvenue sur le portail des supporters du CF Montréal ! ⚽🔵🖤",
        "media": "",
        "time": datetime.now().strftime("%H:%M")
    }
]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CF Montréal - Centre des Supporters & Chat</title>
    <script src="[https://cdn.tailwindcss.com](https://cdn.tailwindcss.com)"></script>
    <link rel="stylesheet" href="[https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css](https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css)">
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen flex flex-col font-sans">

    <header class="bg-black border-b border-blue-600/50 sticky top-0 z-50 shadow-xl">
        <div class="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between">
            <div class="flex items-center space-x-3">
                <div class="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center font-black text-xl text-white shadow-lg shadow-blue-500/30">
                    CFM
                </div>
                <div>
                    <h1 class="text-lg md:text-xl font-bold tracking-wider text-white uppercase">CF Montréal <span class="text-blue-500">Live Hub</span></h1>
                    <p class="text-xs text-slate-400">Espace Supporters & Match en Direct</p>
                </div>
            </div>
            <div class="flex items-center space-x-2">
                <span class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                    <span class="w-2 h-2 mr-1.5 bg-emerald-400 rounded-full animate-pulse"></span> Serveur Actif
                </span>
            </div>
        </div>
    </header>

    <main class="flex-1 max-w-7xl w-full mx-auto p-4 grid grid-cols-1 lg:grid-cols-3 gap-6">

        <div class="space-y-6">
            <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-lg">
                <div class="flex items-center justify-between mb-4">
                    <span class="text-xs font-bold uppercase tracking-wider text-blue-400 flex items-center gap-1.5">
                        <i class="fa-solid fa-calendar-day"></i> Prochain Match MLS
                    </span>
                    <span class="text-xs bg-slate-800 px-2.5 py-1 rounded-md text-slate-300">Stade Saputo</span>
                </div>

                <div class="flex items-center justify-around my-4 py-2 bg-slate-950/50 rounded-xl border border-slate-800/80">
                    <div class="text-center">
                        <div class="w-12 h-12 bg-blue-600/20 rounded-full flex items-center justify-center mx-auto text-xl text-blue-400 font-bold border border-blue-500/30">
                            CFM
                        </div>
                        <span class="text-xs font-semibold mt-2 block">CF Montréal</span>
                    </div>

                    <div class="text-center">
                        <span class="text-xl font-black text-slate-500">VS</span>
                    </div>

                    <div class="text-center">
                        <div class="w-12 h-12 bg-slate-800 rounded-full flex items-center justify-center mx-auto text-xl text-slate-300 font-bold border border-slate-700">
                            TOR
                        </div>
                        <span class="text-xs font-semibold mt-2 block">Toronto FC</span>
                    </div>
                </div>

                <div class="mt-4 pt-3 border-t border-slate-800">
                    <span class="text-xs text-slate-400 block text-center mb-2">Temps restant avant le coup d'envoi :</span>
                    <div id="countdown" class="grid grid-cols-4 gap-2 text-center">
                        <div class="bg-slate-800 p-2 rounded-lg border border-slate-700/50">
                            <span id="cd-days" class="text-lg font-bold text-blue-400 block">00</span>
                            <span class="text-[10px] text-slate-400 uppercase">Jours</span>
                        </div>
                        <div class="bg-slate-800 p-2 rounded-lg border border-slate-700/50">
                            <span id="cd-hours" class="text-lg font-bold text-blue-400 block">00</span>
                            <span class="text-[10px] text-slate-400 uppercase">Heures</span>
                        </div>
                        <div class="bg-slate-800 p-2 rounded-lg border border-slate-700/50">
                            <span id="cd-mins" class="text-lg font-bold text-blue-400 block">00</span>
                            <span class="text-[10px] text-slate-400 uppercase">Mins</span>
                        </div>
                        <div class="bg-slate-800 p-2 rounded-lg border border-slate-700/50">
                            <span id="cd-secs" class="text-lg font-bold text-blue-400 block">00</span>
                            <span class="text-[10px] text-slate-400 uppercase">Secs</span>
                        </div>
                    </div>
                </div>

                <div class="mt-4 text-xs text-slate-400 flex justify-between items-center bg-slate-950/80 p-2.5 rounded-lg border border-slate-800">
                    <span><i class="fa-solid fa-tv text-blue-400 mr-1"></i> Diffusion :</span>
                    <span class="text-slate-200 font-medium">Apple TV (MLS Pass), RDS</span>
                </div>
            </div>

            <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-lg space-y-3">
                <h3 class="text-sm font-bold text-slate-200 uppercase tracking-wider flex items-center gap-2">
                    <i class="fa-solid fa-newspaper text-blue-400"></i> Actualités du Club
                </h3>
                <ul class="text-xs space-y-2 text-slate-300">
                    <li class="p-2.5 bg-slate-950/60 rounded-lg border border-slate-800 hover:border-slate-700 transition">
                        ⚽ Préparation tactique intensive au Centre Nutrilait avant le derby.
                    </li>
                    <li class="p-2.5 bg-slate-950/60 rounded-lg border border-slate-800 hover:border-slate-700 transition">
                        🎟️ Stade Saputo à guichets fermés pour la rencontre de ce week-end.
                    </li>
                </ul>
            </div>
        </div>

        <div class="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-2xl flex flex-col h-[650px] shadow-xl overflow-hidden">
            <div class="bg-slate-950 p-4 border-b border-slate-800 flex items-center justify-between">
                <div class="flex items-center space-x-2">
                    <i class="fa-solid fa-comments text-blue-500 text-lg"></i>
                    <h2 class="font-bold text-slate-100">Salon de Discussion Supporters</h2>
                </div>
                <span id="msg-count" class="text-xs text-slate-400 bg-slate-900 px-2.5 py-1 rounded-full border border-slate-800">0 messages</span>
            </div>

            <div id="chat-box" class="flex-1 overflow-y-auto p-4 space-y-4 bg-slate-950/40">
            </div>

            <div class="p-4 bg-slate-950 border-t border-slate-800">
                <form id="chat-form" class="space-y-2">
                    <div class="flex gap-2">
                        <input type="text" id="username" placeholder="Ton Pseudo..." class="w-1/3 bg-slate-900 text-slate-100 px-3 py-2 rounded-lg border border-slate-800 focus:outline-none focus:border-blue-500 text-sm" required>
                        <input type="url" id="media_url" placeholder="Lien d'image ou vidéo (optionnel)..." class="w-2/3 bg-slate-900 text-slate-100 px-3 py-2 rounded-lg border border-slate-800 focus:outline-none focus:border-blue-500 text-sm">
                    </div>
                    <div class="flex gap-2">
                        <input type="text" id="message" placeholder="Écris ton message ici..." class="flex-1 bg-slate-900 text-slate-100 px-4 py-2.5 rounded-lg border border-slate-800 focus:outline-none focus:border-blue-500 text-sm" required autocomplete="off">
                        <button type="submit" class="bg-blue-600 hover:bg-blue-500 text-white font-bold px-5 py-2.5 rounded-lg transition flex items-center gap-2 text-sm shadow-lg shadow-blue-600/20">
                            <span>Envoyer</span> <i class="fa-solid fa-paper-plane text-xs"></i>
                        </button>
                    </div>
                </form>
            </div>
        </div>

    </main>

    <script>
        function updateCountdown() {
            const matchDate = new Date();
            matchDate.setDate(matchDate.getDate() + (6 - matchDate.getDay() + 7) % 7);
            matchDate.setHours(19, 30, 0, 0);

            const now = new Date();
            const diff = matchDate - now;

            if (diff > 0) {
                const d = Math.floor(diff / (1000 * 60 * 60 * 24));
                const h = Math.floor((diff / (1000 * 60 * 60)) % 24);
                const m = Math.floor((diff / 1000 / 60) % 60);
                const s = Math.floor((diff / 1000) % 60);

                document.getElementById('cd-days').innerText = String(d).padStart(2, '0');
                document.getElementById('cd-hours').innerText = String(h).padStart(2, '0');
                document.getElementById('cd-mins').innerText = String(m).padStart(2, '0');
                document.getElementById('cd-secs').innerText = String(s).padStart(2, '0');
            }
        }
        setInterval(updateCountdown, 1000);
        updateCountdown();

        const chatBox = document.getElementById('chat-box');
        const chatForm = document.getElementById('chat-form');
        const usernameInput = document.getElementById('username');
        const messageInput = document.getElementById('message');
        const mediaInput = document.getElementById('media_url');
        const msgCountElem = document.getElementById('msg-count');

        if (localStorage.getItem('cfm_username')) {
            usernameInput.value = localStorage.getItem('cfm_username');
        }

        let lastCount = 0;

        function renderMedia(url) {
            if (!url) return '';
            const cleanUrl = url.trim();
            if (cleanUrl.match(/\.(jpeg|jpg|gif|png|webp)/i)) {
                return `<img src="${cleanUrl}" class="mt-2 rounded-lg max-h-48 w-full object-cover border border-slate-700/50" alt="Média partagé" onerror="this.style.display='none'">`;
            } else if (cleanUrl.match(/\.(mp4|webm)/i)) {
                return `<video controls src="${cleanUrl}" class="mt-2 rounded-lg max-h-48 w-full border border-slate-700/50"></video>`;
            } else {
                return `<a href="${cleanUrl}" target="_blank" class="mt-2 block text-xs text-blue-400 underline break-all"><i class="fa-solid fa-link"></i> Voir le lien attaché</a>`;
            }
        }

        async function fetchMessages() {
            try {
                const res = await fetch('/api/messages');
                const data = await res.json();
                
                msgCountElem.innerText = `${data.length} message${data.length > 1 ? 's' : ''}`;

                if (data.length !== lastCount) {
                    chatBox.innerHTML = '';
                    data.forEach(msg => {
                        const isMe = msg.user === usernameInput.value.trim();
                        const div = document.createElement('div');
                        div.className = `flex flex-col ${isMe ? 'items-end' : 'items-start'}`;
                        
                        div.innerHTML = `
                            <div class="max-w-xs md:max-w-md rounded-2xl px-4 py-2.5 ${isMe ? 'bg-blue-600 text-white rounded-br-none shadow-md shadow-blue-600/10' : 'bg-slate-900 text-slate-100 border border-slate-800 rounded-bl-none'}">
                                <div class="flex items-center justify-between gap-4 mb-1">
                                    <span class="text-xs font-bold ${isMe ? 'text-blue-200' : 'text-blue-400'}">${msg.user}</span>
                                    <span class="text-[10px] opacity-60">${msg.time || ''}</span>
                                </div>
                                <p class="text-sm break-words">${msg.text}</p>
                                ${renderMedia(msg.media)}
                            </div>
                        `;
                        chatBox.appendChild(div);
                    });
                    chatBox.scrollTop = chatBox.scrollHeight;
                    lastCount = data.length;
                }
            } catch (err) {
                console.error(err);
            }
        }

        chatForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const user = usernameInput.value.trim();
            const text = messageInput.value.trim();
            const media = mediaInput.value.trim();

            if (!user || !text) return;

            localStorage.setItem('cfm_username', user);

            await fetch('/api/send', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ user, text, media })
            });

            messageInput.value = '';
            mediaInput.value = '';
            fetchMessages();
        });

        setInterval(fetchMessages, 2000);
        fetchMessages();
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/messages', methods=['GET'])
def get_messages():
    return jsonify(messages)

@app.route('/api/send', methods=['POST'])
def send_message():
    data = request.get_json() or {}
    user = data.get('user', 'Supporter')
    text = data.get('text', '')
    media = data.get('media', '')
    now = datetime.now().strftime("%H:%M")

    if text:
        messages.append({
            'user': user,
            'text': text,
            'media': media,
            'time': now
        })
        if len(messages) > 100:
            messages.pop(0)
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
EOF
git add chat_serveur.py && git commit -m "Mise a jour complete avec compte a rebours et partage media" && git push origin main
