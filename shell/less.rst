==========================================
less
==========================================


参考
==========

- `less(1) — manpages-ja — Debian unstable — Debian Manpages <https://manpages.debian.org/unstable/manpages-ja/less.1.ja.html>`__


コマンド
===========

自分が使いそうなやつのみ。

N はコマンドに先行する整数 (viみたいな)

::

  h         ヘルプ表示
  q         終了
  r ^R ^L   再描画
  F         tail -F 的な

  === 移動系 ===
  SPACE f ^F        1 window (N行) 進む
        b ^B        1 window (N行) 戻る
  z                 SPACEに似ているが、行数Nを指定するとNが新しいwindowサイズになる
  w                 bに似ているが、行数Nを指定するとNが新しいwindowサイズになる

  d ^D              半 window (N行) 進む
  u ^U              半 window (N行) 戻る

  j ^E ^N RETURN    1行(N行)進む
  k ^Y ^P           1行(N行)戻る

  g                 ファイルの第1行目(第N行目)に移動
  G                 ファイルの最終行(第N行目)に移動

  p %               ファイルのN%の位置に移動する

  === マーク系 ===
  m                 任意の小文字を続けて入力することで、現在の位置をマーク
  '                 マークを呼び出し

  === 検索系 ===
  /pattern          進行方向に検索
  ?pattern          逆方向に検索

      patternに前置する特殊文字
        !   パターンにマッチしない行を検索する

  n   前回の検索を繰り返す (順方向)
  N   前回の検索を繰り返す (逆方向)

  &pattern          マッチした行のみ表示。繰り返すとどんどん絞り込み。
                    空パターン(& Enter)で絞り込みリセット。

  === オプション系 ===
  -       続けて1文字コマンドラインオプション。反転する。
  --      - と似ているがロングオプション。
  -+      続けて1文字コマンドラインオプション。デフォルトに戻す。
  --+     -+ と似ているがロングオプション。
  -!      続けて1文字コマンドラインオプション。デフォルトの反対。
  --!     -! と似ているがロングオプション。

 
   
オプション
===================

自分が使いそうなやつのみ。

::

  -i  --ignore-case         ignore case で検索。patternに大文字が含まれていた場合には case。
  -I  --IGNORE-CASE         ignore case で検索。patternに大文字が含まれていた場合でも ignore case。

  -j<n> --jump-target=<n>  「ターゲット」行とする画面上の行番号を指定する。 

  -m  --long-prompt         %表示のプロンプト。
  -M  --LONG-PROMPT         より詳細なプロンプト。 hoge.txt byte 867/13445 6%

  -p<pattern> --pattern=<pattern>   開いたら検索を実行

  -r  --row-control-chars  制御文字を解釈(制御文字のまま出力)
  -R  --RAW-CONTROL-CHARS  制御文字(色コードとhyperlinkのみ)を解釈(制御文字のまま出力)
                           デフォルトだと制御文字は ^A などと表示する

  -S  --chop-long-lines    行を折り返さない

  -n  --line-numbers       行番号を数えない。プロンプトなどに出さない。byte表示になる。
  -N  --LINE-NUMBERS       行番号を表示する

  -X  --no-init            less終了後表示内容がターミナルに残る。
                           デフォルトだとless起動前の内容に戻る。

  -F  --quit-if-one-screen  最初の画面でファイル全体が表示できる場合、 less を自動的に終了させる。

  +<command>               初期化コマンド(先頭のファイル)。 +G だとファイル末尾を表示。
  ++<command>              初期化コマンド(全てのファイル)

  -+                       1文字オプションをこのように始めると、オプションをデフォルトの状態に戻す。
                           例 -+R など。
  -+--                     ロングオプションのキャンセル。 例 -+--LINE-NUMBERS


環境変数 "LESS" の値もオプションとして使われる。
自分好みの設定を入れておくとよい::

  export LESS="--ignore-case --jump-target=5 --LONG-PROMPT"

