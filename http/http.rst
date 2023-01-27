
HTTPバージョン
=======================

参考

- `HTTP の進化 - HTTP | MDN <https://developer.mozilla.org/ja/docs/Web/HTTP/Basics_of_HTTP/Evolution_of_HTTP>`__



- HTTP/0.9

  - 1990年頃
  - 単なるファイルのやりとりに近い
  - レスポンスのステータスコードもない
  - リクエスト/レスポンスヘッダがない
  - レスポンスはファイルの内容そのまま

- HTTP/1.0

  - 1996年頃。RFC 1945
  - レスポンスのステータースコード行ができた
  - リクエスト/レスポンスヘッダ 導入
  - Content-Type で、プレーンHTMLファイル以外のファイルの転送

- HTTP/1.1

  - 1997年頃。RFC 2068
  - コネクションの再利用(keep-alive)。デフォルトON。
  - パイプライン (最初のリクエストへの回答が完全に転送される前に次のリクエストを送信できる)

    - `HTTP/1.x のコネクション管理 - HTTP | MDN <https://developer.mozilla.org/ja/docs/Web/HTTP/Connection_management_in_HTTP_1.x>`__

  - Chunked 形式のレスポンスをサポート (Content-Lengthを送らず、随時送信して、かつ終わりがきちんと分かる)
  - Hostヘッダ
  - 安定。主流。

- HTTP/2

  - 2010年代の前半
  - 高パフォーマンス(低遅延)狙い
  - テキスト形式ではなく、バイナリ形式。 HTTP1.1のチャンクには対応していない。
  - 多重化。同じコネクションでリクエストを並行に扱える
  - ヘッダの圧縮
  - サーバプッシュ
  - この仕組みは、HTTPの上に乗っているアプリケーションからは、1.1と透過的に(同じように)見える。改修がいらない。

    - ``[HTTP1.1] -- [HTTP/2変換層] -- [トランスポート層]`` 見たいなイメージ

- HTTP/3

  - まだ
  - トランスポート層に TCP/TLS の代わりに QUIC 






メッセージ BODY
==========================

うーん。難しい。

chunked を使う。 Content-Length を送らなくていい。終了チャンク(長さ0のチャンク)によって、終了がわかる。

chunked を使わない。 Content-Lengthを送らずにBodyの送信を始めた場合、コネクションをcloseすることで終了がわかる。

chunked を使わない。 Content-Lengthを送れば、それで終了がわかる



