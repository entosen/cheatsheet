

TODO メモ

vim のフラグ::


  \m、\M、\v、\V、はVimだけの機能。\c \C はどうか

  \v   very magic ≒拡張正規表現
  \m   magic ≒通常正規表現。デフォルト。``( | )`` はエスケープが必要。  

  \c   case insensitive (大文字小文字を無視)
  \C   case sensitive (大文字小文字を区別する)

  s/\CFooFunction/BarFunction/   

  \v, \m は、IntelliJ の IdeaVim では使えた。
  VSCodeVim では使えなかった。もともと `\v` 相当の挙動になっていた。
  VSCodeVim は JavaScript の正規表現ライブラリを使っているため。


::

  肯定先読み (?=)
  肯定後読み (?<=)
  否定先読み (?!)
  否定後読み (?<!)


vim では使える ``\zs`` ``\ze``::

  Foo〜.htm だけを Foo〜.html にしたい

  s/\v(Foo\w*)\.htm\ze/\1.html/     マッチの参照が必要。パターンによっては個数が変わる場合もある。
  s/Foo\w*\zs\.htm\ze/.html/

  \zs \ze は、IdeaVim では使えたが、VSCodeVim では使えなかった。
