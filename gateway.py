import time
import requests
import constants
import os
import winsound


# 必要なディレクトリがあるか確認
def check_dir_existence(dir_path):
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)


check_dir_existence(constants.VOICE_CACHES_DIR)
check_dir_existence(constants.DATAS_DIR)


def read_text_from(path: str) -> str:
    '''テキストファイルの内容を取得する。'''
    with open(path, mode="r", encoding="utf-8") as file:
        text = file.read(-1)
    return text


DOCOMOTTS_API_KEY = read_text_from(constants.API_KEY_FILE_PATH)


def get_voice_from_docomotts(textblock: str) -> bytes:
    '''ドコモ開発者サービスからボイスを取得する。'''
    URL = "https://api.apigw.smt.docomo.ne.jp/crayon/v1/textToSpeech?APIKEY={}".format(DOCOMOTTS_API_KEY)
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
    for i in range(constants.VOICE_WANTING_COUNT):
        time.sleep(constants.VOICE_WAITING_DELTATIME)
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
