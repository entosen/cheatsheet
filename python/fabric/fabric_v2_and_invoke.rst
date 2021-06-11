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

run()
--------------------------------

- http://docs.pyinvoke.org/en/stable/api/runners.html

::

    result = c.run(command, **kwargs)

        エラー時(終了コードが0以外)の挙動
            デフォルトでは、例外(UnexpectedExit)が投げられる。
            warn=True を指定すると、上記例外を飛ばさなくなる。
                それ以外の例外(ネットワークエラーとか認証エラーとか)は飛ぶ

        command の stdout, stderr は、デフォルトでは両方ともstreamに出力される
            hide='out' (or 'stdout') : stdoutを出力しない
            hide='err' (or 'stderr') : stderrを出力しない
            hide='both' (or True)    : 両方出力しない
            hide=None (default)      : 両方出力する
            この指定にかかわらず、stdout,stderr は、Result に保存される


run()の結果 Result
------------------------------------

- http://docs.pyinvoke.org/en/stable/api/runners.html#invoke.runners.Result

::

    result.return_code: 終了コード
    result.ok : boolean. exited == 0
    result.failed : boolean. ok の逆

    result.stdout: stdoutの内容
    result.stderr: stderrの内容
    result.tail('stdout', count=10) : ストリームの末尾を返す

        これらは改行付きなので、うまいことはずす
        result.stdout.rstrip()
        result.stdout.rstrip('\n').splitlines()



sudo()
------------------

commandを sudo で実行する。パスワードは自動入力される。

- http://docs.pyinvoke.org/en/stable/api/context.html#invoke.context.Context.sudo

::

    c.sudo("command")
    c.sudo("command", user='appuser')


sudo()の認証の認証周りで失敗した場合には、 ``AuthFailure`` が投げられる。


パスワードを指定するには

- 何らかの方法で c.config.sudo.password をセット

  - 無理矢理 ``c.config.sudo.password = 'hogehoge'`` とする
  - コマンドラインで ``--prompt-for-sudo-password`` を付けると、
    実行に先立ちプロンプトが出て入力でき、それがセットされる
  - fabfile.py と同じ場所に fabric.yaml を作り、下記の内容を記載::

      ---
      sudo:
        password: 'wveF}bWNYp4Wsu6m'
    

- sudoメソッドのpassword引数で指定::

      c.sudo("command", password='hogehoge')


Context と Config
---------------------------

いろいろな設定値の渡し方がある (設定ファイル、環境変数、コマンドライン、コード中) 。

Context には、それら複数の箇所の記述を適切にマージした Config が含まれる。 ::

    c.config

- http://docs.pyinvoke.org/en/stable/concepts/configuration.html




sudo するには



コマンドライン
=========================

(invoke) task への引数の渡し方、かなりバリエーションがある。

- http://docs.pyinvoke.org/en/stable/concepts/invoking-tasks.html


関数名に ``_`` を含むものは、タスク名としては ``-`` に置換されたものになる。
タスクの引数も同様に ``-`` に置換されたオプションになる。

タスクに引数を渡すには::

    fab task1 --foo=bar --hoge=fuga
        task1(conn, foo='bar', hoge='fuga') と呼ばれる



Fabric の機能
==================

sshコネクションは 最初の run,sudo のタイミングで張られ、そのまま終了まで保持されるっぽい。


https://docs.fabfile.org/en/2.5/api/connection.html

ホスト指定するには
    # fabコマンドラインで -H (もしくは --hosts)
    fab -H host1,host2,host3 taskA taskB
        Running taskA on host1!
        Running taskA on host2!
        Running taskA on host3!
        Running taskB on host1!
        Running taskB on host2!
        Running taskB on host3!

    # @taskデコレータで (ただし、これより --hosts の方が強い)
    @task(hosts=['host1', 'host2', 'host3'])
    def taskA(c):
        c.run('uname -s')

    # コード中で
    from fabric import Connection
    c = Connection('web1')
    result = c.run('uname -s')

    Connection(host='web1', user='deploy', port=2202)
    Connection('deploy@web1:2202')



ユーザー(SSHログイン時の)を指定するには
    例 admin ユーザーを指定する場合

    fabric の設定ファイル (/etc/fabric.yml, ~/.fabric.json など) 下記を書いておく
        user: admin 
    ssh の設定ファイル (~/.ssh/config) に下記を書いておく。(Host ヘッダと組み合わせるとか)
        User admin 
    ホスト名指定のところで、ユーザー名@ の指定をする (--hosts や Connection())
        admin@myhost
    Connectionを作る際に user で指定
        Connection('myhost', user='admin')


元の Connection からちょっと変えた Connection を作る::

    # この4つをインスタンスに渡せば、同じものができるはず。
    # 変えたい部分を変えればよい。
    newConn = Connection(host=conn.host,
                         port=conn.port,
                         user=conn.user,
                         config=conn.config)

    # config を変える場合には、(参照なのでそのままいじると都合が悪いので、)
    # 下記のようにしてコピーを作ってからいじったものを渡す
    newConfig = conn.config.clone(into=Config)  # Connection.__init__ の中でもこうしている
    newConfig.sudo.password = 'hogehgoe'

    # config の一部の値は、コンストラクタ時に処理されているので、
    # 既にある Connection の config を後から変更しない方がいい。

    ただし、--hosts を指定せずに fab を起動した場合、
    taskに渡されるのは fabric.Connection ではなく、invoke.Context になるっぽい。
    そのため、 conn の host を取ろうとするとエラーになってしまうので注意。
    (user と port は、 fabコマンドで作られた incoke.Context なら取れるみたい。 )
    host がないと、fabric.Connection のコンストラクタも呼べないので、
    Connection を作るのは host が確定したタイミング以降でする。

コマンドにシェル解釈が必要な文字( ``&`` とか ``|`` とか ) が含まれている場合、
``bash -c 'command'`` の様に実行されているっぽい。
含まれていない場合、sshd から直接コマンドが実行されている (シェルの解釈されない)。

run() や sudo() に ``shell=`` をつけても効かないっぽい。
``shell=/bin/zsh`` としても、常に bash (ログインシェル？) で動いているっぽかった。
``shell=`` が効くのは Invoke の方だけか？ あとは fabric の local() なら効くかも。
    


タスクランナーを作らずに、単にpythonのライブラリとして使う場合
===================================================================

TODO
