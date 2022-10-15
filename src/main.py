from multiprocessing import Process
import os
import time
import simplematrixbotlib as botlib

from matrix.listener import listener_start
from api.api import api_start
import config

creds = botlib.Creds(
    config.HOMESERVER,
    config.LOGIN,
    config.PASSWORD,
    session_stored_file="./.matrix_session/session.txt"
)

cfg = botlib.Config()
cfg.encryption_enabled = True
cfg.emoji_verify = False
cfg.ignore_unverified_devices = True
cfg.store_path = './.matrix_session/crypto_store/'
cfg.allowlist = []
cfg.join_on_invite = False

bot = botlib.Bot(creds, cfg)

listener = Process(target=listener_start, args=(bot,))
flask_api = Process(target=api_start, args=(bot,))

listener.start()
flask_api.start()

while True:
    if not listener.is_alive():
        print("Listener is not alive")
        flask_api.terminate()
        exit(1)
    time.sleep(1)
    if not flask_api.is_alive():
        print("API is not alive")
        listener.terminate()
        exit(1)
    time.sleep(1)