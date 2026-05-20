from http.server import HTTPServer, BaseHTTPRequestHandler
from playsound3 import playsound
from pathlib import Path
import json
import logging

from config import *


class GSIHandler(BaseHTTPRequestHandler):
  logger = None

  def play_sound(self, path):
    a = Path(path)
    if a.exists() and path != "":
      self.logger.debug(f"Playing sound at path {path}")
      playsound(path, block=False)
    else:
      self.logger.error(f"File does not exist {path}")


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
      self.logger.error("Failed to decode JSON")
      self.send_response(400)
      self.end_headers()
      return

    # Print the data nicely
    self.logger.debug(json.dumps(data, indent=2))
    # print("=" * 60)
    # print(json.dumps(data, indent=2))
    # print("=" * 60)
    # print()

    if not self.json_get(data, ["previously", "player", "name"]): # Avoid sounds from playing upon player change
      # Kill sound
      if self.json_get(data, ["previously", "player", "match_stats", "kills"]):
        self.logger.info("Kill")
        self.play_sound(KILL_SOUND)
      
      # Death sound
      if self.json_get(data, ["previously", "player", "match_stats", "deaths"]):
        self.logger.info("Death")
        self.play_sound(DEATH_SOUND)
      
      # Round end sound
      if self.json_get(data, ["previously","round","phase"]) == "live":
        if self.json_get(data, ["round","phase"]) == "over":
          if self.json_get(data, ["player","team"]) == self.json_get(data, ["round","win_team"]):
            # Round win
            if self.json_get(data, ["previously","player","match_stats","mvps"]):
              self.logger.info("Mvp won")
              self.play_sound(MVP_SOUND)
            else:
              self.logger.info("Round won")
              self.play_sound(WIN_SOUND)
          else:
            # Round loss
            self.logger.info("Round loss")
            self.play_sound(LOSS_SOUND)



    # Send response back to the game
    self.send_response(200)
    self.end_headers()

  def log_message(self, format, *args):
    # Suppress default HTTP log messages to keep output clean
    pass


def main():
  logger = logging.getLogger(__name__)
  if DEBUG:
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.DEBUG)
  else:
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)
  server_address = ('127.0.0.1', PORT)
  httpd = HTTPServer(server_address, GSIHandler)
  GSIHandler.logger = logger
  logger.info(f"GSI Server listening on {server_address[0]}:{server_address[1]}")
  logger.info("Waiting for data...\n")
  
  try:
    httpd.serve_forever()
  except KeyboardInterrupt:
    logger.info("\nServer stopped.")
    httpd.server_close()


if __name__ == '__main__':
  main()