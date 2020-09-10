=======================
プロセス
=======================

ps
===========

https://linuxjm.osdn.jp/html/procps/man1/ps.1.html

よくやるやつ::

    ps auxww   # 全プロセス(cpu,メモリの使用率を表示)
    ps ajxww   # 全プロセス(プロセス親子関係のIDを表示)
    ps auxwwf  # ツリー表示

    # カラム指定、ソート
    ps axww -O 'user,%cpu' --sort user


オプション
-----------------

歴史的経緯で以下3種類がある

- UNIXオプション。まとめることが可能で、前にはダッシュを置かなければならない。
- BSD オプション。まとめることが可能で、ダッシュを使ってはならない。 
- GNU ロングオプション。前に二つのダッシュを置く。 


プロセス選択::

    指定なし  同じ実行ユーザー、かつ、同じ端末のプロセス
    a         端末(tty)を持つ全てのプロセス
    ax -e -A  全てのプロセス

リストによるプロセス選択::

    後ろに引数を取る。(カンマもしくは空白で複数書ける。)
        ps -p "1 2" -p 3,4

    U -u --user   実効ユーザーID or 実効ユーザー名
    -U            実ユーザーID or 実ユーザー名
    -C            コマンド名(実効ファイル名)
    p -p --pid    プロセスIDで選択

なんかこの辺の選択、よくわからん。



カラムの選択::

    指定なし
        PID TTY      STAT   TIME COMMAND

    u   ユーザー指向
        USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND

    j   BSD のジョブ制御フォーマット 親子関係
        PPID   PID  PGID   SID TTY      TPGID STAT   UID   TIME COMMAND

    o format
    -o format
    --format format
        1つ1つ指定する。

    -O format
        -o pid,<format>,state,tname,time,command に等しい

ソート::

    --sort <spec>
        [+|-]key[,[+|-]key[,...]]


その他::

    w -w  出力幅を広げる。2つ指定すると制限なし。

    -H  階層表示(ツリー表示) インデントで。
    f   階層表示(ツリー表示) ASCII アートで。

    e   コマンドの後に環境変数を表示する


カラム

- `%cpu`

    - (CPU時間 / 実時間) * 100 。 
      なので、プロセスが始まってから今までの平均。
      マルチスレッドだと 100% を超えることがある。




pstree
==================

::

    pstree -ap

        引数なしでも、全ユーザーのプロセスを表示してくれる。
        Thread もPIDで管理されているようで、表示してくれる。{ } で囲んで表示。
        -a  起動時のコマンドライン引数を表示
        -p  PIDも表示。
        -l  長く


