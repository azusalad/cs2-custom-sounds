from http.server import HTTPServer, BaseHTTPRequestHandler
import json


class GSIHandler(BaseHTTPRequestHandler):
  def do_POST(self):
    # Read the content length and body
    content_length = int(self.headers['Content-Length'])
    body = self.rfile.read(content_length)
    
    # Parse JSON data
    try:
      data = json.loads(body)
    except json.JSONDecodeError:
      print("Failed to decode JSON")
      self.send_response(400)
      self.end_headers()
      return

    # Print the data nicely
    print("=" * 60)
    print(json.dumps(data, indent=2))
    print("=" * 60)
    print()

    # Send response back to the game
    self.send_response(200)
    self.end_headers()

  def log_message(self, format, *args):
    # Suppress default HTTP log messages to keep output clean
    pass


def main():
  server_address = ('127.0.0.1', 4000)
  httpd = HTTPServer(server_address, GSIHandler)
  print(f"GSI Server listening on {server_address[0]}:{server_address[1]}")
  print("Waiting for CS:GO data...\n")
  
  try:
    httpd.serve_forever()
  except KeyboardInterrupt:
    print("\nServer stopped.")
    httpd.server_close()


if __name__ == '__main__':
  main()