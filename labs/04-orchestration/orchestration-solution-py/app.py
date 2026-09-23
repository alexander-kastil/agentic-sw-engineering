import html
import math
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from string import Template
from urllib.parse import parse_qs, urlparse

from converter import celsius_to_fahrenheit, fahrenheit_to_celsius

HOST = "127.0.0.1"
PORT = 8000
FOLDER = Path(__file__).parent
PAGE = Template((FOLDER / "index.html").read_text(encoding="utf-8"))
STYLES = (FOLDER / "styles.css").read_bytes()


def parse_number(text):
    try:
        number = float(text)
    except ValueError:
        return None
    return number if math.isfinite(number) else None


def convert(query):
    celsius = query.get("celsius", [""])[0].strip()
    fahrenheit = query.get("fahrenheit", [""])[0].strip()
    direction = query.get("convert", [""])[0]
    message = ""

    if direction == "celsius" and celsius:
        number = parse_number(celsius)
        if number is None:
            message = "Enter a valid number"
        else:
            fahrenheit = f"{celsius_to_fahrenheit(number):.1f}"
    elif direction == "fahrenheit" and fahrenheit:
        number = parse_number(fahrenheit)
        if number is None:
            message = "Enter a valid number"
        else:
            celsius = f"{fahrenheit_to_celsius(number):.1f}"

    return celsius, fahrenheit, message


class ConverterHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        url = urlparse(self.path)
        if url.path == "/":
            celsius, fahrenheit, message = convert(parse_qs(url.query))
            body = PAGE.safe_substitute(
                celsius=html.escape(celsius),
                fahrenheit=html.escape(fahrenheit),
                message=html.escape(message),
            ).encode("utf-8")
            self.send_body(body, "text/html; charset=utf-8")
        elif url.path == "/styles.css":
            self.send_body(STYLES, "text/css; charset=utf-8")
        else:
            self.send_error(404)

    def send_body(self, body, content_type):
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main():
    server = HTTPServer((HOST, PORT), ConverterHandler)
    print(f"Temperature converter running at http://{HOST}:{PORT}/")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
