from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import pyautogui

pyautogui.PAUSE = 0.005

class Handler(BaseHTTPRequestHandler):
    def _set_response(self, code=200):
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

    def do_POST(self):
        if self.path != '/parry':
            self._set_response(404)
            self.wfile.write(json.dumps({'status': 'not_found'}).encode('utf-8'))
            return

        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length).decode('utf-8') if length > 0 else ''
        try:
            data = json.loads(body) if body else {}
        except Exception:
            data = {}

        method = (data.get('method') or 'lmb').lower()

        try:
            if method == 'ping':
                resp = {'status': 'ok', 'action': 'ping'}
                self._set_response(200)
            else:
                if method == 'f':
                    pyautogui.press('f')
                elif method == 'lmb_strong':
                    pyautogui.mouseDown(button='left')
                    pyautogui.mouseUp(button='left')
                    pyautogui.mouseDown(button='left')
                    pyautogui.mouseUp(button='left')
                else:
                    pyautogui.mouseDown(button='left')
                    pyautogui.mouseUp(button='left')
                resp = {'status': 'ok', 'action': method}
                self._set_response(200)
        except Exception as e:
            resp = {'status': 'error', 'error': str(e)}
            self._set_response(500)

        self.wfile.write(json.dumps(resp).encode('utf-8'))

if __name__ == '__main__':
    HOST = '127.0.0.1'
    PORT = 8765
    server = HTTPServer((HOST, PORT), Handler)
    print(f'Local input server listening on http://{HOST}:{PORT}/parry')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('Shutting down')
        server.shutdown()
