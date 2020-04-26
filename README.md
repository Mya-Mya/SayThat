## 概要
任意のテキストを読み上げてくれる。

## システム要件
* OS : Windows
* Python : 3.7 以上
* ライブラリ : なし
* ネットワーク環境
* API : 音声合成API(ドコモ開発者サービス音声合成API【Powered by NTTテクノクロス】)

## ファイルの説明
### 準備が必要
* `datas/api_key.txt`にドコモ開発者サービス音声合成API【Powered by NTTテクノクロス】のAPIキーを書いておくこと。
* `text.txt`に読ませたいテキストを書いておくこと。

いずれも`.gitignore`に登録されている。
### アプリが使用
* `voice_caches/` : ボイスキャッシュの保存先。
* `sounds/` : 音の保存先。
### `text.txt`の書き方
読み上げてほしいテキストを書く。
人名など読みにくいものは一応ひらがなにしておく。
文節を意識して、適当な場所に句点を入れる。
効果音を入れたい場所で`*`を挿入する。
どこで改行しても読み方には一切影響しないので構わない。

## コマンド
* `-p` : ボイスキャッシュの取得のみ行い、読み上げを行わない。低速なネットワーク環境下などで使える？
* `-a` : 全てのボイスを準備してから再生を開始する。ネットワークエラーが起こらない限り、全てのテキストが読み上げられることが保証される。

## 用語
|  用語  |  説明  |
| ---- | ---- |
|  音  | アプリ内で使用する音。以下の3つが定義されている。|
|  オープニング音  | 読み上げを開始する時に鳴る(`sounds/op.wav`)。|
|  効果音 | 読み上げの途中に任意で鳴らすことができる(`sounds/se.wav`)。|
|  エンディング音  | 読み上げが終了した時に鳴る(`sounds/ed.wav`)。|
|  テキスト  | 読み上げてほしいテキスト全体。|
|  テキストブロック  | テキストのうち、文頭、`*`(効果音の記号)、文末のいずれかで囲まれた文字列。|
|  ボイスキャッシュ  | ローカルに保存されているボイスのデータ。テキストブロック単位で作成されている。|

## ボイスキャッシュとボイスの再生の挙動
テキストブロック毎にボイスは再生される。そのテキストブロックに対応するボイスがボイスキャッシュ内に
* (A)存在する場合、そのボイスが読み込まれ、再生される。
* 存在しない場合、
  * (B)音声合成APIからそのテキストブロックを読み上げるボイスを取得し、ボイスキャッシュへ保存する。
  * (A)ボイスキャッシュにそのボイスが保存されるまで一定時間待機する。待機時間内にそのボイスが
    * (A)保存された場合、そのボイスが読み込まれ、再生される。
    * (A)保存されなかった場合、処理は中断され、次のテキストブロックに対する処理が開始される。

AとBはそれぞれ別のスレッドで非同期に実行されている。

## 文献
* ドコモ開発者サービス音声合成API【Powered by NTTテクノクロス】仕様,https://dev.smt.docomo.ne.jp/?p=docs.api.page&api_name=text_to_speech&p_name=api_7#tag01