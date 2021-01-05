==================================
Fabric v2 , Invoke
==================================

概要
==========

Invoke
    ローカルでシェルコマンドを実行するPythonライブラリ、および、タスクランナー(CLI)

Fabric 2
    Invoke をSSH経由でのリモートホスト実行に拡張したもの。

    SSHライブラリには `Paramiko <http://www.paramiko.org/>`_ を利用。



本家

- http://www.fabfile.org/
- https://www.pyinvoke.org/

参考

- `Pythonタスクランナー Fabric 2 の紹介 - 前編 Fabricの概要 - - インフラエンジニアway - Powered by HEARTBEATS <https://heartbeats.jp/hbblog/2018/11/fabric2-01.html>`__



インストール
================

::

    pip install invoke
    pip install fabric


例
=================

Invokeの場合
-----------------

デフォルトで読み込まれるファイル名は ``tasks.py`` 。

pythonコードでのタスクの定義::

    from invoke import task

    @task
    def print_uname(c):           # c は context の意。
        c.run('uname -a')


invoke コマンドからの呼び出し方::

    invoke --list                 # タスク一覧の表示

    invoke print-uname            # 関数名に `_` を含む場合、タスク名は `-` に置換される
    invoke taskname arg1 arg2     # タスクにパラメタを渡す場合



Fabric 2 の場合
------------------

デフォルトで読み込まれるファイル名は ``fabric.py`` 。

pythonコードでのタスクの定義::

    from fabric import task

    @task
    def print_uname(c):           # c は Connection の意。
        c.run('uname -a')


fab コマンドからの呼び出し方::

    fab -H <ホスト名のカンマ区切りのリスト> タスク名 [引数...]



詳細
=======================

http://docs.pyinvoke.org/en/stable/api/runners.html
::

    result = c.run(command, **kwargs)

        エラー時(終了コードが0以外)の挙動
            デフォルトでは、例外(UnexpectedExit)が投げられる。
            warn=True を指定すると、例外を飛ばさなくなる。

        command の stdout, stderr は、デフォルトでは両方ともstreamに出力される
            hide='out' (or 'stdout') : stdoutを出力しない
            hide='err' (or 'stderr') : stderrを出力しない
            hide='both' (or True)    : 両方出力しない
            hide=None (default)      : 両方出力する
            この指定にかかわらず、stdout,stderr は、Result に保存される



http://docs.pyinvoke.org/en/stable/api/runners.html#invoke.runners.Result
::

    result.return_code: 終了コード
    result.ok : boolean. exited == 0
    result.failed : boolean. ok の逆

    result.stdout: stdoutの内容
    result.stderr: stderrの内容
    result.tail('stdout', count=10) : ストリームの末尾を返す

        これらは改行付きなので、うまいことはずす


::

    c.sudo(command, **kwargs)

    c.sudo("command")






TODO

sshコネクションは 最初の run,sudo のタイミングで張られ、そのまま終了まで保持されるっぽい。

(invoke) task への引数の渡し方、かなりバリエーションがある。


TODO
ホスト指定するには
ユーザー指定するには
    fabコマンドライン -H <hostname>
sudo するには
--prompt-for-sudo-password






タスクランナーを作らずに、単にpythonのライブラリとして使う場合
===================================================================

TODO
