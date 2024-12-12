======================================
file, directory 関連コマンド
======================================




ファイルの移動,リネーム
==================================

基本は mv でやればよい。


大量ファイルのリネーム
----------------------------------

for と mv で(シェルの変数展開と文字列置換で)::

  for f in *.java ; do
    mv -vi $f ${f/foo/bar}    
  done

※ ``${f/foo/bar}`` は正規表現ではない。(ファイルグロブのパターンが使えるらしい)


for と mv で(正規表現)::

  for f in *.java ; do
    mv -vi $f $(echo $f | sed 's/foo/bar/')   # (注) ためしていない
  done



renameコマンド::

  # Mac の場合、 brew install rename で入る
  rename 's/img-(\d*).jpg/foo-$1-bar.jpg/' *

  # -n オプションで dryrun

rename コマンドは perl の正規表現？

渡されたパスを文字列として正規表現を適用し、mv に渡しているイメージ。
文字列として扱っているので、途中のディレクトリとかも置換できる。
(そのディレクトリが存在していなかったらエラーになるが。)




mac の renameコマンド
-------------------------------

rename コマンドいろいろあるらしい。

とりあえず Mac で入るものからまとめる。

参考

- `renameコマンドの使い方: UNIX/Linuxの部屋 <http://x68000.q-e-d.net/~68user/unix/pickup?rename>`__

::

  brew install rename

::

  rename 's/\.htm$/.html/' *.htm                # 正規表現。置換。
  rename 's/img-(\d*).jpg/foo-$1-bar.jpg/' *    # マッチしたものを使う




