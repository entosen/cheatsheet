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


====================================
自作コマンド (利用者定義命令)
====================================

::

    on 利用者定義命令の名前()
            処理する内容
    end 利用者定義命令の名前


引数の取り方にいくつか種類がある。

位置渡しの利用者定義命令。丸かっこで書く。

::

    命令の名前(値, ...)

    on 命令の名前(変数名, ...)
            処理する内容
    end 命令の名前


ラベル渡しの利用者定義命令(1)。 ``given`` を書く。

::

    命令の名前 given ラベル:値,...

    on 命令の名前 given ラベル:変数名,...
            処理する内容
    end 命令の名前


ラベル渡しの利用者定義命令(2)。 定義済みのラベルを書く。

::

    命令の名前 ラベル 値  ラベル 値  ...

    on 命令の名前 ラベル 変数名  ラベル 変数名  ...
            処理する内容
    end 命令の名前

(注1)定義されているラベル(前置詞)。::

    about / above / against / apart from / around / aside from / at 
    / blow / beneath / beside / between / by / for / from 
    / insted of / into / on / onto / out of / over / since 
    / through(thru) / to / under



注意

tellブロック中から自作コマンドを呼び出すときは、 ``my`` か ``of me`` をつけないといけない。

- ``my`` をつけないと、tell で指定したモノに属するコマンドを探しに行ってしまう
- ``my`` をつけることで、ファイルグローバルのコマンドを探しに行く

::

    tell application "Finder"
        x() of me
        -- my x()   -- もしくは my 
    end tell
     
    on x()
        display dialog "ハンドラX"
    end x

====================================
よく使うコマンド
====================================

クリップボード(変数)::

    set the clipboard to "hoge"


キー入力::

    -- まず、キーを送りたいアプリを前面に出しておく
    tell application "ATOK Customizer"
        activate
    and tell

    tell application "System Events"
        key code 49    --- キーコードを送信する。49 は Space

        set the clipboard to "日本語"
        keystroke "v" using {command down}   -- cmd+V で貼り付け
        delay 0.5  -- ※1

    end tell

IMEがONになっているとうまくいかない。

日本語は keystroke では入らないので、クリップボード経由で貼り付ける。

key code や keystroke は、非同期っぽい。
おそらくキー入力のキューに入れた時点でコマンドが戻ってくる。
なので、実際にキーが処理されるのにはタイムラグがある。
特に、クリップボードから貼り付ける場合、cmd+v を送信して、直後にクリップボードを書き換えるとそれが入力されてしまうことがある。
なので、 cmd+v の後は 0.5秒ぐらい delay するとよい。

キーコード一覧

- https://eastmanreference.com/complete-list-of-applescript-key-codes

        



====================================
ソースコードの文字コード
====================================

スクリプトエディタ.app は、テキスト形式で保存できる (``.applescript`` ファイル) 。

それの文字コードが微妙。

スクリプトエディタで新規作成しテキスト形式へ保存すると...

  - 日本語が混ざらない場合、ASCII ？ になる。
  - 日本語が混ざる場合、Shift-JIS になる。
  - Shift-JISで保存できない日本語が混ざる場合、UTF-16 になる。
  - ちなみに、一度 Shift-JIS や UTF-16 で作成したファイル中の日本語を取り除いて、
    上書き保存しても文字コードは変わらない。


スクリプトエディタで開く分には、utf-8 でも読めるっぽいが、
一度実行すると？勝手にそれをSJISで保存し直してしまう。。。


参考

- `https://github.com/stymyuko/applescript#セットで公開する理由 <https://github.com/stymyuko/applescript#%E3%82%BB%E3%83%83%E3%83%88%E3%81%A7%E5%85%AC%E9%96%8B%E3%81%99%E3%82%8B%E7%90%86%E7%94%B1>`__
