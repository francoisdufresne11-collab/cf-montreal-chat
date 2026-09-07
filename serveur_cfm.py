import base64
import http.server
import socketserver
import sys
import zlib

def safe_decompress(emb_b64):
    try:
        raw_data = base64.b64decode(emb_b64)
    except Exception as e:
        print(f"Erreur de décodage Base64 : {e}")
        return b"<h1>Erreur de decodage Base64</h1>"

    # Essai avec les différents formats de fenêtre zlib (zlib standard, raw deflate, gzip)
    for wbits in (zlib.MAX_WBITS, -zlib.MAX_WBITS, zlib.MAX_WBITS | 32):
        try:
            return zlib.decompress(raw_data, wbits)
        except zlib.error:
            continue

    # Si aucune décompression n'a fonctionné, retourne les données brutes
    return raw_data

# Page HTML de secours si _EMB est corrompu
HTML_CONTENT = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CF Montréal - Arena IA</title>
    <style>
        body { font-family: system-ui, -apple-system, sans-serif; background-color: #0a0a0c; color: #ffffff; text-align: center; margin: 0; padding: 20px; }
        .card { background: #141824; border: 1px solid #1d283a; border-radius: 12px; max-width: 600px; margin: 50px auto; padding: 30px; box-shadow: 0 8px 24px rgba(0,0,0,0.5); }
        h1 { color: #00529b; margin-bottom: 10px; }
        .badge { background: #00529b; color: white; padding: 6px 16px; border-radius: 20px; font-weight: bold; font-size: 0.85em; display: inline-block; margin-bottom: 20px; }
        #timer { font-size: 2.2em; font-weight: bold; color: #38bdf8; margin: 25px 0; }
        .status { color: #94a3b8; font-size: 0.9em; }
    </style>
</head>
<body>
    <div class="card">
        <span class="badge">CF Montréal / Arena IA</span>
        <h1>Serveur Match & Diffusion</h1>
        <p>Le serveur est en ligne et fonctionnel.</p>
        <div id="timer">--:--:--</div>
        <p class="status">Port 5000 &bull; Diffusion active</p>
    </div>
    <script>
        function updateClock() {
            const now = new Date();
            document.getElementById('timer').innerText = now.toLocaleTimeString('fr-CA');
        }
        setInterval(updateClock, 1000);
        updateClock();
    </script>
</body>
</html>"""

# Encapsulation dynamique propre pour garantir l'intégrité
_EMB = base64.b64encode(zlib.compress(HTML_CONTENT.encode('utf-8'))).decode('utf-8')

PAGE_BYTES = safe_decompress(_EMB)

PORT = 5000

class HTTPHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(PAGE_BYTES)))
        self.end_headers()
        self.wfile.write(PAGE_BYTES)

    def log_message(self, format, *args):
        print(f"[{self.log_date_time_string()}] {args[0]}")

if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), HTTPHandler) as httpd:
        print(f"Serveur CFM prêt sur http://localhost:{PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nFermeture du serveur.")
            sys.exit(0)