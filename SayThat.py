import winsound
import glob
import os
from os.path import join
import threading
import time
from argparse import ArgumentParser
import gateway
import constants
import re

print("SayThat {} (C)Mya-Mya(2020)".format(constants.VERSION))

argparser = ArgumentParser()
argparser.add_argument("-p", action="store_true", dest="prepare_only")
argparser.add_argument("-a", action="store_true", dest="play_all_voice")
argparser.add_argument("-t", default=join(constants.CWD, "text.txt"), dest="text_file_path")
args = argparser.parse_args()


def prepare_voices():
    '''ボイスを準備する。読み上げたいテキストのボイスがボイスキャッシュ内に無い場合、取得し利用可能にする。'''
    print("ボイスの準備開始")
    for textblock in textblock_list:
        if not textblock in available_voices:
            # ボイスを取得する
            voice = gateway.get_voice_from_docomotts(textblock)
            if voice is None:
                continue

            # ボイスをファイルへ保存する
            path = join(constants.VOICE_CACHES_DIR, textblock)
            with open(path, "wb") as file:
                file.write(voice)

            # ボイスをボイスキャッシュ表へ追加する
            available_voices.add(textblock)

    print("全てのボイスの準備完了")


# テキストを読み込む
raw_text = gateway.read_text_from(args.text_file_path)
if len(raw_text) == 0:
    exit(0)
textblock_list = [textblock for textblock in re.split("。|、", raw_text.replace("\n", "")) if not textblock == ""]
num_textblock = len(textblock_list)

# ボイスがボイスキャッシュの中にあり準備完了なテキストの集合
available_voices = {os.path.split(path)[1] for path in glob.glob(join(constants.VOICE_CACHES_DIR, "*"))}

# ボイスを準備する。
prepare_voices_thread = threading.Thread(target=prepare_voices)
prepare_voices_thread.start()

# 読むテキストを表示する。
print("-----")
print(raw_text)
print("-----")

if args.play_all_voice:
    print("-aコマンド : 全てのボイスを準備してから再生を開始する")
    prepare_voices_thread.join()

if not args.prepare_only:
    print("再生を開始する")
    gateway.play_sound_file(join(constants.SOUNDS_DIR, "op.wav"))
    for textblock_idx, textblock in enumerate(textblock_list):
        textblock_info = "({}/{})".format(textblock_idx + 1, num_textblock)

        # ボイスの準備を待つループ
        for waiting_cnt in range(constants.VOICE_WANTING_COUNT):
            if textblock in available_voices:
                print("ボイスを再生する{} : {}".format(textblock_info, textblock))
                gateway.play_sound_file(join(constants.VOICE_CACHES_DIR, textblock))
                print("ボイスの再生完了{} : {}".format(textblock_info, textblock))
                break
            print(
                "ボイスが無い{}({}秒目) : {}".format(textblock_info, waiting_cnt * constants.VOICE_WAITING_DELTATIME + 1,
                                             textblock))
            time.sleep(constants.VOICE_WAITING_DELTATIME)

    gateway.play_sound_file(join(constants.SOUNDS_DIR, "ed.wav"))
    print("全ての再生完了")

prepare_voices_thread.join()
exit(0)
