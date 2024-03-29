==================================
gmake
==================================

参考にさせてもらったサイト
==============================

- https://www.gnu.org/software/make/manual/html_node/index.html

    - 本家、英語

- https://www.ecoop.net/coop/translated/GNUMake3.77/make_toc.jp.html

    - リファレンス的なもの。日本語。
    - ちょっと古い。 conditional function とかが載っていない

- `make を使いこなすためのメモ | まくまくいろいろノート <https://maku77.github.io/memo/tool/make.html>`__

    - ひととおりのことが、いい感じのボリュームでまとまっている


チートシート
======================

Makefile::

    objects = main.o kbd.o command.o display.o \
          insert.o search.o files.o utils.o

    edit : $(objects)
            cc -o edit $(objects)

    $(objects) : defs.h
    kbd.o command.o files.o : command.h
    display.o insert.o search.o files.o : buffer.h

    .PHONY
    clean:
        rm ...


ルール::

    targets : prerequisites
            command
            ...
      ↑TABじゃないとだめ

変数展開::

    Make変数の展開
        $(foo), ${foo}
    
    コマンド行も同じ。
    環境変数を展開するつもりでやると、Make変数が展開されるので注意。
    コマンド行で環境変数だけを展開したい場合は
        $${foo}


自動変数::

    $@  ターゲット名 (1つ) 
    $^  prerequisites で指定したすべてのファイル名(重複は除かれる) (リスト) 
    $<  prerequisites で指定した最初のファイル名 (1つ) 
    $*  pattern rules/static pattern rules のstem(語幹)

    $+  prerequisites で指定したすべてのファイル名(重複も残される) (リスト)
    $?  ターゲットより新しい依存関係の名前 (リスト)

    上の変数名に `D`, `F` をつけることで、ディレクトリ部分とファイル名部分を抜き出すことができる。

    $(@D)  $@のディレクトリ部分。末尾の `/` はつかない。スラッシュが含まれない場合は `.`。
           cf. $(dir $@) の末尾には`/`が付く。
    $(@F)  $@のファイル名。$(notdir $@)'と同等。


変数、および、それがいつ評価されるか::

    <immediate> = <deferred>     # 右辺は後で評価。文字通りのまま代入
    <immediate> ?= <deferred>    # 変数が未定義の場合のみ代入。右辺は後で評価。文字通りのまま代入
    <immediate> := <immediate>   # 右辺はすぐ評価。再帰的に展開した結果を代入
    <immediate> += <deferred> or <immediate>   # 追加
                  （右辺に指定した変数が := で作成されたものなら <immediate> となる）

    define <immediate>
            <deferred>
    endef

    <immediate> : <immediate> ; <deferred>
            <deferred>


    条件判定は <immediate> 1st phase で行われる。


分岐::

    all:
    ifeq ($(HOGE), aaa)
            @echo matched.
    else
            @echo not matched.
    endif

    ifeq ($(DEBUG), 1)
      LIBS = $(LIBS_FOR_DEBUG)
    else
      LIBS = $(LIBS_FOR_RELEASE)
    endif

    ifeq (arg1, arg2)
    ifneq (arg1, arg2)
    ifdef foo    # $つけない
    ifndef foo   # $つけない
    

makeの特徴
=====================

最大の特徴は、変更が必要なものだけを更新してくれること。

.. image:: fig_gmake_rule.png


make の２フェイズ処理（変数の展開タイミングについて）
=======================================================

make コマンドが Makefile を処理するとき、以下の2フェイズで処理

1. Read-in phase (1st phase)
   
   - 最初に Makefile の内容をすべて読み込み(インクルードしたファイルもすべて)、
     依存関係のグラフ構造や、変数の値などを内部に保持します。

2. Target-update phase (2nd phase)
   
   - 1st phase で構築された内部構造を用い、最終ゴールを生成するために再帰的にルールを適用していく



ルール
====================


基本的なルール
--------------------

::

    targets : prerequisites
            command
            ...
    ↑ここのインデントはタブ文字じゃないといけない


    # あんまりやらないが、セミコロンで区切ってコマンドを書ける(1行で書ける)
    targets : prerequisites ; command 
            command
            ...

    # 何もしないコマンドを持つルール
    # (cf. コマンドを持たないと暗黙のルールが探索されてしまう。それを避けるために使う)
    targets : prerequisites ;
    targets : ;

- targets: 作りたいファイル名
- prerequisites: targets を作るのに必要なファイル(orタスク)。依存関係
- command: そのファイルを作るためのコマンド


同じターゲットを複数のルールに分けて書く::

    targetA: targetB

    targetA: targetC
            [コマンド行]

↑コマンドはどれか1つにしか書けない。(cf.パターンルール と 2重コロンルール(``::``)は別)


複数のターゲットを持つルール::

    targetA targetB: targetC
            [コマンド行]

    これは下記と同じ

    targetA: targetC
            [コマンド行]
    targetB: targetC
            [コマンド行]

↑変数でtargetを列挙する場合などに便利。


デフォルトゴール
----------------------

一番最初のターゲット(ただし"."で始まるターゲットは除く)。



.PHONY
----------------------

::

    .PHONY: clean
    clean:
            rm *.o temp

``.PHONY`` が指定されたターゲットは、

- (仮にその名前のファイルが存在していても)ファイルが常にないものとして動作する。つまり、常にコマンドが動く。
- (コマンド行がなかったとしても)暗黙のルールの検索をしない。


自動変数
----------------------

コマンドの中で使える。

詳しくは冒頭の `チートシート`_ を参照。


ワイルドカード wildcard
------------------------------

target や prerequisite の指定には、Bourne シェルのワイルドカードを使用することができる。

cf. command でワイルドカードを使うと、そのコマンドを実行するシェルによって展開されます。

::

    * ==> 任意の文字列
    ? ==> 任意の 1 文字
    [...]  ==> どれか1文字
    ~ ==> ホームディレクトリ（Windows の場合は HOME 環境変数の値）
    ~john ==> john のホームディレクトリ

変数に格納する場合::

    # これだと展開されない
    OBJECTS = *.o

    # このように wildcard 関数を使う。 := なのも注意。
    OBJECTS := $(wildcard *.o)


Static Pattern Rules (静的なパターンルール)
-------------------------------------------------

target名(普通は複数並べる)から prerequisites を自動構成するためのルール

::

    targets ...: target-pattern: prereq-patterns ...
            commands
           ...


例::

    OBJECTS = foo.o bar.o

    $(OBJECTS): %.o: %.c
            $(CC) -c $(CFLAGS) $< -o $@

実質これと同じ::

    foo.o: foo.c
            $(CC) -c $(CFLAGS) foo.c -o foo.o
    bar.o: bar.c
            $(CC) -c $(CFLAGS) bar.c -o bar.o

- target-pattern は `%` を1つだけ含む。
- `%` にマッチした部分を stem(語幹) と呼ぶ。
- Static Pattern Rules の command では `$*` で stem を参照できる。

    - パターンルールと違い、ディレクトリ部分を除くような処理は発生しない。ディレクトリも含め単純にマッチ。

- target-pattern にマッチしない target があった場合は警告を出す。cf. `$(filter %.o,$(files))`

    - 依存関係は全部なくなり、 ``$@`` , ``$*`` はターゲット全体、 ``@^`` は空になるっぽい


静的パターンルール と パターンルール(暗黙ルール) との違い

- 静的パターンルールのターゲットには ``%`` を含まない (パターンルールは含む)
- 静的パターンルールのターゲットは常に明確なので、常にルールに登録される

  - cf. パターンルールは、依存関係が存在するか「生成可能」であって初めて登録される


暗黙ルール
-------------------------

.. image:: fig_gmake_implicit.png

ある型からある型の生成方法を記述したルール。 ターゲットに ``%`` を含む

記述方法は2つ

- パターンルール
- サフィックスルール (古い)


下記のどれかに当てはまる場合に、暗黙ルールを探しにいく

- あるターゲットに対し、コマンド行を1つを持たないルールを書く
- 依存関係にだけ出現し、それについてのルールを全く書かない

一般的には、

- コマンドを持たないターゲット
- コマンドを持たない二重コロンルール
- ルールのないターゲット (依存関係でしか書かれていないファイル)


どの暗黙ルールが適用されるか

- (1) 作ろうとしているターゲットが、その暗黙ルールのターゲットパターンに当てはまる
- (2) さらに、その暗黙ルールの依存関係に該当するファイルが存在しているか「作成可能」である

※注意：このとき元の作ろうとしているターゲットの明示的な依存関係は影響しない::

    foo.o: foo.p

    こう書いたとしても、foo.p と書いたことが暗黙ルールの選択には影響しない。
    foo.c が存在するなら .c から .o を作る暗黙ルールが適用される。
    (どちらの暗黙ルールが先に定義されているかによる)

コマンドのないターゲットに暗黙ルールを使わせないようにするには、
セミコロンを使ってターゲットに空っぽの(何もしない)コマンドを与える::

    foo: foo-1 foo-2 foo-3 ;


パターンルール
^^^^^^^^^^^^^^^

パターンルールを書くことで、暗黙のルールを追加、再定義できる。

target に ``%`` という文字を含んでいる。

``%`` は1文字以上の文字列にマッチする。


::

    %.o : %.c
            $(CC) -c $(CFLAGS) $(CPPFLAGS) $< -o $@


依存関係は、1つも書かなくてもいいし、 ``%`` を含まない固定のファイルを書いてもよい。複数書いてもよい。


ターゲットパターンに ``/`` を含む・含まないで挙動が違う。

(1) ターゲットパターンに ``/`` を **含む** 場合

- ``/`` も含めて単純な文字列マッチ

例::

    dir1/aaa_%.o: out1/bbb_%.c foo.c
        command...
    に対して

    (例1) dir1/aaa_hoge.o がターゲットのとき
    依存関係は
        dir1/aaa_hoge.o: out1/bbb_hoge.c foo.c
    $* は hoge

    (例2) dir1/aaa_dir/hoge.o ターゲットのとき
    依存関係は
        dir1/aaa_dir/hoge.o: out1/bbb_dir/hoge.c foo.c
    $* は dir/hoge


(2) ターゲットパターンに ``/`` を **含まない** 場合

ディレクトリ部分を除いたファイル名部分にしかマッチしないようになっている。

- 比較前にディレクトリ部分が除かれ、ファイル名だけになる
- ファイル名に対してパターン比較
- 依存関係パターンの``%``を埋め、ディレクトリ名を前置する
- stem( ``$*`` ) は ``ディレクトリ/%`` になる

例::

    aaa_%.o: bbb_%.c other.c
        command...
    に対して

    (例1) aaa_hoge.o がターゲットのとき
    依存関係は
        aaa_hoge.o: bbb_hoge.c other.c
    $* は hoge

    (例2) dir1/aaa_hoge.o がターゲットのとき
    依存関係は
        dir1/aaa_hoge.o: dir1/bbb_hoge.c other.c
    $* は dir1/hoge

    (例3) dir1/aaa_dir/hoge.o ターゲットはマッチしない。





1つのターゲットパターンに、複数のパターンルール
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

通常のルールとは異なり、
1つのターゲットパターンに、(依存関係の型の違う)複数のパターンルールを定義することができる。

::

    %.o : %.c
            $(CC) ...  # C
    %.o : %.cpp
            $(CXX) ...  # C++
    %.o : %.f
            $(FC) ...  # fortran

定義順に当てはまるかどうかチェックされ、最初に当てはまった1つだけが使われる。

1つのパターンルールで、2つ以上のターゲット
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

2つ以上のターゲットを書いた場合、

::

    %.tab.c %.tab.h: %.y
            bison -d $<


- cf. 通常のルールの場合は「同じ依存関係とコマンドを適用するたくさんの異なるルール」分解されるが、パターンルールの場合はそうはならない
- そのコマンドで、それら全てのターゲットが生成されるとみなす

    - コマンドは、すべてのターゲットを作るために一度だけ実行される

- 暗黙ルールを探すときは、現在注目しているターゲット(ファイル名)が複数のターゲットパターンのどれかにマッチすればよく、
  それ以外のターゲットパターンは関係ない
- このコマンドが実行されると、他のターゲットも含め、更新されたとマークされる。(他方の依存関係でコマンドが実行されることはない)

↑ どういうとき使うんだ？？？2つ以上のファイルを一度に生成する場合でしか使わない？


何でも一致ルール
^^^^^^^^^^^^^^^^^^^

ターゲットが ``%`` だけのルール

マッチしすぎて、これを探しにいってmakeが遅くなる弊害があるので、以下のどちらかの制限が入る。


(1)「何でも一致」ルールを二重コロンで定義して終点(terminal)にしてしまう

::

    % :: RCS/%,v
            $(CO) $(COFLAGS) $<

その依存関係のファイルが存在しない場合(明示的な依存関係でも作られない場合？）、
暗黙ルールの連鎖をせずにその暗黙ルールの適用をあきらめる。
言い換えるとそれ以上の連鎖をしない。

(2) 二重コロンにしない場合

他の(なんでも一致ではない)パターンルールが存在するターゲットには、適用しない

::

    %.c:   # ダミーのパターンルール

    %: %.c
            $(LINK.c) $^ $(LOADLIBES) $(LDLIBS) -o $@

例えば hoge.c には `%.c` のパターンルールがあるので、この何でも一致ルールは適用しない。
(hoge.c を作ろうとして、hoge.c.c からビルドしたりはしない)




古いタイプのサフィクスルール(Suffix Rules)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

    # 「既知のサフィックス」が2つ連なったもの。ダブルサフィックス
    .c.o:
            $(CC) -c $(CFLAGS) $(CPPFLAGS) -o $@ $<
        ↓
    %.o : %.c と同じ

    # 「既知のサフィックス」が1つ連なったもの。シングルサフィックス
    .c:
            command
        ↓
    % : %.c と同じ


「既知のサフィックス」はデフォルトでいくつか登録されているが、変更したい場合は::

    # 追加したい場合
    .SUFFIXES: .hack .win

    # デフォルトを使わずに設定したい場合
    .SUFFIXES:            # デフォルトサフィックスの削除する
    .SUFFIXES: .c .o .h   # 好きなサフィックスリストを定義する


注意

- 依存関係を持たせることはできない。書いた場合は通常のルール (``.c.o`` という変な名前がターゲットのルール) として扱われる::

    .c.o: foo.h    # 意図と異なる！
            $(CC) -c $(CFLAGS) $(CPPFLAGS) -o $@ $<


暗黙ルールの検索アルゴリズム
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``archive(member)`` という形式のアーカイブメンバーターゲットに対しては以下のアルゴリズムは二度実行されます。
つまり、一度目は t という完全なターゲット名に利用し、
二度目は第一の実行でルールが見つからない場合に ``(member)`` を t というターゲットとして利用します。 

1. t を d というディレクトリ部分と n という残りの部分に分離します。
   たとえば t が ``src/foo.o`` なら、 d は ``src/`` で、 n は ``foo.o`` になります。 
2. 全てのパターンルールのリストを t か n に一致するターゲットのみに絞り込みます

   - 1つのパターンルールに複数のターゲットパターンがある場合は、それらのどれか1つに一致すればよい
   - ターゲットの型にスラッシュが含まれれば t に対して比較するものとし、
   - そうでなければ n に対して比較するものとします。

3. リスト中に1つでも「何でも一致」ルール **ではない** ものがあった場合、リストから非終点「何でも一致」ルールを削除します。
4. コマンドのないルールはリストから削除します。
5. リスト中の各型ルールに対して

   1. t か n に一致したターゲット型の ``%`` の部分(空っぽではない)としてs という語幹を見つける
   2. 依存関係パターンから ``%`` の部分を s に置き換えて依存関係を作成する。
      この際、ターゲットパターンが ``/`` を含まない場合、 d をその前につける。 
   3. 全ての依存関係が存在しているか「存在すべき」かをテストする。
      (ファイル名がmakefile内で、ターゲットもしくは明示的な依存関係として書かれている場合に「存在すべき」と考えます。)
      全ての依存関係が存在するか「存在すべき」である、または依存関係が1つもないなら、このルールが適用されます。 

6. 型ルールが全然見つからなければ、リスト中の各パターンルールに対してさらに頑張って次の事を試してみます。 

   1. ルールが終点(terminal)ならそれを無視して次のルールに移る。
   2. 前に書いたとおりに依存関係の名前を作成する。
   3. 全部の依存関係が存在する、または「存在すべき」かをテストする。
   4. 存在しない依存関係のそれぞれに対し、このアルゴリズムを再帰的に適用し、
      暗黙ルールでその依存関係を「生成可能」かを調べる。
   5. 全ての依存関係が、存在するか「存在すべき」か、暗黙のルールで「生成可能」である場合には、
      このルールが適用される。 

7. どの暗黙ルールも適用されない場合、 もしあれば ``.DEFAULT`` のルールが適用される。
   この場合は t に ``.DEFAULT`` の持つものと同じコマンドを与える。
   そうでない場合 t にはコマンドがないことになる。

一旦適用するルールが見つかったら、
(ターゲットパターンが複数あった場合) t や n に一致した以外のターゲットパターンについて、``%`` が置換され、
その結果のファイル名は t というターゲットファイルを更新するコマンドが実行されるまでは保管されます。
コマンド実行終了後、保管されていたファイル名はどれもデータベースに入れられ、
更新済みで t ファイルと同じ更新ステータスを持つとマークされます。


二重コロンルール
--------------------

同じターゲットで、二重コロンルールと一重コロンルールは共存できない。

二重コロンルールは、それぞれが独立した別のルールとして扱われる。

ターゲットファイルが複数の依存ファイルをもっていて，各依存ファイルごとにことなるコマンドを実行しなければならない場合に使う。らしい。

::

    g.lib:: sub1.obj
            lib g.lib-+sub1.obj

    g.lib:: sub2.obj
            lib g.lib-+sub2.obj


.. image:: fig_gmake_doublecolon.png


ただし、何でも一致ルール(``%``) で使う場合は、意味が変わる。


検索パス
--------------------

VPATH変数

- target や prerequisites の検索パスを追加したい時
- 複数のパスを指定したい場合は、コロン (:) かスペースで区切って指定
- カレントディレクトリはデフォルトで検索するので、指定する必要はない

::

        VPATH = src:../headers


vpath ディレクティブ

- ファイルの種類ごとに検索パスを追加する

:: 

    vpath %.h   ../headers
    vpath %.cpp src
    vpath %     hoge



リンクライブラリの検索パス

::

    foo : foo.c -lcurses
            cc $^ -o $@


- prerequisistes に -l<name> という形式でリンクライブラリを指定しておくと、
  lib<name>.so、あるいは lib<name>.a が検索される
- 以下の順番で libcurses.so ファイルが検索される

    - カレントディレクトリ
    - vpath に設定したディレクトリ
    - VPATH に設定したディレクトリ
    - /lib
    - /usr/lib
    - <prefix>/lib （通常は /usr/local/lib）

- libcurses.so ファイルが見つからなかった場合は、上記の順で libcurses.a ファイルが検索される








コマンド行 command
=====================

デフォルトでは /bin/sh で解釈される。
(make変数の ``SHELL`` を設定することで変更できる。)


行頭につけるやつ
----------------------

- ``-`` : マイナス始まり。エラーでも止まらない (デフォルトではエラーで停止する)
- ``@`` : 実行コマンドを表示しない。(デフォルトでは表示する)
- ``+`` : `-n` オプションなどの、スキップを避ける


注意点
------------

``$(変数名)`` , ``${変数名}`` : コマンド行で、make変数を展開するとき。

``$${変数名}`` :  コマンド行で、make変数ではなく、shell変数を展開するとき

コマンド行は、普通は1行ごとにサブシェルに渡される。

なので、forみたいな場合は行末バックスラッシュが必要::

    all:
            for i in $(LIST); do \
                echo $$i; \
            done

同様に cd は次の行には波及しない::

    all:
            cd hoge
            pwd       # hoge ディレクトリではない

    all:
            cd hoge && pwd    # こうする
    


再帰make sub-make
-------------------------------

``$(MAKE)`` を使う理由。

- 今のと同じ(パスの)makeを使ってくれる。 (/bin/make なのか、 /usr/local/bin/gmake なのか)
- ``-t(--touch), -n(--just-print), -q(--question)`` で実行されていた場合は、

  - ``$(MAKE)`` と書けば、同じオプションで実行される。
  - ``make`` と書くとその行は他のコマンドと同様、エコーバックするだけで実行されない
        


サブディレクトリで make を実行する場合::

    subsystem:
            cd subdir && $(MAKE)
    subsystem:
            $(MAKE) -C subdir

``-C`` 使った方がよい。ディレクトリが変わったことが表示される。(cf. ``-w`` オプション)


通常 make変数は、sub-make には渡されない。(環境変数とコマンド行で与えられた変数は渡る)。
export しておけば渡る。 (この場合のexportは、環境変数ではなく、あくまで sub-make へのexport)


MAKELEVEL 変数 : sub-make の呼び出し階層の深さを表す変数


コマンドの缶詰
----------------

defineで、一連のコマンドを変数に入れておく。

定義::

    define run-yacc
    yacc $(firstword $^)
    mv y.tab.c $@
    endef


使うとき:: 

    foo.c : foo.y
            $(run-yacc)



変数
====================

変数名
-----------

- 使える文字は？ TODO
- 大文字小文字を区別

    - makefileの内部利用が目的の変数には小文字
    - 大文字の変数名は暗黙のルールを制御する媒介変数(parameters)や
      コマンドオプションで上書きすべき媒介変数(parameters)



代入
----------

::

    =
        再帰展開変数。 Recursively expanded variable
        右辺は変数展開されない。一字一句同じに格納される。
        あとで再帰的に評価。

    :=
        単純展開変数。 Simply expanded variables
        右辺は(再帰的に)評価されて結果の値が格納される

    ?=
        変数が未定義のときのみ定義する Conditional variable assignment

    +=
        変数の値を追加。１つのスペースでつないでつなげる。


define で改行も含め一字一句そのまま代入できる::

    define <変数名>
    ...
    ...
    endef

ターゲット内だけで有効な変数を定義する (Target-specific Variable)::

    target ... : variable-assignment

        そのターゲットおよび、そのターゲットの prerequisites の構築に対して有効。
        ルールの記述とは別の行に書かないといけない。


コマンドラインから指定する場合::

    gmake FOO=BAR target


展開
----------

::

    $(変数名)     make変数
    ${変数名}     make変数

    サフィックスを置換して展開 (代用参照, substitution reference)
        マッチしなければ、置換されずに代入される。

    $(var:aaa=bbb)

        foo := a.o b.o c.o.o
        bar := $(foo:.o=.c)    # a.c b.c c.o.c

    パターンに%を含ませたらサフィックス以外もいける

        foo := dir1/aaa dir1/bbb dir1/ccc
        bar := $(foo:dir1/%=dir2/%)  # dir2/aaa dir2/bbb dir2/ccc

    cf. これは patsubst 関数でも書ける
        $(patsubst %.o,%.c,$(foo))




変数定義の優先順位
--------------------

1. makefile 内の変数定義（override ディレクティブ付き）
2. コマンドライン引数で指定した変数定義  (`make FOO=BAR all`)
3. makefile 内の変数定義（override ディレクティブなし）
4. 環境変数

- make のコマンドライン引数で変数値を指定すると、通常は Makefile 内での定義よりも優先される
- この優先度を変えて、Makefile 内の変数定義を有効にしたい場合は override ディレクティブを使用します。
- この優先度は、+= 演算子による値の追加でも同様で、
  コマンドライン引数で変数値が指定されていると、その変数への += での追加は通常無視されます。

::

    override hoge = 100
    override foo += aaa.o


変数がいつ評価されるか
--------------------------

`チートシート`_ を参照




分岐
====================

``conditional-directive`` は後述の ``ifdef`` や ``ifeq`` など。

::

    conditional-directive
      text-if-true
    endif


    conditional-directive
      text-if-true
    else
      text-if-false
    endif


    # GNU make version 3.81以降だと、 else if 的なものが使える
    conditional-directive-one
      text-if-one-is-true
    else conditional-directive-two
      text-if-two-is-true
    else
      text-if-one-and-two-are-false
    endif

    # それ以前でどうようなことをやる場合。(非常に見づらい)
    conditional-directive-one
      text-if-one-is-true
    else 
      conditional-directive-two
        text-if-two-is-true
      else
        text-if-one-and-two-are-false
      endif
    endif




コマンド行だとこんな感じ::

    all:
    ifeq ($(HOGE), aaa)
            @echo matched.
    else
            @echo not matched.
    endif


コマンド行以外だとこんな感じ (インデントはタブにしないのが推奨)::

    ifeq ($(DEBUG), 1)
      LIBS = $(LIBS_FOR_DEBUG)
    else
      LIBS = $(LIBS_FOR_RELEASE)
    endif




::

    ifeq (arg1, arg2)
    ifeq 'arg1' 'arg2'
    ifeq "arg1" "arg2"
    ifeq 'arg1' "arg2"
    ifeq "arg2" 'arg2'   文字列一致

    ifneq (arg1, arg2)
    ifneq 'arg1' 'arg2'
    ifneq "arg1" "arg2"
    ifneq 'arg1' "arg2"
    ifneq "arg2" 'arg2'   文字列不一致

::

    ifdef 変数名   (変数*名* つまり $ をつけないな点注意)
    ifndef 変数名

ifdefは、変数の値が空でないこと(fooを定義していない or foo= )を調べる。
変数を再帰的には展開しない点注意。

条件チェックは、Read-in phase (1st phase) で行われるので、注意。




関数
=======================

関数の基本形
--------------

::

    $(関数 引数)
    ${関数 引数}

    $(関数 引数,引数,...)
    ${関数 引数,引数,...}


- 引数はカンマで区切る。空白はつけられない。引数の一部になってしまう
- ダブルクオートなども評価されず、そのまま引数の一部になる


文字列関数
-------------

::

    $(subst from,to,text)
        置換

    $(patsubst pattern,replacement,list)
        $(patsubst %.c,%.o,x.c.c bar.c)
        パターン置換
        cf. サフィックス置換、代用参照、$(var:aaa=bbb)

    $(strip string)
        stringの前後の空白部分を削除し、
        文字列の内部にある一つ以上の空白文字を一文字のスペースに置換

    $(findstring find,in)
        $(findstring a,a b c)    # → a
        $(findstring foo,hogefoobar)    # → foo
        文字列探索。in文字列中に find文字列 が出現すれば true扱い。
        見つかればその値、見つからなければ空文字列

    $(filter pattern...,text)
        リストの中からパターン(複数可,どれか)に合うものだけを抽出
        $(filter %.c %.s,$(sources))
            拡張子が .c と .s のものだけを抽出

    $(filter-out pattern...,text)
        リストの中からパターン(複数可,どれにも)に合わないものだけを抽出

    $(sort list)

    $(word n,text)
        n番目の単語。1始まり。

    $(wordlist s,e,text)
        textの中のsからeまでの(その番号自身を含めた)単語のリストを返します。sとeの有効値は１から始まります。

    $(words text)
        単語数を返す

    $(firstword names...)
        最初の単語を返す

    $(lastword names...)
        最後の単語を返す


ファイル名関数
--------------------

::

    $(dir names...)
        ディレクトリ部分抽出。末尾に`/`が付く

    $(notdir names...)
        ディレクトリ以外の部分(ファイル名の部分)抽出

    $(suffix names...)
        拡張子を抽出

    $(basename names...)
        拡張子以外を抽出

    $(addsuffix suffix,names...)
        リストのそれぞれにsuffixを付け加える

    $(addprefix prefix,names...)
        リストのそれぞれにprefixを付け加える

    $(join list1,list2)
        python の zip みたいな動作

    $(wildcard pattern)
        patternは(シェルファイル名で使う型と同じような)ワイルドカードを含むファイル名

    $(realpath names...)
        それぞれの絶対パスを返す。 . や .. は含まない。 / の繰り返しもない。
        symlinkも解釈し、残らない。

    $(abspath names...)
        それぞれの絶対パスを返す。 . や .. は含まない。 / の繰り返しもない。
        symlinkはたどらず、そのまま残る。


条件関数
--------------

- condition は、空文字列なら false 扱い、それ以外なら true 扱い

::

    $(if condition,then-part[,else-part])
        condition の前後の空白を削除したのちにそれを評価。
        非空文字列(true扱い)だったら then-part 、
        空文字列(false扱い)だったら else-part (else-partが指定されてなかったら空文字列)。

    $(or condition1[,condition2[,condition3…]])
        順に見ていって、非空文字列(true扱い)の引数が出てきたら、それを返す(true扱い)。
        全ての引数が、空文字列(false扱い)だった場合、空文字列を返す(false扱い)。

    $(and condition1[,condition2[,condition3…]])
        順に見ていって、空文字列(false扱い)の引数が出てきたら、空文字列を返す(false扱い)。
        全ての引数が、非空文字列(true扱い)だった場合、 最後の引数を返す(true扱い)。


``$(eq)`` がないので使いづらい。代わりに

- ``$(filter Linux,$(OS))`` を使う。( ``%`` と空白を含まない前提) (わかりにくい)
- ``$(filterstring Linux,$(OS))`` を使う。 (厳密にやるなら逆向きも) 


``$(not)`` もない。 ``$(if)`` 使って無理矢理逆にやるか。



foreach関数
-------------

::

    $(foreach var,list,text)
    $(foreach 仮変数名,リスト,それぞれに適用される表現)

    python の内包表現 [text for var in list] みたいな感じ。

    例
    files := $(foreach dir,$(dirs),$(wildcard $(dir)/*))



shell関数
-----------------

シェルスクリプトにおけるバッククオートに似てる。

::

    contents := $(shell cat foo)
    files := $(shell echo *.c)    # これだとほぼ wildcard 関数と同じ


その他関数
-----------


::

    $(file op filename[,text])
        ファイルを読み書きする
        op は >,  >>,  <

        $(file >$@.in,$^)


    $(call variable,param,param,…)
        自前の関数を呼び出す

        reverse = $(2) $(1)
        foo = $(call reverse,a,b)


    $(value variable)
        変数を展開せずに返す cf. $(variable)


    $(eval content)
        変数の値を Makefile の記述として取り込む

    $(origin variable)
        その変数がどこで定義されたかを返す。
        undefined, default, environment, environment override,
        command line, override, automatic, bletch

    $(flavor variable)
        変数のフレーバーを返す
        undefined, recursive, simple

    $(error text…)
    $(warning text…)
    $(info text…)





デバッグの仕方
========================

デバッグ時に役立ちそうなオプション::

    -p
    --print-data-base
        makefileを読んでその結果としてデータベース(ルールと変数の値)を出力する。
        それからmakefileはいつも通りに(指定した場合指定したように)実行される。
        このオプションは `-v` スイッチ(下を参照)で与えられるバージョン情報も出力します。
        全くファイルを作成しようとしないでデータベースを出力するには `make -p -f /dev/null` を使って下さい。 

    -d
    --debug
    通常処理に加えてデバッグ情報を出力します。
        デバッグ情報は、どんなファイルがmakeの作業に関わるか、
        どのファイル時刻が比較されてその結果はどうだったか、
        どんなファイルを本当はmakeするべきだったか、
        どんな暗黙ルールが関わったか、
        など、どれがmakeの実行に関わったかという類のことなら何でも教えてくれます。 

    -n
    --just-print
    --dry-run
    --recon
        普通どおり実行されるはずのコマンドを出力するが、実行はしない。
        コマンドを実行する代わりに…の項を参照。 



Tips
=====================

foreach的なことをしたい
------------------------------

- 変数を変える必要がない場合

    - 依存関係に列挙してそれぞれ処理させる::

          ALL_PACKAGES = aaa.pkg bbb.pkg ccc.pkg
          all: $(ALL_PACKAGES)

          $(ALL_PACKAGES): 
                command $@

- ifeqなどの条件分岐によって変数を変える必要がある場合

    - 依存関係に列挙して、それぞれで 引数を変えて sub-make を呼ぶ::

          ALL_PACKAGES = aaa.pkg bbb.pkg ccc.pkg
          all: $(ALL_PACKAGES)

          $(ALL_PACKAGES): 
                $(MAKE) PACKAGE=$@ build  とか
                $(MAKE) build/$@          とか


