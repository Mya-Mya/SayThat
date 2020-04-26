
import winsound
import requests
import glob
import os
from os.path import join
import threading
import time
import sys

VERSION="1.0"

CWD = os.getcwd()
SOUNDS_DIR = join(CWD, "sounds", "")
VOICE_CACHES_DIR = join(CWD, "voice_caches", "")
DATAS_DIR = join(CWD, "datas", "")

API_KEY_FILE_PATH = join(DATAS_DIR, "api_key.txt")
TEXT_FILE_PATH = join(CWD, "text.txt")

VOICE_WAITING_DELTATIME = 1
VOICE_WAITING_TIMEOUT = 30
VOICE_WANTING_COUNT = int(VOICE_WAITING_TIMEOUT / VOICE_WAITING_DELTATIME)

PREPARE_ONLY = "-p" in sys.argv


def read_text_from(path: str) -> str:
    '''テキストファイルの内容を取得する。'''
    with open(path, mode="r", encoding="utf-8") as file:
        text = file.read(-1)
    return text


def get_voice_from_docomotts(textblock: str) -> bytes:
    '''ドコモ開発者サービスからボイスを取得する。'''
    URL = "https://api.apigw.smt.docomo.ne.jp/crayon/v1/textToSpeech?APIKEY={}".format(API_KEY)
    data = {
        "Command": "AP_Synth",
        "SpeakerID": "1",
        "StyleID": "1",
        "SpeechRate": "0.8",
        "AudioFileFormat": "2",
        "TextData": textblock
    }
    headers = {
        "Content-Type": "application/json"
    }
    voice = None
    for i in range(VOICE_WANTING_COUNT):
        time.sleep(VOICE_WAITING_DELTATIME)
        print("ボイスを取得する : {}".format(textblock))
        try:
            response = requests.post(URL, json=data)
        except:
            print("ボイスの取得中に何らかのエラーが起きた : {}".format(textblock))
            continue
        if response.status_code == 200:
            voice = response.content
            print("ボイスの取得完了 : {}".format(textblock))
            break
        print("ボイスを取得できなかった({}) : {}".format(response.status_code, textblock))

    return voice


def play_sound_file(path: str):
    '''音声ファイルを非同期に再生する。'''
    winsound.PlaySound(path, winsound.SND_FILENAME + winsound.SND_NODEFAULT)


def prepare_voices():
    '''ボイスを準備する。読み上げたいテキストのボイスがボイスキャッシュ内に無い場合、取得し利用可能にする。'''
    print("ボイスの準備開始")
    for textblock in textblock_list:
        if not textblock in available_voices:
            # ボイスを取得する
            voice = get_voice_from_docomotts(textblock)
            if voice is None:
                continue

            # ボイスをファイルへ保存する
            path = join(VOICE_CACHES_DIR, textblock)
            with open(path, "wb") as file:
                file.write(voice)

            # ボイスをボイスキャッシュ表へ追加する
            available_voices.add(textblock)

    print("全てのボイスの準備完了")


# API KEYを読み込む
API_KEY = read_text_from(API_KEY_FILE_PATH)

# テキストを読み込む
raw_text = read_text_from(TEXT_FILE_PATH)
if len(raw_text) == 0:
    exit(0)
textblock_list = raw_text.replace("\n", "").split("*")
num_textblock = len(textblock_list)

# ボイスがボイスキャッシュの中にあり準備完了なテキストの集合
available_voices = {os.path.split(path)[1] for path in glob.glob(join(VOICE_CACHES_DIR, "*"))}

# ボイスを準備する。
prepare_voices_thread = threading.Thread(target=prepare_voices)
prepare_voices_thread.start()

if not PREPARE_ONLY:
    print("再生を開始する")
    play_sound_file(join(SOUNDS_DIR, "op.wav"))
    for textblock_idx, textblock in enumerate(textblock_list):
        textblock_info = "{}".format(textblock_idx + 1, num_textblock)
        if textblock_idx != 0:
            play_sound_file(join(SOUNDS_DIR, "se.wav"))

        # ボイスの準備を待つループ
        for waiting_cnt in range(VOICE_WANTING_COUNT):
            if textblock in available_voices:
                print("ボイスを再生する{} : {}".format(textblock_info, textblock))
                play_sound_file(join(VOICE_CACHES_DIR, textblock))
                print("ボイスの再生完了{} : {}".format(textblock_info, textblock))
                break
            print(
                "ボイスが無い{}({}秒目) : {}".format(textblock_info, waiting_cnt * VOICE_WAITING_DELTATIME + 1, textblock))
            time.sleep(VOICE_WAITING_DELTATIME)

    play_sound_file(join(SOUNDS_DIR, "ed.wav"))
    print("全ての再生完了")

prepare_voices_thread.join()
exit(0)
