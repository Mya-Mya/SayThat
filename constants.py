import os
from os.path import join

VERSION = "1.4"

VOICE_WAITING_DELTATIME = 1
VOICE_WAITING_TIMEOUT = 30
VOICE_WANTING_COUNT = int(VOICE_WAITING_TIMEOUT / VOICE_WAITING_DELTATIME)

CWD = os.path.dirname(__file__)
SOUNDS_DIR = join(CWD, "sounds", "")
VOICE_CACHES_DIR = join(CWD, "voice_caches", "")
DATAS_DIR = join(CWD, "datas", "")

API_KEY_FILE_PATH = join(DATAS_DIR, "api_key.txt")