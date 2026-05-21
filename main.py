from http.server import HTTPServer, BaseHTTPRequestHandler
from pygame import mixer
from pathlib import Path
import json
import logging

from config import *

class Sounds:
  SOUND_MAP = {
    "kill": KILL_SOUND,
    "death": DEATH_SOUND,
    "loss": LOSS_SOUND,
    "win": WIN_SOUND,
    "mvp": MVP_SOUND,
    "freeze": FREEZETIME_SOUND,
    "start": START_SOUND,
    "bomb": BOMB_SOUND
  }

  # Sounds that require stopping start and bomb sounds first
  STOPS_ROUND_START = {"loss", "win", "mvp", "bomb"}

  def __init__(self, logger):
    mixer.init()
    self.logger = logger
    self.sounds = {}
    for name, t in self.SOUND_MAP.items():
      filepath = t[0]
      volume = t[1]
      a = Path(filepath)
      if a.exists() and filepath != "":
        sound = mixer.Sound(filepath)
      else:
        sound = mixer.Sound("sounds/blank.wav")
      sound.set_volume(volume)
      self.sounds[name] = sound

  def play_sound(self, sound):
    if sound in self.STOPS_ROUND_START:
      self.sounds["start"].stop()
      self.sounds["bomb"].stop()
    if sound in self.sounds:
      self.logger.debug(f"Playing {sound} from {self.SOUND_MAP[sound]}")
      self.sounds[sound].play()

class GSIHandler(BaseHTTPRequestHandler):
  logger = None
  sounds = None

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

    if not self.json_get(data, ["previously", "player", "name"]): # Avoid sounds from playing upon player change
      # Kill sound
      if self.json_get(data, ["previously", "player", "match_stats", "kills"]):
        self.logger.info("Kill")
        self.sounds.play_sound("kill")
      
      # Death sound
      if self.json_get(data, ["previously", "player", "match_stats", "deaths"]):
        self.logger.info("Death")
        self.sounds.play_sound("death")
      
      # Round end sound
      if self.json_get(data, ["previously", "round", "phase"]) == "live":
        if self.json_get(data, ["round", "phase"]) == "over":
          if self.json_get(data, ["player", "team"]) == self.json_get(data, ["round", "win_team"]):
            # Round win
            if self.json_get(data, ["previously", "player", "match_stats", "mvps"]):
              self.logger.info("Mvp won")
              self.sounds.play_sound("mvp")
            else:
              self.logger.info("Round won")
              self.sounds.play_sound("win")
          else:
            # Round loss
            self.logger.info("Round loss")
            self.sounds.play_sound("loss")

      # Freeze time sound
      elif self.json_get(data, ["previously", "round", "phase"]) == "over":
        if self.json_get(data, ["round", "phase"]) == "freezetime":
          self.logger.info("Freeze time")
          self.sounds.play_sound("freeze")
      
      # Round start sound
      elif self.json_get(data, ["previously", "round", "phase"]) == "freezetime":
        if self.json_get(data, ["round", "phase"]) == "live":
          self.logger.info("Round start")
          self.sounds.play_sound("start")
      
      # Bomb sound
      elif self.json_get(data, ["added", "round", "bomb"]):
        self.logger.info("Bomb planted")
        self.sounds.play_sound("bomb")

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
  sounds = Sounds(logger)
  GSIHandler.sounds = sounds
  logger.info(f"GSI Server listening on {server_address[0]}:{server_address[1]}")
  logger.info("Waiting for data...\n")
  
  try:
    httpd.serve_forever()
  except KeyboardInterrupt:
    logger.info("\nServer stopped.")
    httpd.server_close()


if __name__ == '__main__':
  main()