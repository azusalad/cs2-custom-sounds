from http.server import HTTPServer, BaseHTTPRequestHandler
import json

from config import *


class GSIHandler(BaseHTTPRequestHandler):
  def json_get(self, data, keys, default_value=""):
    #print(f"json get called with {keys}")
    current = data
    #print(f"current is {current}")
    for key in keys[:-1]:
      #print(f"narrowing with {key}")
      current = current.get(key, {})
      if not isinstance(current, dict):
        return default_value
      #print(f"current is {current}")
    #print(f"returning {current.get(keys[-1], default_value)}\n\n")
    return current.get(keys[-1], default_value)

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

    # Round end sound
    if self.json_get(data, ["previously","round","phase"]) == "live":
      if self.json_get(data, ["round","phase"]) == "over":
        if self.json_get(data, ["player","team"]) == self.json_get(data, ["round","win_team"]):
          # Round win
          if self.json_get(data, ["previously","player","match_stats","mvps"]):
            print("Mvp won")
          else:
            print("Round won")
        else:
          # Round loss
          print("Round loss")

    # Kill sound
    if self.json_get(data, ["previously", "player", "match_stats", "kills"]):
      print("Kill")
    
    # Death sound
    if self.json_get(data, ["previously", "player", "match_stats", "deaths"]):
      print("Death")

    # Print the data nicely
    # print("=" * 60)
    # print(json.dumps(data, indent=2))
    # print("=" * 60)
    # print()

    # Send response back to the game
    self.send_response(200)
    self.end_headers()

  def log_message(self, format, *args):
    # Suppress default HTTP log messages to keep output clean
    pass


def main():
  server_address = ('127.0.0.1', PORT)
  httpd = HTTPServer(server_address, GSIHandler)
  print(f"GSI Server listening on {server_address[0]}:{server_address[1]}")
  print("Waiting for data...\n")
  
  try:
    httpd.serve_forever()
  except KeyboardInterrupt:
    print("\nServer stopped.")
    httpd.server_close()


if __name__ == '__main__':
  main()