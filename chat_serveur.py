import os
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

messages = [
    {"user": "Robot CF Montréal", "text": "Bienvenue dans le chat des supporters du CF Montréal ! ⚽🔵🖤"}
]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CF Montréal - Chat en Direct</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="h-screen flex flex-col bg-slate-950 text-white font-sans">
    <header class="bg-black border-b-2 border-blue-600 p-4 shadow-lg flex items-center justify-between px-6">
        <div class="flex items-center space-x-3">
            <span class="text-3xl">⚽</span>
            <h1 class="text-xl md:text-2xl font-bold tracking-wider text-white">CF MONTRÉAL <span class="text-blue-500">CHAT</span></h1>
        </div>
        <span class="bg-blue-600 text-xs px-3 py-1 rounded-full uppercase tracking-wider font-semibold">En Direct</span>
    </header>

    <main class="flex-1 overflow-y-auto p-4 space-y-4 max-w-4xl w-full mx-auto" id="chat-box">
    </main>

    <footer class="bg-slate-900 border-t border-slate-800 p-4">
        <form id="chat-form" class="max-w-4xl mx-auto flex flex-col sm:flex-row gap-2">
            <input type="text" id="username" placeholder="Ton pseudo..." class="bg-slate-800 text-white px-4 py-2 rounded-lg border border-slate-700 focus:outline-none focus:border-blue-500 sm:w-1/4" required>
            <input type="text" id="message" placeholder="Écris ton message ici..." class="bg-slate-800 text-white px-4 py-2 rounded-lg border border-slate-700 focus:outline-none focus:border-blue-500 flex-1" required autocomplete="off">
            <button type="submit" class="bg-blue-600 hover:bg-blue-700 text-white font-bold px-6 py-2 rounded-lg transition duration-200">Envoyer</button>
        </form>
    </footer>

    <script>
        const chatBox = document.getElementById('chat-box');
        const chatForm = document.getElementById('chat-form');
        const usernameInput = document.getElementById('username');
        const messageInput = document.getElementById('message');

        if (localStorage.getItem('cfm_pseudo')) {
            usernameInput.value = localStorage.getItem('cfm_pseudo');
        }

        let lastCount = 0;

        async function fetchMessages() {
            try {
                const res = await fetch('/api/messages');
                const data = await res.json();
                
                if (data.length !== lastCount) {
                    chatBox.innerHTML = '';
                    data.forEach(msg => {
                        const div = document.createElement('div');
                        const isMe = msg.user === usernameInput.value.trim();
                        div.className = `flex flex-col ${isMe ? 'items-end' : 'items-start'}`;
                        div.innerHTML = `
                            <div class="max-w-xs md:max-w-md rounded-2xl px-4 py-2 ${isMe ? 'bg-blue-600 text-white rounded-br-none' : 'bg-slate-800 text-slate-200 border border-slate-700 rounded-bl-none'}">
                                <span class="text-xs text-blue-300 font-bold block">${msg.user}</span>
                                <p class="text-sm mt-1 break-words">${msg.text}</p>
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

            if (!user || !text) return;

            localStorage.setItem('cfm_pseudo', user);

            await fetch('/api/send', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ user, text })
            });

            messageInput.value = '';
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
    user = data.get('user', 'Anonyme')
    text = data.get('text', '')
    if text:
        messages.append({'user': user, 'text': text})
        if len(messages) > 100:
            messages.pop(0)
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
