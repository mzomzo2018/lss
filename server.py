from PySide6.QtCore import QCoreApplication
from http.server import HTTPServer, SimpleHTTPRequestHandler
import sys
import threading
import webbrowser
import os

from PySide6.QtNetwork import QLocalServer


def start_http_server():
    # Start HTTP server on port 8000 to serve files from current directory
    server = HTTPServer(('127.0.0.1', 8000), SimpleHTTPRequestHandler)
    print("HTTP server started on http://127.0.0.1:8000")
    server.serve_forever()


def main():
    app = QCoreApplication(sys.argv)

    # Start local server
    server = QLocalServer()
    if not server.listen("LSS_Server"):
        print("Could not start server")
        return

    # Start HTTP server in a separate thread
    http_thread = threading.Thread(target=start_http_server, daemon=True)
    http_thread.start()

    # Open browser to mainwindow.py
    index_path = os.path.join(os.path.dirname(__file__), 'mainwindow.py')
    if os.path.exists(index_path):
        webbrowser.open('http://127.0.0.1:8000/mainwindow.py')
    else:
        print("mainwindow.py not found")
        return

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
