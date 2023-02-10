#####################
AppleScript
#####################

ざっくりいってしまうと、Macのアプリケーションを操作できるスクリプト。

アプリケーションにメッセージを送るイメージ。

使いどころとしては、アプリケーションの起動・終了、キー操作など。




参考

- `鳶嶋工房 / アップルスクリプティング(Apple Scripting) <http://tonbi.jp/AppleScript/>`__
- `AppleScript 言語ガイド(2008年版 2016年改訂) - mytrans マニュアル等の個人的な翻訳 <https://sites.google.com/site/zzaatrans/home/applescriptlangguide>`__


::

    tell application "Google Chrome"
        <コマンド>
    end tell

    tell application "Google Chrome"
        activate
    end tell

    -- こういう書き方もあるらしい
    tell application "Google Chrome" to activate



====================================
言語仕様
====================================

- 変数名などの大文字小文字は区別されない
- 基本的にindexとかoffsetは1始まり


コメント
================

::

    -- 2つのマイナス以降はコメント

    (*
       コメント
       コメント
       -- 行コメントをネストすることもできます
        (* ブロックコメントをネストすることもできます *)
    *)


リテラルと定数
====================


boolean::

    true
    false

数値。型としては real, integer, number があるらしい

::

    -94596
    3.1415
    9.9999999999E+10


文字列::

    "aaa"

    "aaa" & "bbb" & "ccc"    -- 連結

    character 5 of "AppleScript"    -- "Apple"  インデックスは1始まり
    word 2 of "1 two 3 four"        -- "two"

    -- 複数行
    "あああ
    いいい
    ううう"

    paragraph 2 of result   -- "いいい" paragraph は行


    text from character 5 to character 7 of "AppleScript"
    --> "eSc"
    text from character 3 to word 2 of "Apple Japan"
    --> "ple Japan"
    character -1 of "一番最後は?"
    --> "?"

    "AppleScript" contains "apple"    -- true  (大文字小文字は区別しない)



リスト::

    {1, 7, "beethoven", 4.5}   --- 型を混ぜられます
    {1, {2, 3, 4}, 5}          --- 入れ子にできます
    {}                         --- 空リスト

    -- 操作
    set theList to {1,2,3}
    item 3 of theList              --- 取り出す。1始まり。
    set item 2 of theList to "a"   --- 変更  --> {1,"a",3}

    {4,5,6} & 7        --- 連結  --> {4,5,6,7}
    {4,5,6} & {7,8}    --- 連結  --> {4,5,6,7,8}
    "3" & {4, "aaa"}   --- 左辺が文字列だと文字列として連結されるので注意。"34aaa"

    {"R", 2, "D", 2} as string     ---> "R2D2"

    -- 比較
    {1, 2} = {2, 1}    --> false
    {"A", "O", "R"} contains "R" --> true



レコード::

    {product: "pen", price: 2.34}
    {text returned:"", button returned:"OK"}

    a of {a:10, b:0, c:2}     --- 取り出す --> 10

    set theRecord to {a:10, b:0, c:2}
    set c of theRecord to 120    --- 変更  {a:10, b:120, c:2}






result -- 直前の計算結果が入っている






====================================
コマンド(命令, command)
====================================

他のプログラミング言語で言うところの関数。「動作」。用語辞典だと "v" (動詞) と書いてある。

4種類

- AppleScriptが用意している「AppleScript命令」

  - ``get``, ``set``, ``count``, ``copy``, ``run`` の5つらしい
  - アプリケーション側で同名のコマンドが用意されていることもあるらしい

- OSAXが用意している「スクリプティング機能追加(OSAX)命令」

  - StandardAdditions.osax で用語が見られる

- アプリケーションが用意している「アプリケーション命令」

  - tell声明文と一緒に使う

- ユーザーが作成する「ユーザー定義命令」

呼び出し::

    count "この文章は何文字？"  --> 9
    round 123.45                --> 123
    beep 2                      ---> 値を返さない

    random number 100           ---> "random number" というコマンド。2語以上のコマンドも存在する
    current date                ---> date "2023年2月10日 金曜日 20:16:11"

引数

- 引数には必須のものと省略可能なものがある
- 引数には、直接の引数と、ラベル付きの引数がある

定義の例(実際は1行で書かないといけない)::

    display dialog 文字列1
            [default answer 文字列2]           -- [...] は省略可能な引数
            [buttons リスト]
            [default button 整数1 | 文字列3]
            [with icon 整数2 | 文字列4 | note/caution/stop]
            [giving up after 整数3]

    offset v: Find one piece of text inside another
        offset
            of <text> : the source text to find the position of
            in <text> : the target text to search in
            → intefer: the position of the source text in the target, or 0 if not found

型がbool型のラベル付き引数は、with/without 形式でも書ける。
スクリプトエディタは勝手に with/without 形式に直してしまう。::

    some command ラベル1 true ラベル2 false
    → some commant with ラベル1 without ラベル2




無意味句::

    about, above, against, apart from, around, aside from, at,
    below, beneath, beside, between, by, for, from, instead of,
    into, on, onto, out of, over, since, thru (throughも可), under




====================================
コマンド2
====================================

用語をみる



activate --- アプリケーションを起動してアクティブ(手前)にする。すでに起動済みなら手前にするだけ？
run --- アプリケーションを起動するのみ。アクティブにはしない。
quit  -- アプリケーションを終了

open::

    open location "http://tonbi.jp/"


tell
